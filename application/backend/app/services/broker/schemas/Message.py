from jsonschema import validate

MessageTypes = []

MessageTypeToPayloadMapping = {
    "Get_Events_In_Need_Of_Invitations": None
}

Message = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "payload": {
            "anyOf": MessageTypes,
            "default": None
        },
    },
    "required": ["type"],
}
