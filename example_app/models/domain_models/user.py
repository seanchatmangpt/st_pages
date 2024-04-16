from typing import Optional

from pydantic import BaseModel, Field

from dspygen.utils.yaml_tools import uuid_factory


class User(BaseModel):
    """
    Represents a user within the context of a chatbot interaction. Users are individuals interacting with the
    educational system, such as students or administrators. Each user has a unique identifier and an optional
    name to personalize interactions. A Chatbot is considered a user in the context of the conversation.
    """
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the user.")
    name: Optional[str] = Field(None, description="The name of the user.")
