class MessageHandlers:
    handlers = {}

    @classmethod
    def handle(cls, type_: str):
        def decorator(func):
            cls.handlers[type_] = func
            return func
        return decorator

    @classmethod
    def process_message(cls, message: dict, correlation_id: str, reply_to: str):
        type_ = message['type']
        payload = message.get('payload')
        cls.handlers[type_](payload, correlation_id, reply_to)
