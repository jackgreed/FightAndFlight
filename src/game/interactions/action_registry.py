class ActionDefinition:
    def __init__(self, action_id: str, label: str, command_type: str):
        self.action_id = action_id
        self.label = label
        self.command_type = command_type


ACTION_REGISTRY = {
    "chop": ActionDefinition("chop", "Chop", "ChopCommand"),
    "inspect": ActionDefinition("inspect", "Inspect", "InspectCommand"),
}