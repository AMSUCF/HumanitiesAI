# -*- coding: utf-8 -*-
"""Slide routing for the 2025->2026 conversion.

Every slide gets a decision: keep (in its base-mapped week), move (to the
2026 week its reading now belongs to), or cut (content removed from the
course). Decisions are deterministic and recorded with reasons so the
draft report can show every call for instructor review.
"""
from __future__ import annotations

# 2025 deck number -> 2026 week number (old 10+11 merge into new 10)
BASE_MAP = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
            10: 10, 11: 10, 12: 11, 13: 12, 14: 13, 15: 14}

# Noble chapters moved to weeks 4-8 in 2026; two 2025 chapters were dropped.
# Routing is by SOURCE deck because each 2025 week assigned one known chapter.
NOBLE_MAP = {9: 4, 10: 5, 11: 6, 12: None, 13: None, 14: 7, 15: 8}
# Mitchell parts moved up two weeks (2025 weeks 3-7 -> 2026 weeks 1-5).
MITCHELL_MAP = {3: 1, 4: 2, 5: 3, 6: 4, 7: 5}

CUT_PATTERNS = [
    ("code to joy", "Code to Joy (Littman) removed from the course"),
    ("littman", "Code to Joy (Littman) removed from the course"),
    ("wizard of oz", "Oz fine-tuning corpus replaced by Ghosts Before the Shell"),
    ("oz completion", "Oz fine-tuning corpus replaced by Ghosts Before the Shell"),
    ("oz-fragments", "Oz fine-tuning corpus replaced by Ghosts Before the Shell"),
    ("oz books", "Oz fine-tuning corpus replaced by Ghosts Before the Shell"),
    ("eternauta", "El Eternauta reading removed"),
    ("free year of gemini", "expired Gemini student offer"),
    ("gemini for students", "expired Gemini student offer"),
    ("through october 6", "expired Gemini student offer"),
]

NOBLE_KEYS = ("safiya noble", "algorithms of oppression", "noble")
MITCHELL_KEYS = ("melanie mitchell", "guide for thinking humans", "mitchell")


def classify(deck: int, text: str) -> tuple[str, int | None, str]:
    """Return (action, target_week, reason).

    action: "keep" | "move" | "cut"
    target_week: 2026 week for keep/move, None for cut.
    """
    t = " ".join(text.lower().split())
    base = BASE_MAP[deck]

    for pat, reason in CUT_PATTERNS:
        if pat in t:
            return "cut", None, reason

    # Sora: retained only in the video week (base week 7) as the hype-cycle
    # case study; anywhere else it was a tool pointer and is gone.
    if "sora" in t:
        if base == 7:
            return "keep", 7, "Sora retained as Week 7 hype-cycle case study"
        return "cut", None, "Sora discontinued; tool references removed"

    if any(k in t for k in NOBLE_KEYS) and deck in NOBLE_MAP:
        target = NOBLE_MAP[deck]
        if target is None:
            return "cut", None, "Noble chapter dropped from the 2026 sequence"
        if target != base:
            return "move", target, f"Noble chapter now assigned in Week {target}"
        return "keep", base, "Noble chapter unchanged for this week"

    if any(k in t for k in MITCHELL_KEYS) and deck in MITCHELL_MAP:
        target = MITCHELL_MAP[deck]
        if target != base:
            return "move", target, f"Mitchell part now assigned in Week {target}"
        return "keep", base, "Mitchell part unchanged for this week"

    return "keep", base, "base mapping"
