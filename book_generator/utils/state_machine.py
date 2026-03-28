"""
Lightweight state machine helpers for workflow gating.
Used by tasks and API routes to validate transitions.
"""

VALID_TRANSITIONS: dict[str, list[str]] = {
    "pending":              ["outline_generating", "paused", "error"],
    "outline_generating":   ["outline_ready", "paused", "error"],
    "outline_ready":        ["chapters_generating", "paused"],
    "chapters_generating":  ["chapters_ready", "paused", "error"],
    "chapters_ready":       ["compiling", "error"],
    "compiling":            ["completed", "error"],
    "paused":               ["outline_generating", "outline_ready", "chapters_generating", "compiling"],
    "error":                ["pending"],
    "completed":            [],
}


def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])


def assert_transition(current: str, target: str) -> None:
    if not can_transition(current, target):
        raise ValueError(f"Invalid transition: {current!r} → {target!r}")
