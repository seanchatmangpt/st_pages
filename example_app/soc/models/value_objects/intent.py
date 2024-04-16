from pydantic import BaseModel, Field


class Intent(BaseModel):
    """
    Represents an intent identified in a user's message. Intents capture the intended action or purpose behind
    a user's input, facilitating effective understanding and response by the chatbot. Each intent has a name
    indicating the action and a confidence score representing the certainty of the intent classification.
    """
    name: str = Field("", description="The name of the identified intent.")
    confidence: float = Field(0, description="The confidence score for the identified intent.")

