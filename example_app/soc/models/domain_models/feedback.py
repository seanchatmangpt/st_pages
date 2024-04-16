from pydantic import BaseModel, Field


class Feedback(BaseModel):
    """
    Represents feedback provided in response to a question or interaction. Feedback includes a feedback ID for
    identification, the content of the feedback message, and an optional flag indicating whether action is required
    based on the feedback.
    """
    id: str = Field(1, description="The unique identifier for the feedback.")
    content: str = Field("", description="The content of the feedback message.")
    action_required: bool = Field(False, description="Indicates whether action is required based on the feedback.")

