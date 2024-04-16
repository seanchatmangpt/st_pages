from typing import List, Optional
from models import Conversation, Message, User, DialogueState


class ConversationStateTracker:
    conversations: List[Conversation] = []

    def __init__(self, user: User):
        self.current_conversation: Optional[Conversation] = None
        self.user = user

    def start_new_conversation(self) -> None:
        """Initializes a new conversation for the user."""
        self.current_conversation = Conversation(user=self.user, messages=[])
        self.conversations.append(self.current_conversation)

    def add_message_to_conversation(self, message: Message) -> None:
        """Adds a new message to the current conversation."""
        if not self.current_conversation:
            raise ValueError("No active conversation.")
        self.current_conversation.messages.append(message)
        self.update_dialogue_state(message)

    def update_dialogue_state(self, message: Message) -> None:
        """Updates the dialog state based on the latest message."""
        # Example placeholder logic. Real implementation would analyze the message content.
        if message.user == self.user:
            new_state = DialogueState(conversation_id=self.current_conversation.id, current_state="UserMessage",
                                    next_actions=[])
        else:
            new_state = DialogueState(conversation_id=self.current_conversation.id, current_state="SystemResponse",
                                    next_actions=[])
        self.current_conversation.dialogue_states.append(new_state)

    def get_current_state(self) -> DialogueState:
        """Returns the current dialog state of the conversation."""
        if not self.current_conversation or not self.current_conversation.dialogue_states:
            raise ValueError("No active conversation or dialog states.")
        return self.current_conversation.dialogue_states[-1]

    def summarize_conversation(self) -> str:
        """Generates a summary of the current conversation, highlighting key points and topics discussed."""
        # Simplified for illustration. Real implementation could use NLP to generate summaries.
        summary = "Conversation Summary:\n"
        for msg in self.current_conversation.messages:
            summary += f"- {msg.text}\n"
        return summary

