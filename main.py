from agent.config import load_config
from agent.controller import AgentController
from agent.gui import AgentGUI


def main() -> None:
    config = load_config()
    controller = AgentController(config)
    gui = AgentGUI(controller)
    gui.run()


if __name__ == '__main__':
    main()
