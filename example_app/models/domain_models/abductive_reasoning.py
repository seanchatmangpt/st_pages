from typing import List

from pydantic import BaseModel, Field

class AbductiveReasoning(BaseModel):
    """
    Represents an abductive reasoning process, which is a form of logical inference that starts with an observation
    or set of observations and seeks the simplest and most likely explanation. This model is used to formalize the
    process of generating hypotheses based on incomplete information, prioritizing explanations that may not be
    conclusively proven but are plausible given the available data.
    """
    observation: str = Field(..., description="The initial observation or set of observations that necessitate an explanation.")
    hypotheses: List[str] = Field([], description="A list of possible explanations generated through abductive reasoning.")
    preferred_hypothesis: str = Field("", description="The hypothesis considered most plausible or likely, given the current evidence and context.")
    evidence_supporting_preferred: List[str] = Field([], description="Evidence supporting the preferred hypothesis.")
    reasoning_for_preference: str = Field("", description="The reasoning behind the preference for the selected hypothesis over others.")
    context: List[str] = Field([], description="Additional context or information that informs the abductive reasoning process.")
    confidence_level: float = Field(0.0, description="A numeric representation of the confidence in the preferred hypothesis, ranging from 0 to 1.")

    class Config:
        schema_extra = {
            "example": {
                "observation": "The garden's gate is open, and the dog is missing.",
                "hypotheses": [
                    "The dog learned to open the gate.",
                    "A family member forgot to close the gate.",
                    "Someone entered the garden and left the gate open."
                ],
                "preferred_hypothesis": "A family member forgot to close the gate.",
                "evidence_supporting_preferred": [
                    "The dog has never shown the ability to open the gate before.",
                    "There are no signs of forced entry or unfamiliar footprints."
                ],
                "reasoning_for_preference": "It's the simplest explanation that fits the facts without assuming new behavior from the dog or action from an unknown third party.",
                "context": [
                    "The dog does not know how to open gates.",
                    "There has been no recent suspicious activity in the neighborhood."
                ],
                "confidence_level": 0.75
            }
        }
