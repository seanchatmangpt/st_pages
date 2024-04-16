from typing import List

from pydantic import BaseModel, Field

from dspygen.bpmn_models.other_entities import Conversation
from soc.models.domain_models.dialogue_state import DialogueState


class UserInteraction(BaseModel):
    """
    Represents user interaction, including conversations and dialog states. Conversations track the exchange
    of messages between users and chatbots, while dialog states capture the current state of the conversation
    and any relevant actions.
    """
    conversations: List[Conversation] = Field(
        [], description="A list of conversations, each containing a series of messages exchanged between users and chatbots."
    )
    dialogue_states: List[DialogueState] = Field(
        [], description="A list of dialog states, each representing the current state of a conversation and any relevant actions."
    )

    class Config:
        arbitrary_types_allowed = True