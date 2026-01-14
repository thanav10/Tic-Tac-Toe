
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple
import time
import math
import json

# -----------------------------
# Data models
# -----------------------------

@dataclass
class VisionFeatures:
    """Outputs from your vision model (real or stub)."""
    wound_type: str                         # 'laceration','burn','bruise','swelling','deformity','infection', etc.
    area_cm2: float                         # estimated surface area
    depth_mm: float                         # estimated depth (if known; else 0)
    active_bleeding: bool
    location: str                           # 'hand','face','joint','limb','torso','head','eye'
    contamination: bool
    deformity: bool
    infection_signs: bool
    pain_0_10: float
    mechanism: str                          # 'cut','fall','burn','crush','unknown'
    model_confidence: float                 # 0..1
    red_flags: List[str] = field(default_factory=list)  # e.g., ["exposed_bone","eye_injury","airway","altered_consciousness"]

@dataclass
class IntakeAnswers:
    """Short questionnaire answers (non-vision)."""
    tetanus_outdated: bool = False
    on_anticoagulants: bool = False
    numbness_or_tingling: bool = False
    age_years: Optional[int] = None

@dataclass
class TriageDecision:
    band: str                 # 'immediate','urgent','standard'
    severity: float           # 0..100
    reasons: List[str]
    confidence: float         # propagated model confidence (0..1)
    suggested_destination: str
    est_duration_min: int

# -----------------------------
# Vision model interface (stub)
# -----------------------------

class VisionModelStub:
    """
    Replace this class with your real model.
    For now, it simply accepts a dict of features and validates/provides defaults.
    """
    VALID_TYPES = {"laceration","burn","bruise","swelling","deformity","infection"}
    VALID_LOCS = {"hand","face","joint","limb","torso","head","eye"}
    VALID_MECH = {"cut","fall","burn","crush","unknown"}

    def predict(self, features: Dict[str, Any]) -> VisionFeatures:
        # Defensive defaults
        wt = str(features.get("wound_type","laceration")).lower()
        if wt not in self.VALID_TYPES:
            wt = "laceration"
        loc = str(features.get("location","limb")).lower()
        if loc not in self.VALID_LOCS:
            loc = "limb"
        mech = str(features.get("mechanism","unknown")).lower()
        if mech not in self.VALID_MECH:
            mech = "unknown"

        vf = VisionFeatures(
            wound_type = wt,
            area_cm2 = float(features.get("area_cm2", 1.0)),
            depth_mm = float(features.get("depth_mm", 0.0)),
            active_bleeding = bool(features.get("active_bleeding", False)),
            location = loc,
            contamination = bool(features.get("contamination", False)),
            deformity = bool(features.get("deformity", False)),
            infection_signs = bool(features.get("infection_signs", False)),
            pain_0_10 = float(features.get("pain_0_10", 3.0)),
            mechanism = mech,
            model_confidence = float(features.get("model_confidence", 0.85)),
            red_flags = list(features.get("red_flags", [])),
        )
        return vf

# -----------------------------
# Severity scoring
# -----------------------------

class SeverityScorer:
    """
    A transparent, rule-augmented severity scorer producing 0..100 and triage band.
    Override rules trump the numeric score.
    """
    # Band thresholds
    THRESH_IMMEDIATE = 85.0
    THRESH_URGENT = 60.0

    # Targets & weights can be tuned with clinical feedback
    DESTINATION_BY_TYPE = {
        "laceration": ("suturing_room", 25),
        "burn": ("burn_care", 30),
        "bruise": ("fast_track", 10),
        "swelling": ("fast_track", 10),
        "deformity": ("imaging", 40),
        "infection": ("fast_track", 20),
    }

    LOCATION_RISK = {
        "eye": 1.0, "face": 0.8, "head": 0.8,
        "hand": 0.7, "joint": 0.7,
        "torso": 0.5, "limb": 0.4,
    }

    MECHANISM_RISK = {"crush": 1.0, "burn": 0.7, "fall": 0.5, "cut": 0.4, "unknown": 0.3}

    def score(self, vf: VisionFeatures, answers: IntakeAnswers) -> TriageDecision:
        reasons: List[str] = []
        # 1) Hard overrides (red flags -> immediate)
        if vf.red_flags:
            reasons += [f"red_flag:{rf}" for rf in vf.red_flags]
            band = "immediate"
            severity = 100.0
            dest, dur = self.DESTINATION_BY_TYPE.get(vf.wound_type, ("fast_track", 15))
            return TriageDecision(band, severity, reasons, vf.model_confidence, dest, dur)

        # 2) Numeric fusion
        size_norm = min(vf.area_cm2 / 10.0, 1.0)        # area >=10 cm2 saturates
        depth_norm = min(vf.depth_mm / 10.0, 1.0)       # depth >=10 mm saturates
        bleed = 1.0 if vf.active_bleeding else 0.0
        inf = 1.0 if vf.infection_signs else 0.0
        contam = 1.0 if vf.contamination else 0.0

        loc_risk = self.LOCATION_RISK.get(vf.location, 0.4)
        mech_risk = self.MECHANISM_RISK.get(vf.mechanism, 0.3)
        pain_norm = max(0.0, min(vf.pain_0_10 / 10.0, 1.0))

        # Weighted sum (tunable)
        severity = (
            30.0 * size_norm +
            25.0 * depth_norm +
            20.0 * bleed +
            10.0 * loc_risk +
            5.0  * mech_risk +
            5.0  * pain_norm +
            3.0  * inf +
            2.0  * contam
        )
        severity = max(0.0, min(severity, 100.0))

        # Reasons (explainability chips)
        if bleed: reasons.append("active_bleeding")
        if vf.depth_mm >= 5.0: reasons.append(">5mm_depth")
        if vf.area_cm2 >= 5.0: reasons.append(">5cm2_area")
        if vf.location in {"face","hand","joint","eye","head"}: reasons.append(f"location:{vf.location}")
        if vf.deformity: reasons.append("deformity")
        if vf.infection_signs: reasons.append("infection_signs")
        if vf.contamination: reasons.append("contamination")
        if pain_norm >= 0.7: reasons.append("high_pain")

        # 3) Soft overrides / safety margins
        # If model is uncertain and score near a boundary, bump to higher band
        boundary_pad = 5.0
        if vf.model_confidence < 0.55 and (self.THRESH_URGENT - boundary_pad) <= severity < self.THRESH_URGENT:
            severity = self.THRESH_URGENT
            reasons.append("low_confidence_escalation")

        # If deformity is present -> at least Urgent
        if vf.deformity and severity < self.THRESH_URGENT:
            severity = self.THRESH_URGENT + 1
            reasons.append("suspected_fracture_escalation")

        # 4) Map to band
        if severity >= self.THRESH_IMMEDIATE:
            band = "immediate"
        elif severity >= self.THRESH_URGENT:
            band = "urgent"
        else:
            band = "standard"

        # Destination & duration
        dest, dur = self.DESTINATION_BY_TYPE.get(vf.wound_type, ("fast_track", 15))

        return TriageDecision(band, float(round(severity,2)), reasons, vf.model_confidence, dest, dur)


# -----------------------------
# Priority queue with aging
# -----------------------------

class TriageQueue:
    TARGET = {"immediate":10, "urgent":30, "standard":90}          # minutes
    WEIGHT = {"immediate":5.0, "urgent":2.5, "standard":1.0}
    AGING  = {"immediate":0.00, "urgent":0.01, "standard":0.02}    # bonus per minute

    def __init__(self):
        self._cases: Dict[str, dict] = {}   # case_id -> record
        self._created_at = time.time()

    @staticmethod
    def _now_min() -> float:
        return time.time()/60.0

    def add(self, case_id: str, decision: TriageDecision, created_min: Optional[float]=None):
        if created_min is None:
            created_min = self._now_min()
        self._cases[case_id] = {
            "id": case_id,
            "band": decision.band,
            "severity": decision.severity,
            "created_min": created_min,
            "destination": decision.suggested_destination,
            "est_duration_min": decision.est_duration_min,
            "reasons": decision.reasons,
            "confidence": decision.confidence,
        }

    def _priority(self, rec: dict, now_min: float) -> float:
        band = rec["band"]
        elapsed = max(0.0, now_min - rec["created_min"])
        base = self.WEIGHT[band] * (1.0 + (elapsed / self.TARGET[band]))
        aging = self.AGING[band] * elapsed
        return base + aging

    def snapshot(self) -> List[dict]:
        """Return a list of cases with live priorities, sorted descending."""
        now_min = self._now_min()
        rows = []
        for rec in self._cases.values():
            pr = self._priority(rec, now_min)
            rows.append({
                **rec,
                "elapsed_min": round(max(0.0, now_min - rec["created_min"]), 1),
                "priority": round(pr, 4),
                "target_min": self.TARGET[rec["band"]],
            })
        rows.sort(key=lambda r: (-r["priority"], r["created_min"]))
        return rows

    def pop_next(self) -> Optional[dict]:
        """Pop the highest priority case (if any)."""
        rows = self.snapshot()
        if not rows:
            return None
        top = rows[0]
        del self._cases[top["id"]]
        return top


# -----------------------------
# Convenience runner
# -----------------------------

def run_demo(cases: List[dict], seed_min_offset: float = 0.0) -> dict:
    """
    cases: list of dict with 'case_id' and 'vision' sub-dict. Example:
        {
          "case_id": "A001",
          "vision": {...},
          "answers": {...}   # optional
        }
    """
    vm = VisionModelStub()
    scorer = SeverityScorer()
    tq = TriageQueue()

    base_min = time.time()/60.0 - seed_min_offset  # allow backdating arrivals

    results = []
    for i, item in enumerate(cases):
        vf = vm.predict(item["vision"])
        answers = item.get("answers", {})
        ans_obj = IntakeAnswers(**answers) if answers else IntakeAnswers()
        decision = scorer.score(vf, ans_obj)
        created_min = base_min + i * 0.5  # stagger arrivals by 30s
        tq.add(item["case_id"], decision, created_min=created_min)
        results.append({
            "case_id": item["case_id"],
            "band": decision.band,
            "severity": decision.severity,
            "reasons": decision.reasons,
            "confidence": decision.confidence,
            "destination": decision.suggested_destination,
            "est_duration_min": decision.est_duration_min,
            "arrival_min": created_min,
        })

    queue_view = tq.snapshot()
    ordering = [row["id"] for row in queue_view]

    return {
        "decisions": results,
        "queue": queue_view,
        "next_up": ordering[0] if ordering else None
    }


# -----------------------------
# Minimal CLI
# -----------------------------

def _load_cases(path: str) -> List[dict]:
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, list), "JSON must be a list of cases"
            return data
    elif path.endswith(".jsonl"):
        out = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
        return out
    else:
        raise SystemExit("Provide .json or .jsonl input")

def main():
    import argparse, time
    ap = argparse.ArgumentParser(description="AI Triage demo (stub vision + rules)")
    ap.add_argument("--cases", required=False, help="Path to cases.json or .jsonl")
    ap.add_argument("--seed-offset-min", type=float, default=2.0, help="Backdate arrivals by N minutes")
    args = ap.parse_args()

    if args.cases:
        cases = _load_cases(args.cases)
    else:
        cases = [
            {"case_id":"A001","vision":{
                "wound_type":"laceration","area_cm2":8.0,"depth_mm":6.0,"active_bleeding":True,
                "location":"hand","contamination":True,"deformity":False,"infection_signs":False,
                "pain_0_10":7,"mechanism":"cut","model_confidence":0.86
            }},
            {"case_id":"A002","vision":{
                "wound_type":"burn","area_cm2":4.0,"depth_mm":1.0,"active_bleeding":False,
                "location":"face","contamination":False,"deformity":False,"infection_signs":False,
                "pain_0_10":5,"mechanism":"burn","model_confidence":0.90
            }},
            {"case_id":"A003","vision":{
                "wound_type":"bruise","area_cm2":1.0,"depth_mm":0.0,"active_bleeding":False,
                "location":"limb","contamination":False,"deformity":False,"infection_signs":False,
                "pain_0_10":3,"mechanism":"fall","model_confidence":0.92
            }},
            {"case_id":"A004","vision":{
                "wound_type":"swelling","area_cm2":2.0,"depth_mm":0.0,"active_bleeding":False,
                "location":"joint","contamination":False,"deformity":True,"infection_signs":False,
                "pain_0_10":6,"mechanism":"fall","model_confidence":0.80
            }},
            {"case_id":"A005","vision":{
                "wound_type":"laceration","area_cm2":5.5,"depth_mm":4.0,"active_bleeding":False,
                "location":"hand","contamination":False,"deformity":False,"infection_signs":True,
                "pain_0_10":8,"mechanism":"cut","model_confidence":0.50  # may trigger low_confidence_escalation
            }},
        ]

    out = run_demo(cases, seed_min_offset=args.seed_offset_min)
    # Pretty print
    print("=== TRIAGE DECISIONS ===")
    for d in out["decisions"]:
        print(json.dumps(d, indent=2))

    print("\n=== QUEUE (highest priority first) ===")
    for row in out["queue"]:
        print(json.dumps(row, indent=2))

    print("\nNEXT UP:", out["next_up"])

if __name__ == "__main__":
    main()
