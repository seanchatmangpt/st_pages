from pydantic import BaseModel, Field

from dspygen.modules.gen_pydantic_instance import instance
from dspygen.utils.dspy_tools import init_dspy


class SkillMetric(BaseModel):
    """
    Represents a skill metric measuring a student's progress or level achieved in a certain skill. Skill metrics
    provide insights into students' proficiency and development in specific areas of knowledge or competence.
    Each skill metric includes the name of the skill being measured and the level achieved by the student.
    """
    skill_name: str = Field("", description="The name of the skill being measured.")
    level_achieved: str = Field("", description="The level achieved in the skill.")


def main():
    """Main function"""
    init_dspy()
    print(instance(SkillMetric, "Generate a new skill metric for the apple logic question."))


if __name__ == '__main__':
    main()
