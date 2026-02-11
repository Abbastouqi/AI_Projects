import os
from dotenv import load_dotenv
import yaml
from agent.voice import listen_for_command
from agent.command_router import route_command

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()
    config = load_config()

    print("PC AI Assistant started.")
    print("Type a command, or press Enter to use voice (if enabled).")
    print("Examples:")
    print("- open admissions portal")
    print("- login to riphah admissions")
    print("- apply for admission")
    print("- quit")

    while True:
        text = input("\nCommand (or Enter for voice): ").strip()

        if not text:
            if config.get("voice", {}).get("enabled", False):
                text = listen_for_command(language=config["voice"]["language"])
            else:
                print("Voice disabled in config.yaml")
                continue

        if not text:
            continue

        if text.lower() in ("quit", "exit", "stop"):
            print("Goodbye.")
            break

        route_command(text, config)

if __name__ == "__main__":
    main()
