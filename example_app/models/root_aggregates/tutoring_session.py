import uuid
from typing import List

from pydantic import BaseModel, Field

from dspygen.utils.yaml_tools import uuid_factory
from soc.models.domain_models.response import Response
from soc.models.root_aggregates.quest import Quest


class TutoringSession(BaseModel):
    """
    Represents a tutoring session between a student and a chatbot on a particular quest. Tutoring sessions provide
    interactive learning experiences and support to students as they progress through educational quests. Each
    tutoring session has a unique session identifier, student identifier, associated quest, and a list of responses
    exchanged between the student and the chatbot.
    """
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the tutoring session.")
    student_id: str = Field(default_factory=uuid_factory, description="The unique identifier for the student.")
    quest: Quest = Field(default_factory=Quest, description="The quest for the tutoring session.")
    responses: List[Response] = Field([], description="The responses provided during the tutoring session.")
