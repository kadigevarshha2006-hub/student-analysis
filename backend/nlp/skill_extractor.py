import re
from typing import Dict, List, Set, Any
from backend.nlp.skill_taxonomy import SKILL_TAXONOMY, get_all_skills_flat, get_canonical_skill

class SkillExtractor:
    def __init__(self):
        self.skills_flat = get_all_skills_flat()

    def extract_skills_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extracts and categorizes skills across the entire text body (skills section, projects, experience, etc.)
        Normalizes all aliases to canonical skill names.
        """
        if not text:
            return {"categorized_skills": {}, "all_skills": [], "skill_details": []}

        # Normalize text with padding for reliable boundary detection
        lower_text = " " + re.sub(r"[,/|;()\[\]{}•\-]", " ", text.lower()) + " "
        found_skills_map: Dict[str, Dict[str, Any]] = {}

        for item in self.skills_flat:
            canonical_name = item["name"]
            category = item["category"]
            aliases = item["aliases"] or []

            # Check canonical name and all known aliases
            search_terms = [canonical_name.lower()] + [a.lower() for a in aliases]

            for term in search_terms:
                if not term.strip():
                    continue

                # Word boundary matching with protection for single-letter and symbol-rich terms
                if term in ["c", "r", "go"]:
                    pattern = rf"\b{re.escape(term)}\b(?:\s+(?:programming|language|developer|code|dev|script)|\s*[\n,;])"
                elif term in ["c++", "c#", ".net"]:
                    pattern = rf"(?:\s|^){re.escape(term)}(?:\s|$|[,;])"
                else:
                    pattern = rf"\b{re.escape(term)}\b"

                if re.search(pattern, lower_text, re.IGNORECASE):
                    if canonical_name not in found_skills_map:
                        found_skills_map[canonical_name] = {
                            "name": canonical_name,
                            "category": category,
                            "confidence": 1.0,
                            "source": "explicit"
                        }
                    break

        # Group by category
        categorized: Dict[str, List[str]] = {}
        for item in found_skills_map.values():
            cat = item["category"]
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(item["name"])

        all_skills = sorted(list(found_skills_map.keys()))
        skill_details = list(found_skills_map.values())

        return {
            "categorized_skills": categorized,
            "all_skills": all_skills,
            "skill_details": skill_details
        }

# Global singleton instance
skill_extractor = SkillExtractor()
