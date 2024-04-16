import uuid
from datetime import datetime
from typing import List, Tuple

from pydantic import BaseModel, Field

from dspygen.modules.gen_pydantic_instance import instance
from dspygen.utils.json_tools import extract
from dspygen.utils.pydantic_tools import InstanceMixin
from dspygen.utils.yaml_tools import uuid_factory, now_factory
from soc.models.domain_models.user import User
from soc.models.value_objects.entity import Entity
from soc.models.value_objects.intent import Intent


class Message(BaseModel):
    """
    Represents a message in a conversation with the chatbot. Messages capture user inputs, including text,
    intents, and entities, along with additional metadata such as timestamps and user information.
    The Chatbot is considered a user in the context of the conversation.
    """
    message_id: str = Field(default_factory=uuid_factory, description="The unique identifier for the message.")
    text: str = Field("", description="The text content of the message.")
    timestamp: str = Field(default_factory=now_factory, description="The timestamp of the message.")
    user: User | None = Field(None, description="The user who sent the message.")
    intents: List[Intent] = Field([], description="A list of identified intents in the message.")
    entities: List[Entity] = Field([], description="A list of extracted entities from the message.")

    @staticmethod
    def from_prompt(prompt: str):
        from dspygen.utils.dspy_tools import init_dspy
        from dspygen.lm.groq_lm import Groq
        # init_dspy(Groq, model="mixtral-8x7b-32768")
        init_dspy()

        from soc.prototypes.json_module import json_call
        result = json_call(Message.model_json_schema(), prompt)

        return Message.model_validate_json(result)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_dspy
    from dspygen.lm.groq_lm import Groq
    # init_dspy(Groq, model="mixtral-8x7b-32768")
    init_dspy()

    # extractor = IntentAndEntityExtractor()

    from soc.prototypes.json_module import json_call
    result = json_call(Message.model_json_schema(), "I am need to learn about the apple yield. 3 intents and 3 entities.")


    print(extract(result))

    return Message.model_validate_json(result)

    # message.process_and_update(extractor)
    # print(message.model_dump_json(indent=2))


if __name__ == '__main__':
    main()
