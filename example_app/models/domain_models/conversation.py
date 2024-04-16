from typing import List
from pydantic import BaseModel, Field
from dspygen.utils.yaml_tools import YAMLMixin, uuid_factory
from soc.models.domain_models.user import User
from soc.models.value_objects.message import Message
from soc.modules.assess_learning_progress_module import assess_learning_progress_call


class Conversation(BaseModel, YAMLMixin):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the conversation.")
    messages: List[Message] = Field([], description="A list of messages in the conversation.")

    def history(self) -> str:
        """Generates a textual history of the conversation."""
        return '\n'.join([f"{msg.user.name}: {msg.text}" for msg in self.messages])

    def save(self) -> None:
        """Saves or updates the current conversation instance."""
        from soc.repositories.repository import conversation_repository

        conversation_repository.save(self)

    def add_message(self, message: Message) -> None:
        """Adds a new message to the conversation."""
        self.messages.append(message)

    @classmethod
    def get_by_id(cls, conversation_id: str) -> "Conversation":
        """Retrieves a conversation by its unique identifier."""
        from soc.repositories.repository import conversation_repository

        return conversation_repository.get(id=conversation_id)


def main():
    """Main function"""
    # Creating a new conversation
    conversation = Conversation(conversation_id="1")
    message = Message(user=User(name="John Doe"), text="Hello, world!")
    conversation.messages.append(message)

    # Saving the conversation
    conversation.save()

    # Retrieving the conversation by ID
    retrieved_conversation = Conversation.get_by_id(conversation.id)
    print(retrieved_conversation.history())



if __name__ == '__main__':
    main()
