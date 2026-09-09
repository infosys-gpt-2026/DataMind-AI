from langchain_core.messages import HumanMessage, AIMessage


class ConversationMemory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, message: str):
        self.messages.append(
            HumanMessage(content=message)
        )

    def add_ai_message(self, message: str):
        self.messages.append(
            AIMessage(content=message)
        )

    def get_history(self):
        return self.messages.copy()

    def get_recent_history(self, max_messages: int = 10):
        return self.messages[-max_messages:]

    def clear(self):
        self.messages.clear()

    def is_empty(self) -> bool:
        return len(self.messages) == 0


# Shared conversation memory
conversation_memory = ConversationMemory()


# --------------------------------------------------
# Module-level helper functions
# --------------------------------------------------

def add_user_message(message: str):
    conversation_memory.add_user_message(message)


def add_ai_message(message: str):
    conversation_memory.add_ai_message(message)


def get_chat_history():
    return conversation_memory.get_history()


def get_recent_chat_history(max_messages: int = 10):
    return conversation_memory.get_recent_history(max_messages)


def clear_chat_history():
    conversation_memory.clear()