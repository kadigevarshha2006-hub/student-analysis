import re
from typing import Dict, Any, List

STRONG_ACTION_VERBS = {
    "architected", "developed", "engineered", "designed", "built", "implemented",
    "optimized", "scaled", "containerized", "automated", "orchestrated", "reduced",
    "improved", "accelerated", "deployed", "integrated", "spearheaded", "mentored",
    "created", "streamlined", "configured", "launched", "migrated", "constructed",
    "programmed", "formulated", "established", "directed", "administered"
}

WEAK_PASSIVE_VERBS = {
    "worked on", "helped with", "assisted in", "responsible for", "handled", "participated in",
    "involved in", "did tasks", "helped"
}

def calculate_ats_and_quality_scores(
    raw_text: str,
    parsed_data: Dict[str, Any],
    extracted_skills: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Computes 3 distinct scores with itemized evidence checklists:
    1. ATS Compatibility (0-100)
    2. Resume Health (0-100)
    3. Section breakdown & itemized evidence
    """
    ats_checks: List[Dict[str, Any]] = []
    sections = parsed_data.get("sections", {})
    contact_info = parsed_data.get("personal_info", {})
    all_skills = extracted_skills.get("all_skills", [])
    categorized_skills = extracted_skills.get("categorized_skills", {})
    word_count = len(raw_text.split())

    # =============================================================
    # 1. ATS COMPATIBILITY ENGINE (Deterministic Evidence-Based)
    # =============================================================
    
    # Check 1: Contact Information Completeness with Specific Evidence
    contact_evidence = []
    contact_missing = []
    contact_score = 0.0

    if contact_info.get("name"):
        contact_evidence.append(f"✓ Name detected: {contact_info['name']}")
        contact_score += 20.0
    else:
        contact_missing.append("Candidate Full Name")

    if contact_info.get("email"):
        contact_evidence.append(f"✓ Email detected: {contact_info['email']}")
        contact_score += 25.0
    else:
        contact_missing.append("Email Address")

    if contact_info.get("phone"):
        contact_evidence.append(f"✓ Phone detected: {contact_info['phone']}")
        contact_score += 25.0
    else:
        contact_missing.append("Phone Number")

    if contact_info.get("linkedin"):
        contact_evidence.append(f"✓ LinkedIn detected: {contact_info['linkedin']}")
        contact_score += 15.0
    elif contact_info.get("github"):
        contact_evidence.append(f"✓ GitHub detected: {contact_info['github']}")
        contact_score += 15.0
    else:
        contact_missing.append("LinkedIn or GitHub profile link")

    if contact_info.get("location"):
        contact_evidence.append(f"✓ Location detected: {contact_info['location']}")
        contact_score += 15.0

    contact_score = min(100.0, contact_score)
    ats_checks.append({
        "check": "Contact Information Completeness",
        "status": "PASS" if contact_score >= 80 else "WARNING",
        "score": contact_score,
        "message": " | ".join(contact_evidence) if contact_evidence else "No contact information detected.",
        "recommendation": f"Add missing contact fields: {', '.join(contact_missing)}." if contact_missing else None
    })

    # Check 2: Standard Section Headings with Itemized Evidence
    detected_headers = []
    missing_headers = []
    std_sections_map = {
        "education": "Education",
        "skills": "Skills / Technical Stack",
        "projects": "Projects",
        "experience": "Work Experience / Internships"
    }

    for key, display_name in std_sections_map.items():
        content = sections.get(key, "").strip()
        if content and len(content.split()) >= 3:
            detected_headers.append(display_name)
        else:
            missing_headers.append(display_name)

    # If experience is missing but projects has strong bullets, candidate is undergraduate/student
    headings_score = (len(detected_headers) / len(std_sections_map)) * 100.0
    if len(detected_headers) >= 3:
        headings_score = max(headings_score, 85.0)

    ats_checks.append({
        "check": "Standard Section Headings",
        "status": "PASS" if len(detected_headers) >= 3 else "WARNING",
        "score": headings_score,
        "message": f"✓ Detected sections: {', '.join(detected_headers)}" + (f" (Optional missing: {', '.join(missing_headers)})" if missing_headers else ""),
        "recommendation": f"Ensure your resume contains clear headings for: {', '.join(missing_headers)}." if missing_headers and len(detected_headers) < 3 else None
    })

    # Check 3: Action Verb Strength
    raw_lower = raw_text.lower()
    words_in_doc = set(re.findall(r"\b[a-z]+\b", raw_lower))
    found_strong_verbs = sorted(list(words_in_doc.intersection(STRONG_ACTION_VERBS)))
    found_weak_verbs = [w for w in WEAK_PASSIVE_VERBS if w in raw_lower]

    verb_score = min(100.0, max(45.0, (len(found_strong_verbs) * 14.0) - (len(found_weak_verbs) * 8.0)))
    if len(found_strong_verbs) >= 4:
        verb_msg = f"✓ Detected {len(found_strong_verbs)} high-impact action verbs: {', '.join(found_strong_verbs[:6])}."
    else:
        verb_msg = f"Detected {len(found_strong_verbs)} action verbs: {', '.join(found_strong_verbs) if found_strong_verbs else 'None'}."

    ats_checks.append({
        "check": "Action Verb Strength",
        "status": "PASS" if len(found_strong_verbs) >= 3 else "WARNING",
        "score": verb_score,
        "message": verb_msg,
        "recommendation": "Begin each project/experience bullet with active power verbs (e.g. 'Architected', 'Engineered', 'Optimized', 'Integrated')." if len(found_strong_verbs) < 3 else None
    })

    # Check 4: Quantifiable Achievements & Metrics
    metrics_matches = re.findall(r"\b(?:\d+%(?:\s+increase|\s+reduction|\s+growth|\s+improvement)?|\$\d+[kKmM]?|\d+\+?\s*(?:users|ms|seconds|rps|clients|engineers|queries|apis|microservices|stars|contributions))\b", raw_text, re.IGNORECASE)
    metrics_count = len(metrics_matches)
    metrics_score = min(100.0, max(50.0, metrics_count * 25.0))

    ats_checks.append({
        "check": "Quantifiable Achievements & Metrics",
        "status": "PASS" if metrics_count >= 2 else "WARNING",
        "score": metrics_score,
        "message": f"✓ Detected {metrics_count} quantifiable metric expressions: {', '.join(metrics_matches[:4])}." if metrics_count > 0 else "No quantifiable percentages or numeric performance metrics detected.",
        "recommendation": "Consider adding measurable metrics where applicable (e.g. 'improved query latency by 35%', 'handled 500+ daily queries')." if metrics_count == 0 else None
    })

    # Check 5: Document Length & Parseability
    if word_count < 50:
        length_score = 20.0
        length_status = "FAIL"
        length_msg = f"Extracted text volume is only {word_count} words. Document may be an unread image or corrupted."
    elif 150 <= word_count <= 850:
        length_score = 100.0
        length_status = "PASS"
        length_msg = f"✓ Optimal document volume: {word_count} words (well within standard 250 - 750 words 1-page guideline)."
    else:
        length_score = 80.0
        length_status = "WARNING"
        length_msg = f"Total document length is {word_count} words."

    ats_checks.append({
        "check": "Resume Length & Text Volume",
        "status": length_status,
        "score": length_score,
        "message": length_msg,
        "recommendation": "Aim for a concise 1-page resume (300-600 words) for undergraduate/early career profiles." if word_count > 850 else None
    })

    # Calculate Overall ATS Compatibility Score
    ats_score = round(sum(c["score"] for c in ats_checks) / len(ats_checks), 1)

    # =============================================================
    # 2. RESUME HEALTH (Overall Quality, Breadth & Completeness)
    # =============================================================
    skills_count = len(all_skills)
    category_count = len(categorized_skills)
    skills_health = min(100.0, max(30.0, (skills_count * 5.0) + (category_count * 10.0)))

    projects_count = len(parsed_data.get("projects", []))
    projects_health = min(100.0, max(40.0, projects_count * 30.0))

    edu_count = len(parsed_data.get("education", []))
    edu_health = 100.0 if edu_count >= 1 else 50.0

    readability_score = min(98.0, max(75.0, 100.0 - (word_count > 900) * 12.0))
    formatting_score = round(min(98.0, (headings_score * 0.5) + (contact_score * 0.5)), 1)

    # Resume Health Composite
    resume_health_score = round(
        (ats_score * 0.30) +
        (skills_health * 0.30) +
        (projects_health * 0.25) +
        (edu_health * 0.15),
        1
    )

    # Strengths, Weaknesses, Recommendations
    strengths = []
    weaknesses = []
    recommendations = []

    if skills_count >= 8:
        strengths.append(f"Extensive technical skill coverage with {skills_count} verified technologies across {category_count} domains.")
    else:
        weaknesses.append("Technical keyword density could be broader.")
        recommendations.append("Explicitly list key languages, frameworks, and developer tools you have used.")

    if contact_score >= 80:
        strengths.append("Complete contact profile with accessible professional links.")

    if projects_count >= 2:
        strengths.append(f"Strong practical demonstration with {projects_count} documented technical projects.")

    if metrics_count == 0:
        weaknesses.append("Lack of quantifiable numeric metrics in project descriptions.")
        recommendations.append("Add measurable outcomes (e.g. '% response time reduction', 'number of active users') where available.")

    return {
        "overall_score": resume_health_score,
        "resume_health_score": resume_health_score,
        "ats_score": ats_score,
        "quality_score": resume_health_score,
        "skills_score": round(skills_health, 1),
        "readability_score": readability_score,
        "formatting_score": formatting_score,
        "section_breakdown": {
            "contact_info": round(contact_score, 1),
            "headings": round(headings_score, 1),
            "skills": round(skills_health, 1),
            "experience": round(min(100.0, max(50.0, len(parsed_data.get("experience", [])) * 30.0)), 1),
            "projects": round(projects_health, 1)
        },
        "ats_checks": ats_checks,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }
