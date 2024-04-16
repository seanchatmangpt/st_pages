from typing import List

from pydantic import BaseModel, Field


class ExamPoint(BaseModel):
    """
    Represents an exam point, which is a component of an examination or assessment. An exam point includes
    evidence, reasoning, and possibly assumptions, providing a structured approach to presenting information
    or arguments in an examination context.
    """
    ep_number: int = Field(1, description="The number or identifier of the exam point.")
    evidence: List[str] = Field([], description="A list of evidence supporting the exam point.")
    reasoning: str = Field("", description="The reasoning behind the exam point.")
    assumptions: List[str] = Field([], description="A list of assumptions made in relation to the exam point.")
    weight: float = Field(1.0, description="The weight or importance of the exam point in the overall assessment.")

