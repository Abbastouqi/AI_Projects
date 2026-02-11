def redact(s: str) -> str:
    if not s:
        return ""
    if len(s) <= 4:
        return "*" * len(s)
    return s[:2] + "*" * (len(s) - 4) + s[-2:]
