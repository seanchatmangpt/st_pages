from typing import List

from pydantic import BaseModel, Field

from soc.models.root_aggregates.quest import Quest
from soc.models.root_aggregates.tutoring_session import TutoringSession


class EducationalContent(BaseModel):
    """
    Represents educational content, which includes quests and tutoring sessions. Quests are collections of
    questions on particular topics, while tutoring sessions track interactions between students and chatbots
    during learning activities.
    """
    quests: List[Quest] = Field([], description="A list of quests, each containing a collection of questions.")
    tutoring_sessions: List[TutoringSession] = Field(
        [], description="A list of tutoring sessions, tracking interactions between students and chatbots."
    )

    class Config:
        arbitrary_types_allowed = True