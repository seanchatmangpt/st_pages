from typing import Optional

from pydantic import BaseModel, Field


class Action(BaseModel):
    """
    Represents an action taken by the chatbot in response to a user message. Actions define the behavior or
    response of the chatbot, which can include custom actions, utterances, or other types of interactions.
    Each action has a name indicating the type of action, an action type specifying the nature of the action,
    and an optional response providing additional information or content for the action.
    """
    action_name: str = Field("", description="The name of the action.")
    action_type: str = Field("", description="The type of the action.")
    response: Optional[str] = Field(None, description="The response of the action.")

