import getpass
import json
import os

# Optional injected credentials for non-interactive usage (e.g. web frontend)
INJECTED_CREDENTIALS = {}
SAVED_CREDENTIALS_PATH = os.path.join("data", "credentials.json")

def set_injected_credentials(creds: dict):
    """Set credentials to be returned by prompt functions (used by web frontend)."""
    global INJECTED_CREDENTIALS
    INJECTED_CREDENTIALS = creds or {}

def clear_injected_credentials():
    global INJECTED_CREDENTIALS
    INJECTED_CREDENTIALS = {}

def load_saved_credentials() -> dict:
    """Load saved credentials from disk (if present)."""
    try:
        if not os.path.exists(SAVED_CREDENTIALS_PATH):
            return {}
        with open(SAVED_CREDENTIALS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        if not isinstance(data, dict):
            return {}
        return data
    except Exception:
        return {}

def save_credentials(creds: dict) -> None:
    """Persist credentials locally for auto-login (opt-in)."""
    try:
        os.makedirs(os.path.dirname(SAVED_CREDENTIALS_PATH), exist_ok=True)
        payload = {
            "email": creds.get("email", ""),
            "password": creds.get("password", ""),
        }
        with open(SAVED_CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass

def clear_saved_credentials() -> None:
    """Delete saved credentials."""
    try:
        if os.path.exists(SAVED_CREDENTIALS_PATH):
            os.remove(SAVED_CREDENTIALS_PATH)
    except Exception:
        pass

def prompt_registration():
    # If credentials were injected by a caller, use them (no interactive prompt)
    if INJECTED_CREDENTIALS:
        return {
            "name": INJECTED_CREDENTIALS.get("name", ""),
            "mobile": INJECTED_CREDENTIALS.get("mobile", ""),
            "email": INJECTED_CREDENTIALS.get("email", ""),
            "password": INJECTED_CREDENTIALS.get("password", ""),
        }

    print("\n--- Registration Details ---")
    name = input("Full name: ").strip()
    mobile = input("Mobile (03xxxxxxxxx): ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password (hidden): ").strip()
    return {"name": name, "mobile": mobile, "email": email, "password": password}

def prompt_login(default_email: str = ""):
    # If credentials injected, return them without prompting or printing
    if INJECTED_CREDENTIALS and (INJECTED_CREDENTIALS.get("email") or INJECTED_CREDENTIALS.get("password")):
        return {
            "email": INJECTED_CREDENTIALS.get("email") or default_email,
            "password": INJECTED_CREDENTIALS.get("password", ""),
        }

    print("\n--- Login Details ---")
    email = input(f"Email [{default_email}]: ").strip() or default_email
    password = getpass.getpass("Password (hidden): ").strip()
    return {"email": email, "password": password}
