from dataclasses import dataclass, asdict


# ============================================================
# RISK RESULT
# ============================================================

@dataclass
class RiskResult:

    rainfall_risk: float
    historical_flood_risk: float
    image_risk: float
    report_risk: float
    road_risk: float
    infrastructure_risk: float

    final_score: float
    risk_level: str
    recommended_action: str

    def to_dict(self):
        return asdict(self)


# ============================================================
# COMMON RISK ENGINE
# ============================================================

class RiskEngine:

    # Original project weights
    WEIGHTS = {
        "rainfall": 0.25,
        "historical_flood": 0.20,
        "image": 0.15,
        "report": 0.10,
        "road": 0.15,
        "infrastructure": 0.15,
    }

    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    @staticmethod
    def normalize(value):

        if value is None:
            return None

        try:
            value = float(value)
        except (TypeError, ValueError):
            return None

        return max(
            0.0,
            min(100.0, value)
        )

    # --------------------------------------------------------
    # RISK LEVEL
    # --------------------------------------------------------

    @staticmethod
    def get_risk_level(score):

        if score >= 75:
            return "Critical"

        elif score >= 50:
            return "High"

        elif score >= 25:
            return "Moderate"

        else:
            return "Low"

    # --------------------------------------------------------
    # RECOMMENDED ACTION
    # --------------------------------------------------------

    @staticmethod
    def get_recommendation(level):

        if level == "Critical":

            return (
                "Immediate attention required. "
                "Prioritize inspection, monitoring and "
                "appropriate emergency preparedness."
            )

        elif level == "High":

            return (
                "Increase monitoring and prioritize inspection "
                "of affected areas. Prepare maintenance and "
                "response teams."
            )

        elif level == "Moderate":

            return (
                "Continue monitoring conditions and inspect "
                "areas showing elevated risk."
            )

        else:

            return (
                "Current available signals indicate relatively "
                "low community risk. Continue routine monitoring."
            )

    # --------------------------------------------------------
    # CALCULATE RISK
    # --------------------------------------------------------

    def calculate(
        self,
        rainfall=None,
        historical_flood=None,
        image=None,
        report=None,
        road=None,
        infrastructure=None
    ):

        signals = {
            "rainfall": self.normalize(rainfall),
            "historical_flood": self.normalize(
                historical_flood
            ),
            "image": self.normalize(image),
            "report": self.normalize(report),
            "road": self.normalize(road),
            "infrastructure": self.normalize(
                infrastructure
            ),
        }

        # ----------------------------------------------------
        # IMPORTANT:
        # Only signals that are actually available are used.
        # None = unavailable.
        # 0 = genuinely available signal with zero risk.
        # ----------------------------------------------------

        active_signals = {
            name: value
            for name, value in signals.items()
            if value is not None
        }

        if not active_signals:

            final_score = 0.0

        else:

            active_weight_total = sum(
                self.WEIGHTS[name]
                for name in active_signals
            )

            weighted_score = sum(
                active_signals[name]
                * self.WEIGHTS[name]
                for name in active_signals
            )

            # Re-normalize using only available signals.
            final_score = (
                weighted_score / active_weight_total
            )

        final_score = round(
            max(
                0.0,
                min(100.0, final_score)
            ),
            2
        )

        risk_level = self.get_risk_level(
            final_score
        )

        recommended_action = self.get_recommendation(
            risk_level
        )

        return RiskResult(

            rainfall_risk=(
                signals["rainfall"]
                if signals["rainfall"] is not None
                else 0.0
            ),

            historical_flood_risk=(
                signals["historical_flood"]
                if signals["historical_flood"] is not None
                else 0.0
            ),

            image_risk=(
                signals["image"]
                if signals["image"] is not None
                else 0.0
            ),

            report_risk=(
                signals["report"]
                if signals["report"] is not None
                else 0.0
            ),

            road_risk=(
                signals["road"]
                if signals["road"] is not None
                else 0.0
            ),

            infrastructure_risk=(
                signals["infrastructure"]
                if signals["infrastructure"] is not None
                else 0.0
            ),

            final_score=final_score,
            risk_level=risk_level,
            recommended_action=recommended_action
        )


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def calculate_risk(
    rainfall=None,
    historical_flood=None,
    image=None,
    report=None,
    road=None,
    infrastructure=None
):

    engine = RiskEngine()

    result = engine.calculate(

        rainfall=rainfall,

        historical_flood=historical_flood,

        image=image,

        report=report,

        road=road,

        infrastructure=infrastructure
    )

    return result.to_dict()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "JEEVAN-NETRA Common Risk Engine Test"
    )

    print("-" * 50)

    # Test 1: Report only
    report_test = calculate_risk(
        report=60
    )

    print(
        "Report Only:",
        report_test["final_score"],
        report_test["risk_level"]
    )

    # Test 2: Image + Road + Infrastructure
    image_test = calculate_risk(
        image=95,
        road=96.63,
        infrastructure=72.50
    )

    print(
        "Image Intelligence:",
        image_test["final_score"],
        image_test["risk_level"]
    )

    # Test 3: Rainfall + Historical Flood
    historical_test = calculate_risk(
        rainfall=80,
        historical_flood=70
    )

    print(
        "Historical Signals:",
        historical_test["final_score"],
        historical_test["risk_level"]
    )

    print("-" * 50)

    print(
        "Risk Engine test completed."
    )