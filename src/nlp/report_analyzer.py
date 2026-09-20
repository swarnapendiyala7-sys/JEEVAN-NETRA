import re
from pathlib import Path


def analyze_report(text):
    """
    Lightweight NLP-based community report analyzer.

    Extracts:
    - incident type
    - risk keywords
    - possible location
    - severity
    - recommended action
    """

    if not text or not text.strip():
        raise ValueError("Report text cannot be empty.")

    text_lower = text.lower()

    # ---------------------------------------------------------
    # INCIDENT KEYWORDS
    # ---------------------------------------------------------

    incident_keywords = {
        "Flooding": [
            "flood",
            "flooded",
            "waterlogging",
            "water logged",
            "water accumulation",
            "heavy rain",
            "overflow"
        ],

        "Road Damage": [
            "pothole",
            "road damage",
            "road damaged",
            "broken road",
            "crack in road",
            "damaged road"
        ],

        "Electrical Hazard": [
            "electric shock",
            "electrical",
            "short circuit",
            "power line",
            "electric wire",
            "sparking",
            "spark",
            "transformer"
        ],

        "Fire": [
            "fire",
            "smoke",
            "burning",
            "flames"
        ],

        "Infrastructure Damage": [
            "building damage",
            "building damaged",
            "wall collapsed",
            "bridge damage",
            "bridge damaged",
            "roof damage",
            "structure damaged",
            "collapsed"
        ],

        "Garbage / Obstruction": [
            "garbage",
            "trash",
            "waste",
            "debris",
            "blocked road",
            "obstruction",
            "blockage"
        ]
    }

    # ---------------------------------------------------------
    # DETECT INCIDENTS
    # ---------------------------------------------------------

    detected_incidents = []

    incident_scores = {}

    for incident, keywords in incident_keywords.items():

        matched_keywords = []

        for keyword in keywords:

            if keyword in text_lower:
                matched_keywords.append(keyword)

        if matched_keywords:

            detected_incidents.append(incident)

            incident_scores[incident] = matched_keywords


    # ---------------------------------------------------------
    # RISK KEYWORDS
    # ---------------------------------------------------------

    risk_keywords = [
        "danger",
        "dangerous",
        "risk",
        "critical",
        "emergency",
        "urgent",
        "injury",
        "injured",
        "death",
        "fatality",
        "trapped",
        "blocked",
        "collapsed",
        "sparking",
        "overflow"
    ]

    detected_risk_keywords = [
        keyword
        for keyword in risk_keywords
        if keyword in text_lower
    ]


    # ---------------------------------------------------------
    # LOCATION EXTRACTION
    # ---------------------------------------------------------

    location = "Location not identified"

    location_patterns = [
        r"\b(?:at|near|in|around)\s+([A-Za-z][A-Za-z\s]{2,40})",
        r"\b(?:road|street|area|colony|village|town)\s+([A-Za-z][A-Za-z\s]{2,40})"
    ]

    for pattern in location_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            location = match.group(1).strip()

            # Remove common trailing words
            location = re.sub(
                r"\s+(and|is|was|has|have|with)$",
                "",
                location,
                flags=re.IGNORECASE
            )

            break


    # ---------------------------------------------------------
    # SEVERITY
    # ---------------------------------------------------------

    critical_words = [
        "critical",
        "emergency",
        "trapped",
        "death",
        "fatality",
        "collapsed",
        "fire",
        "electric shock",
        "sparking"
    ]

    high_words = [
        "danger",
        "dangerous",
        "urgent",
        "injury",
        "injured",
        "overflow",
        "blocked"
    ]

    if any(word in text_lower for word in critical_words):

        severity = "Critical"
        risk_level = "CRITICAL"

    elif any(word in text_lower for word in high_words):

        severity = "High"
        risk_level = "HIGH"

    elif detected_incidents:

        severity = "Moderate"
        risk_level = "MODERATE"

    else:

        severity = "Low"
        risk_level = "LOW"


    # ---------------------------------------------------------
    # RECOMMENDED ACTION
    # ---------------------------------------------------------

    actions = {

        "Flooding":
            "Inspect water accumulation and drainage systems. "
            "Restrict access to severely flooded areas if necessary.",

        "Road Damage":
            "Inspect the damaged road and identify potholes, cracks "
            "or structural problems. Notify the responsible authority.",

        "Electrical Hazard":
            "Keep people away from the affected area and immediately "
            "notify electrical maintenance personnel.",

        "Fire":
            "Treat the incident as an emergency. Keep people away "
            "and contact emergency response services.",

        "Infrastructure Damage":
            "Restrict access to the damaged structure and request "
            "an immediate structural inspection.",

        "Garbage / Obstruction":
            "Inspect and clear the obstruction while maintaining "
            "safe access for the public."
    }


    if detected_incidents:

        primary_incident = detected_incidents[0]

        recommended_action = actions[primary_incident]

    else:

        primary_incident = "Unknown"

        recommended_action = (
            "Review the report manually and determine the appropriate "
            "response."
        )


    # ---------------------------------------------------------
    # RISK SCORE
    # ---------------------------------------------------------

    risk_score = 0

    risk_score += len(detected_incidents) * 20
    risk_score += len(detected_risk_keywords) * 10

    if severity == "Critical":
        risk_score += 40

    elif severity == "High":
        risk_score += 30

    elif severity == "Moderate":
        risk_score += 20

    risk_score = min(
        100,
        risk_score
    )


    # ---------------------------------------------------------
    # RESULT
    # ---------------------------------------------------------

    return {

        "incident": primary_incident,

        "detected_incidents":
            detected_incidents,

        "matched_keywords":
            incident_scores,

        "risk_keywords":
            detected_risk_keywords,

        "location":
            location,

        "severity":
            severity,

        "risk_level":
            risk_level,

        "risk_score":
            risk_score,

        "recommended_action":
            recommended_action,

        "report_length":
            len(text),

        "word_count":
            len(text.split())
    }