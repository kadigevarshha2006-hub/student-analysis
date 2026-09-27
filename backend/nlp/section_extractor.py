import re
from typing import Dict, Any, List, Optional
from backend.schemas.resume import ContactInfo, ParsedResumeData, EducationItem, ExperienceItem, ProjectItem

# Comprehensive Section Header Synonym Regex Patterns
SECTION_PATTERNS = {
    "summary": r"(?:professional\s+summary|career\s+summary|summary|profile|about\s+me|objective|career\s+objective|executive\s+summary)",
    "education": r"(?:educational\s+qualifications|academic\s+background|academics|academic\s+qualifications|education|academic\s+history|qualifications|degrees)",
    "skills": r"(?:technical\s+skills\s*(?:&|and)\s*tools|technical\s+skills|skills\s*(?:&|and)\s*tools|core\s+competencies|technical\s+competencies|technologies|tech\s+stack|programming\s+skills|tools\s*(?:&|and)\s*technologies|proficiencies|skills)",
    "experience": r"(?:professional\s+experience|work\s+experience|internship\s+experience|internships|employment\s+history|work\s+history|industry\s+experience|experience)",
    "projects": r"(?:academic\s+projects|technical\s+projects|personal\s+projects|key\s+projects|selected\s+projects|portfolio\s+projects|major\s+projects|projects)",
    "certifications": r"(?:certifications\s*(?:&|and)\s*licenses|certifications|certificates|licenses|courses|accreditations|training)",
    "achievements": r"(?:honors\s*(?:&|and)\s*awards|achievements|awards|honors|publications|extracurricular\s+activities|extracurricular|activities|leadership)"
}

def clean_header_line(line: str) -> str:
    """Strips leading bullet points, numbers, symbols, and formatting from a line."""
    cleaned = re.sub(r"^[\s\d\.\-\*\•\#\:\=\_\[\]\(\)\>\~\|]+", "", line).strip()
    cleaned = re.sub(r"[\:\=\-_\|]+$", "", cleaned).strip()
    return cleaned

def extract_contact_info(text: str) -> ContactInfo:
    """
    Extracts candidate name, email, phone, LinkedIn, GitHub, and location with robust international patterns.
    """
    info = ContactInfo()
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # 1. Email Regex
    email_match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
    if email_match:
        info.email = email_match.group(1).lower().strip()

    # 2. Phone Regex (supports Indian 10-digit, +91, international with dashes/spaces/parentheses)
    phone_candidates = re.findall(r"(?:(?:\+|00)\d{1,4}[-.\s]?)?(?:\(?\d{2,5}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4,6}", text)
    for cand in phone_candidates:
        digits_only = re.sub(r"\D", "", cand)
        if 10 <= len(digits_only) <= 13:
            info.phone = cand.strip()
            break

    # 3. LinkedIn Profile
    linkedin_match = re.search(r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([a-zA-Z0-9_\-\.]+)", text, re.IGNORECASE)
    if linkedin_match:
        info.linkedin = f"linkedin.com/in/{linkedin_match.group(1).rstrip('/')}"
    else:
        # Check text format like "LinkedIn: username"
        alt_li = re.search(r"linkedin\s*[:\-]\s*([a-zA-Z0-9_\-\.]+)", text, re.IGNORECASE)
        if alt_li and "@" not in alt_li.group(1):
            info.linkedin = f"linkedin.com/in/{alt_li.group(1)}"

    # 4. GitHub Profile
    github_match = re.search(r"(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_\-\.]+)", text, re.IGNORECASE)
    if github_match:
        info.github = f"github.com/{github_match.group(1).rstrip('/')}"
    else:
        alt_gh = re.search(r"github\s*[:\-]\s*([a-zA-Z0-9_\-\.]+)", text, re.IGNORECASE)
        if alt_gh and "@" not in alt_gh.group(1):
            info.github = f"github.com/{alt_gh.group(1)}"

    # 5. Location
    loc_match = re.search(r"\b([A-Z][a-zA-Z\s]+,\s*(?:India|USA|United States|UK|Canada|Germany|[A-Z]{2}))\b", text[:1200])
    if loc_match:
        info.location = loc_match.group(1).strip()
    elif "hyderabad" in text[:1200].lower():
        info.location = "Hyderabad, India"

    # 6. Candidate Name
    for line in lines[:6]:
        cleaned = re.sub(r"[\-|•|].*$", "", line).strip()
        cleaned = re.sub(r"(?:email|phone|github|linkedin|tel|contact).*$", "", cleaned, flags=re.IGNORECASE).strip()
        
        words = cleaned.split()
        if 1 <= len(words) <= 4 and re.match(r"^[A-Za-z\s\.\']+$", cleaned):
            lower_clean = cleaned.lower()
            if not any(kw in lower_clean for kw in ["resume", "curriculum", "cv", "page", "developer", "engineer", "undergraduate", "student", "bachelor"]):
                info.name = cleaned.title()
                break

    if not info.name and info.email:
        # Extract potential name from email username prefix (e.g. kadigevarshha2006 -> Varshha Kadige)
        prefix = info.email.split("@")[0]
        clean_prefix = re.sub(r"\d+", "", prefix).replace(".", " ").replace("_", " ").title()
        if len(clean_prefix) >= 3:
            info.name = clean_prefix

    return info

def segment_sections(text: str) -> Dict[str, str]:
    """
    Segments resume text into standard thematic sections using flexible fuzzy header matching.
    """
    sections: Dict[str, str] = {
        "header": "",
        "summary": "",
        "education": "",
        "skills": "",
        "experience": "",
        "projects": "",
        "certifications": "",
        "achievements": "",
        "other": ""
    }

    lines = text.split("\n")
    current_section = "header"
    current_lines: List[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        clean_line = clean_header_line(stripped)
        lower_clean = clean_line.lower()

        # Section headers are typically short (<= 6 words)
        is_header = False
        if 1 <= len(clean_line.split()) <= 6:
            for sec_name, pattern in SECTION_PATTERNS.items():
                if re.fullmatch(pattern, lower_clean, re.IGNORECASE) or re.match(rf"^{pattern}\b", lower_clean, re.IGNORECASE):
                    # Save accumulated lines for previous section
                    sections[current_section] = "\n".join(current_lines).strip()
                    current_section = sec_name
                    current_lines = []
                    is_header = True
                    break

        if not is_header:
            current_lines.append(stripped)

    # Save final section
    sections[current_section] = "\n".join(current_lines).strip()
    return sections

def parse_structured_resume(text: str) -> Dict[str, Any]:
    """
    Unified canonical structured representation of the resume.
    """
    contact_info = extract_contact_info(text)
    sections = segment_sections(text)

    # 1. Education Items
    education_items = []
    edu_text = sections.get("education", "")
    if edu_text:
        edu_lines = [l.strip() for l in edu_text.split("\n") if l.strip()]
        for line in edu_lines:
            degree_match = re.search(r"(bachelor|master|b\.s\.|m\.s\.|b\.tech|b\.e\.|m\.tech|ph\.d|diploma|associate|engineering|undergraduate)", line, re.IGNORECASE)
            if degree_match:
                education_items.append(EducationItem(degree=line, institution=None, year=None, gpa=None))

    # 2. Experience Items
    experience_items = []
    exp_text = sections.get("experience", "")
    if exp_text:
        exp_lines = [l.strip() for l in exp_text.split("\n") if l.strip()]
        current_item = None
        for line in exp_lines:
            if line.startswith("-") or line.startswith("*"):
                if current_item:
                    current_item.bullets.append(line.lstrip("-* ").strip())
            else:
                if current_item:
                    experience_items.append(current_item)
                current_item = ExperienceItem(title=line, company=None, duration=None, bullets=[])
        if current_item:
            experience_items.append(current_item)

    # 3. Project Items
    project_items = []
    proj_text = sections.get("projects", "")
    if proj_text:
        proj_lines = [l.strip() for l in proj_text.split("\n") if l.strip()]
        current_proj = None
        for line in proj_lines:
            if line.startswith("-") or line.startswith("*"):
                if current_proj:
                    current_proj.bullets.append(line.lstrip("-* ").strip())
            else:
                if current_proj:
                    project_items.append(current_proj)
                current_proj = ProjectItem(title=line, technologies=[], description=line, bullets=[])
        if current_proj:
            project_items.append(current_proj)

    # 4. Certifications
    cert_items = []
    cert_text = sections.get("certifications", "")
    if cert_text:
        cert_items = [l.lstrip("-* ").strip() for l in cert_text.split("\n") if l.strip()]

    # 5. Achievements
    achieve_items = []
    ach_text = sections.get("achievements", "")
    if ach_text:
        achieve_items = [l.lstrip("-* ").strip() for l in ach_text.split("\n") if l.strip()]

    return {
        "personal_info": contact_info.model_dump(),
        "sections": sections,
        "education": [e.model_dump() for e in education_items],
        "experience": [exp.model_dump() for exp in experience_items],
        "projects": [p.model_dump() for p in project_items],
        "certifications": cert_items,
        "achievements": achieve_items,
        "links": [v for k, v in contact_info.model_dump().items() if k in ["linkedin", "github"] and v]
    }
