import cv2
import numpy as np


def analyze_image(image_path):
    """
    Lightweight OpenCV-based visual risk analyzer.

    Returns visual scores for:
    - Flooding
    - Road Damage
    - Infrastructure
    - Obstruction
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to load image: {image_path}")

    # Resize for faster processing
    height, width = image.shape[:2]

    scale = min(800 / width, 800 / height, 1.0)

    if scale < 1.0:
        image = cv2.resize(
            image,
            (
                int(width * scale),
                int(height * scale)
            )
        )

    # ---------------------------------------------------------
    # Convert colour spaces
    # ---------------------------------------------------------

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    # ---------------------------------------------------------
    # 1. FLOODING DETECTION
    # ---------------------------------------------------------
    # Water often contains blue/cyan/low-saturation
    # reflective regions. This is a visual indicator,
    # not a trained flood classifier.

    blue_mask = (
        (h >= 85) &
        (h <= 130) &
        (s >= 35) &
        (v >= 45)
    )

    cyan_mask = (
        (h >= 75) &
        (h < 100) &
        (s >= 25) &
        (v >= 50)
    )

    dark_reflective_mask = (
        (v >= 35) &
        (v <= 150) &
        (s <= 100)
    )

    water_pixels = (
        blue_mask |
        cyan_mask |
        dark_reflective_mask
    )

    water_ratio = float(np.mean(water_pixels))

    flooding_score = min(
        100.0,
        water_ratio * 100 * 1.8
    )

    # ---------------------------------------------------------
    # 2. ROAD SURFACE / DAMAGE INDICATOR
    # ---------------------------------------------------------

    edges = cv2.Canny(
        gray,
        threshold1=70,
        threshold2=150
    )

    edge_ratio = float(np.mean(edges > 0))

    # Irregular surface texture
    texture_score = min(
        100.0,
        edge_ratio * 500
    )

    road_score = texture_score

    # ---------------------------------------------------------
    # 3. INFRASTRUCTURE INDICATOR
    # ---------------------------------------------------------

    contrast = float(np.std(gray))

    infrastructure_score = min(
        100.0,
        contrast * 1.5
    )

    # ---------------------------------------------------------
    # 4. OBSTRUCTION INDICATOR
    # ---------------------------------------------------------

    # Contours give an approximate measure of
    # object complexity in the scene.

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    significant_contours = [
        contour
        for contour in contours
        if cv2.contourArea(contour) > 100
    ]

    contour_score = min(
        100.0,
        len(significant_contours) * 2.5
    )

    obstruction_score = contour_score

    # ---------------------------------------------------------
    # RISK SCORES
    # ---------------------------------------------------------

    scores = {
        "Flooding": round(flooding_score, 2),
        "Road Damage": round(road_score, 2),
        "Infrastructure": round(infrastructure_score, 2),
        "Obstruction": round(obstruction_score, 2)
    }

    # ---------------------------------------------------------
    # CONDITION SELECTION
    # ---------------------------------------------------------

    detected_condition = max(
        scores,
        key=scores.get
    )

    confidence = scores[detected_condition]

    # Keep confidence within a sensible range
    confidence = max(
        30.0,
        min(95.0, confidence)
    )

    # ---------------------------------------------------------
    # SEVERITY
    # ---------------------------------------------------------

    if confidence >= 75:
        severity = "High"
        risk_level = "CRITICAL"

    elif confidence >= 55:
        severity = "Moderate"
        risk_level = "HIGH"

    elif confidence >= 40:
        severity = "Low"
        risk_level = "MODERATE"

    else:
        severity = "Low"
        risk_level = "LOW"

    # ---------------------------------------------------------
    # RECOMMENDED ACTION
    # ---------------------------------------------------------

    actions = {
        "Flooding":
            "Inspect water accumulation, drainage systems and affected roads.",

        "Road Damage":
            "Inspect road surfaces for potholes, cracks and structural damage.",

        "Infrastructure":
            "Inspect nearby public infrastructure for visible damage.",

        "Obstruction":
            "Inspect the area for garbage, debris or road blockages."
    }

    return {
        "condition": detected_condition,
        "confidence": round(confidence, 2),
        "severity": severity,
        "risk_level": risk_level,
        "scores": scores,
        "recommended_action": actions[detected_condition],

        "image_width": int(width),
        "image_height": int(height),

        "edge_ratio": round(edge_ratio, 4),
        "water_ratio": round(water_ratio, 4),
        "contrast": round(contrast, 2),
        "contours": len(significant_contours)
    }