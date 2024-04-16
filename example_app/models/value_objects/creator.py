from pydantic import BaseModel, Field


# Defining a creator or administrator of the educational content
class Creator(BaseModel):
    """
    Represents the creator or administrator of the educational content. Creators like Owen & Stephen are responsible
    for crafting the questions and designing interactive experiences for students. This class encapsulates their
    identity and role within the educational system, allowing recognition and proper programming for their contributions.
    """
    name: str = Field("", description="The name of the creator.")
    role: str = Field("creator", description="The role of the creator, defaults to 'Creator/Administrator'.")

