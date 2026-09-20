import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "final_historical_risk.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "risk_fusion_features.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("Historical risk data loaded!")
print("Rows:", len(df))


# ============================================================
# RISK SIGNALS
# ============================================================

df["Rainfall_Signal"] = (
    df["Rainfall_Risk_Score"].fillna(0)
)

df["Historical_Flood_Signal"] = (
    df["Historical_Flood_Present"].fillna(0)
)


# ============================================================
# RISK FUSION
# ============================================================

df["Risk_Fusion_Score"] = (
    df["Rainfall_Signal"]
    + df["Historical_Flood_Signal"]
)


# ============================================================
# OVERALL RISK LEVEL
# ============================================================

def calculate_risk(score):

    if score >= 3:
        return "CRITICAL"

    elif score == 2:
        return "HIGH"

    elif score == 1:
        return "MODERATE"

    else:
        return "LOW"


df["Overall_Risk_Level"] = (
    df["Risk_Fusion_Score"]
    .apply(calculate_risk)
)


# ============================================================
# RECOMMENDED ACTION
# ============================================================

def recommend_action(risk):

    if risk == "CRITICAL":
        return (
            "Immediate emergency monitoring and "
            "preparedness recommended."
        )

    elif risk == "HIGH":
        return (
            "Increase monitoring and prepare "
            "local response resources."
        )

    elif risk == "MODERATE":
        return (
            "Continue monitoring rainfall and "
            "historical flood conditions."
        )

    else:
        return (
            "Routine monitoring recommended."
        )


df["Recommended_Action"] = (
    df["Overall_Risk_Level"]
    .apply(recommend_action)
)


# ============================================================
# SAVE RESULT
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# RESULTS
# ============================================================

print("\n========================================")
print("RISK FUSION COMPLETED")
print("========================================")

print("\nRisk Fusion Distribution:")

print(
    df["Overall_Risk_Level"]
    .value_counts()
)


print("\nSample Results:")

print(
    df[
        [
            "State",
            "Year",
            "Rainfall_Signal",
            "Historical_Flood_Signal",
            "Risk_Fusion_Score",
            "Overall_Risk_Level"
        ]
    ].head(10)
)


print("\nSaved to:")

print(OUTPUT_PATH)