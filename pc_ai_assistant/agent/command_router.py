from agent.admissions_riphah import register_then_login, login_only
from agent.apply_riphah import apply_riphah

def route_command(command: str, config: dict):
    c = command.lower()

    has_register = ("register" in c or "signup" in c or "sign up" in c)
    has_apply = ("apply" in c or "admission" in c or "application" in c)
    wants_submit = ("submit" in c or "final" in c or "apply online" in c or "auto apply" in c)

    # Combined flow: register + apply online
    if has_register and has_apply:
        register_then_login(config)
        apply_riphah(config, submit=wants_submit)
        return

    # Register intent (keywords: register, signup)
    if has_register:
        register_then_login(config)
        return

    # Login intent (keywords: login, log in)
    if "login" in c or "log in" in c or "sign in" in c:
        login_only(config)
        return
    
    # Apply intent (keywords: apply, admission application)
    if has_apply:
        apply_riphah(config, submit=wants_submit)  # submit when user explicitly requests online/auto submit
        return

    # If no match, show help
    print("⚠️  Command not recognized. Try:")
    print("- register")
    print("- login")
    print("- apply for admission")
