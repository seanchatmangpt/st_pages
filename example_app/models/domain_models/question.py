from typing import List, Union

from pydantic import BaseModel, Field

from dspygen.modules.gen_pydantic_instance import instance
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.yaml_tools import uuid_factory


class Question(BaseModel):
    """
    Model for individual questions in a quest. Questions serve as challenges to test students' knowledge and understanding.
    """
    id: str = Field(default_factory=uuid_factory, description="The unique identifier for the question.")
    text: str = Field("", description="The text of the question.")
    type: str = Field("Multiple Choice", description="Type of question, defaults to Multiple Choice.")
    options: List[str] = Field([], description="Possible answers for the question.")
    correct_option: int = Field(1, description="Index of the correct option from the options list.")


class QuestionConstructionProcess(BaseModel):
    """
    Represents the process of constructing a question. Each process includes the question being constructed, the
    reason for constructing the question, and a list of intermediate outputs such as evidence, reasoning, and
    assumptions involved in the construction process.
    """
    question: str = Field("", description="The question being constructed.")
    reason_for_question: str = Field("", description="The reason for constructing the question.")
    intermediate_outputs: List[str] = Field(
        [], description="A list of intermediate outputs involved in the construction process."
    )


class ConstructedQuestion(BaseModel):
    """
    Represents a constructed question, including the formulated question itself, the reason behind constructing
    this particular question, and the intermediate outputs involved in the question construction process.
    """
    formulated_question: str = Field("", description="The formulated question.")
    reason_for_this_question: str = Field("", description="The reason for constructing this question.")
    intermediate_outputs: QuestionConstructionProcess = Field(
        default_factory=QuestionConstructionProcess, description="The intermediate outputs involved in the question construction process."
    )


def main():
    """Main function"""
    init_dspy()
    print(instance(Question, "Generate a new question with text 'What is the capital of France?' "))

if __name__ == '__main__':
    main()
