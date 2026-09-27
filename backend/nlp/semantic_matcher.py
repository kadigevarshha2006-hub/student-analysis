import math
from typing import Dict, Any, List, Set, Tuple
from backend.nlp.skill_extractor import skill_extractor
from backend.nlp.skill_taxonomy import get_canonical_skill

# Lazy-loaded SentenceTransformer model
_sbert_model = None

def get_sentence_transformer():
    global _sbert_model
    if _sbert_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _sbert_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print(f"SentenceTransformer load notice: {e}. Using TF-IDF fallback matcher.")
            _sbert_model = False
    return _sbert_model

def compute_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Computes cosine similarity between two dense vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return max(0.0, min(1.0, dot_product / (norm1 * norm2)))

def calculate_fallback_similarity(text1: str, text2: str) -> float:
    """Fallback Jaccard/TF-IDF word overlap similarity."""
    words1 = set(w.lower() for w in text1.split() if len(w) > 2)
    words2 = set(w.lower() for w in text2.split() if len(w) > 2)
    if not words1 or not words2:
        return 0.5
    overlap = len(words1.intersection(words2))
    return min(1.0, (2.0 * overlap) / (len(words1) + len(words2)))

# Transferable skill relationships for Partial Matching
TRANSFERABLE_SKILLS_MAP = {
    "PostgreSQL": ["MySQL", "SQL", "SQLite", "Oracle DB"],
    "MySQL": ["PostgreSQL", "SQL", "SQLite"],
    "Kubernetes": ["Docker", "Microservices", "CI/CD"],
    "Docker": ["Linux", "CI/CD"],
    "AWS": ["Cloud", "Google Cloud Platform", "Azure", "Docker"],
    "Azure": ["AWS", "Google Cloud Platform", "Cloud"],
    "Google Cloud Platform": ["AWS", "Azure", "Cloud"],
    "TypeScript": ["JavaScript"],
    "Vue.js": ["React", "JavaScript", "HTML", "CSS"],
    "Angular": ["React", "TypeScript", "JavaScript"],
    "FastAPI": ["Flask", "Django", "Python", "REST APIs"],
    "Django": ["FastAPI", "Flask", "Python"],
    "PyTorch": ["TensorFlow", "Machine Learning", "Python"],
    "TensorFlow": ["PyTorch", "Machine Learning", "Python"],
    "Scikit-learn": ["Python", "Pandas", "NumPy", "Machine Learning"],
    "Next.js": ["React", "JavaScript", "Node.js"]
}

def match_resume_to_job(
    resume_text: str,
    job_text: str,
    resume_skills: List[str]
) -> Dict[str, Any]:
    """
    Computes 3-tier skill matching (MATCHED, PARTIALLY MATCHED, MISSING) and semantic vector similarity.
    """
    # 1. Normalize resume skills to canonical names
    res_skills_set = set(get_canonical_skill(s) for s in resume_skills)

    # 2. Extract and canonicalize job requirements from JD text
    job_extracted = skill_extractor.extract_skills_from_text(job_text)
    job_skills_set = set(job_extracted.get("all_skills", []))

    # Also check if any raw job words match canonical skills
    for word in job_text.split():
        canon = get_canonical_skill(word.strip(".,;:()[]{}"))
        if canon in [s["name"] for s in skill_extractor.skills_flat]:
            job_skills_set.add(canon)

    matching_skills: List[str] = []
    partial_skills: List[Dict[str, str]] = []
    missing_skills: List[str] = []

    for req in sorted(list(job_skills_set)):
        canon_req = get_canonical_skill(req)
        
        # A. Exact or Canonical Match
        if canon_req in res_skills_set:
            matching_skills.append(canon_req)
        else:
            # B. Check for Partial/Transferable Skill
            related_found = None
            if canon_req in TRANSFERABLE_SKILLS_MAP:
                for related in TRANSFERABLE_SKILLS_MAP[canon_req]:
                    if related in res_skills_set:
                        related_found = related
                        break

            if related_found:
                partial_skills.append({
                    "skill": canon_req,
                    "demonstrated_alternative": related_found,
                    "reason": f"Candidate has verified proficiency in {related_found}, which provides transferable foundational knowledge for {canon_req}."
                })
            else:
                # C. Missing Requirement
                missing_skills.append(canon_req)

    # Calculate 3-tier skill match score
    total_reqs = len(job_skills_set)
    if total_reqs > 0:
        raw_skill_score = ((len(matching_skills) * 1.0) + (len(partial_skills) * 0.5)) / total_reqs * 100.0
        skill_match_score = min(100.0, max(0.0, raw_skill_score))
    else:
        skill_match_score = 80.0

    # 3. Compute Semantic Similarity (Sentence Transformers)
    model = get_sentence_transformer()
    if model:
        try:
            embeddings = model.encode([resume_text[:2000], job_text[:2000]])
            sim = compute_cosine_similarity(embeddings[0].tolist(), embeddings[1].tolist())
            semantic_score = round(sim * 100.0, 1)
        except Exception as e:
            print(f"Error encoding embeddings: {e}")
            semantic_score = round(calculate_fallback_similarity(resume_text, job_text) * 100.0, 1)
    else:
        semantic_score = round(calculate_fallback_similarity(resume_text, job_text) * 100.0, 1)

    experience_relevance = round(min(100.0, (semantic_score * 0.5) + (skill_match_score * 0.5)), 1)
    
    overall_match = round(
        (skill_match_score * 0.55) +
        (semantic_score * 0.30) +
        (experience_relevance * 0.15),
        1
    )

    # 4. Prioritize Missing Skills (High, Medium, Low)
    high_priority = []
    medium_priority = []
    low_priority = []

    for skill in missing_skills:
        lower_skill = skill.lower()
        if lower_skill in job_text.lower() and any(req_word in job_text.lower() for req_word in ["required", "must have", "proficient", "essential", "core"]):
            high_priority.append({
                "skill": skill,
                "reason": "Explicitly listed as a mandatory requirement in the job description."
            })
        elif skill in ["Docker", "AWS", "Kubernetes", "SQL", "React", "Python", "FastAPI", "CI/CD"]:
            medium_priority.append({
                "skill": skill,
                "reason": "Core standard technology in high demand for this engineering profile."
            })
        else:
            low_priority.append({
                "skill": skill,
                "reason": "Beneficial secondary or domain-specific tool."
            })

    if not high_priority and missing_skills:
        for s in missing_skills[:2]:
            high_priority.append({
                "skill": s,
                "reason": "Key requirement mentioned in the target role description."
            })
        for s in missing_skills[2:4]:
            medium_priority.append({"skill": s, "reason": "Standard secondary requirement."})
        for s in missing_skills[4:]:
            low_priority.append({"skill": s, "reason": "Optional preferred qualification."})

    return {
        "overall_match_percentage": overall_match,
        "semantic_similarity_score": semantic_score,
        "skill_match_score": round(skill_match_score, 1),
        "experience_relevance_score": experience_relevance,
        "matching_skills": matching_skills,
        "partial_skills": partial_skills,
        "missing_skills": missing_skills,
        "skill_gap_priority": {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        }
    }
