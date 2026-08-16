class ConversationMemory:
    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages
        self.active_product = None

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def set_product(self, product):
        if product:
            self.active_product = product

    def get_product(self):
        return self.active_product

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages = []
        self.active_product = None