from typing import List, Optional

from pydantic import BaseModel, Field

from dspygen.utils.yaml_tools import uuid_factory
from soc.models.value_objects.skill_metric import SkillMetric


class StudentProgress(BaseModel):
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the student.")
    completed_quests: List[int] = Field(default=[], description="A list of completed quest IDs.")
    skill_metrics: List[SkillMetric] = Field(default=[], description="A list of skill metrics for the student.")

    def add_completed_quest(self, quest_id: int) -> None:
        """
        Marks a quest as completed for the student.
        """
        if quest_id not in self.completed_quests:
            self.completed_quests.append(quest_id)

    def update_skill_metric(self, skill_name: str, level_achieved: float) -> None:
        """
        Updates or adds a skill metric for the student.
        """
        for skill_metric in self.skill_metrics:
            if skill_metric.skill_name == skill_name:
                skill_metric.level_achieved = max(skill_metric.level_achieved, level_achieved)
                return
        # If the skill does not exist, add a new entry
        self.skill_metrics.append(SkillMetric(skill_name=skill_name, level_achieved=level_achieved))

    def get_skill_level(self, skill_name: str) -> Optional[float]:
        """
        Retrieves the current level achieved for a given skill.
        """
        for skill_metric in self.skill_metrics:
            if skill_metric.skill_name == skill_name:
                return skill_metric.level_achieved
        return None

    def get_completion_rate(self, total_quests: int) -> float:
        """
        Calculates the completion rate of the student based on the total number of quests.
        """
        if total_quests == 0:
            return 0.0  # Avoid division by zero
        return len(self.completed_quests) / total_quests

    def has_completed_quest(self, quest_id: int) -> bool:
        """
        Checks if a student has completed a specific quest.
        """
        return quest_id in self.completed_quests