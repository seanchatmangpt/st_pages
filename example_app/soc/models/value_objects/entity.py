from typing import Any, Optional

from pydantic import BaseModel, Field


class Entity(BaseModel):
    """
    Represents an entity extracted from a user's message. Entities capture specific pieces of information
    mentioned in the user input, such as dates, locations, or other relevant data. Each entity includes
    the name of the extracted entity, its value, start and end positions in the message, and an optional
    confidence score.
    """
    entity: str = Field("", description="The name of the extracted entity.")
    value: Any = Field("", description="The value of the extracted entity.")
    start: int = Field(1, description="The starting position of the entity in the message.")
    end: int = Field(1, description="The ending position of the entity in the message.")
    confidence: Optional[float] = Field(None, description="The confidence score for the extracted entity.")

