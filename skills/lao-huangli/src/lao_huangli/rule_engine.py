from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional

from .calendar_core import DIZHI


ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / "rules"


def load_ruleset_items(profile_id: str, filename: str) -> List[Dict[str, object]]:
    path = RULES_DIR / profile_id / f"{filename}.json"
    if not path.exists():
        return []
    return json.loads(path.read_text())


def get_ruleset_source_metadata(ruleset_id: Optional[str]) -> Dict[str, object]:
    if not ruleset_id:
        return {"ruleSourceLevel": "none", "sourceRefs": []}

    ruleset_dir = RULES_DIR / ruleset_id
    if not ruleset_dir.exists():
        return {"ruleSourceLevel": "none", "sourceRefs": []}

    source_levels = OrderedDict()
    source_refs = OrderedDict()
    for path in sorted(ruleset_dir.glob("*.json")):
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            continue
        for item in data:
            level = item.get("sourceLevel")
            if level:
                source_levels[level] = True
            for ref in item.get("sourceRef", []):
                key = (ref.get("work"), ref.get("location"), ref.get("url"))
                if key not in source_refs:
                    source_refs[key] = ref

    level_text = ",".join(source_levels.keys()) if source_levels else "none"
    return {"ruleSourceLevel": level_text, "sourceRefs": list(source_refs.values())}


def compute_jianchu(profile_id: str, month_branch: str, day_branch: str) -> str:
    rules = load_ruleset_items(profile_id, "jianchu")
    if not rules:
        return "待规则库补齐"

    cycle = rules[0]["cycle"]
    month_index = DIZHI.index(month_branch)
    day_index = DIZHI.index(day_branch)
    return cycle[(day_index - month_index) % 12]


def compute_yellow_black_dao(profile_id: str, month_branch: str, day_branch: str) -> str:
    rules = load_ruleset_items(profile_id, "yellow-black-dao")
    if not rules:
        return "待规则库补齐"

    rule = rules[0]
    start_branch = rule["monthStarts"][month_branch]
    start_index = DIZHI.index(start_branch)
    day_index = DIZHI.index(day_branch)
    return rule["order"][(day_index - start_index) % 12]


def evaluate_rules(profile_id: str, rule_context: Dict[str, str]) -> Dict[str, List[str]]:
    decision = {"yi": [], "ji": [], "warnings": [], "explanations": []}
    for rule in load_ruleset_items(profile_id, "yi-ji-rules"):
        if rule_context.get(rule["field"]) not in rule["values"]:
            continue

        effect = rule["effect"]
        decision[effect].extend(rule["items"])
        decision["explanations"].append(rule["reason"])

    return decision


def get_active_ruleset(profile_id: str, overlay_ruleset: Optional[str]) -> Optional[str]:
    if profile_id == "bazi-v1":
        return overlay_ruleset
    return profile_id


def get_capabilities(profile_id: str, ruleset_id: Optional[str], is_hybrid: bool) -> Dict[str, bool]:
    has_rule_layer = ruleset_id is not None
    return {
        "calendarCore": True,
        "ganzhi": True,
        "solarTerms": True,
        "jianchu": has_rule_layer,
        "yellowBlackDao": has_rule_layer,
        "dutyGod": False,
        "yiJi": has_rule_layer,
        "sourceTrace": has_rule_layer,
        "isHybrid": is_hybrid,
    }


def evaluate_rule_layer(
    profile_id: str,
    overlay_ruleset: Optional[str],
    calendar_context: Dict[str, object],
) -> Dict[str, object]:
    ganzhi = calendar_context["ganzhi"]
    month_branch = ganzhi["month"][1]
    day_branch = ganzhi["day"][1]
    is_hybrid = profile_id == "bazi-v1" and overlay_ruleset is not None
    ruleset_id = get_active_ruleset(profile_id, overlay_ruleset)

    if ruleset_id:
        daily = {
            "jianchu": compute_jianchu(ruleset_id, month_branch, day_branch),
            "yellowBlackDao": compute_yellow_black_dao(ruleset_id, month_branch, day_branch),
            "chongsha": "待规则库补齐",
            "taishen": "待规则库补齐",
            "pengzu": "待规则库补齐",
        }
        decision = evaluate_rules(ruleset_id, daily)
    else:
        daily = {}
        decision = {"yi": [], "ji": [], "warnings": [], "explanations": []}

    source_metadata = get_ruleset_source_metadata(ruleset_id)
    provenance = {
        "calendarCore": "algorithmic",
        "ruleLayer": ruleset_id,
        "ruleSourceLevel": source_metadata["ruleSourceLevel"],
        "sourceRefs": source_metadata["sourceRefs"],
        "isHybrid": is_hybrid,
        "overlayRuleset": overlay_ruleset,
    }
    return {
        "daily": daily,
        "decision": decision,
        "capabilities": get_capabilities(profile_id, ruleset_id, is_hybrid),
        "provenance": provenance,
        "ruleLayer": ruleset_id,
        "isHybrid": is_hybrid,
    }
