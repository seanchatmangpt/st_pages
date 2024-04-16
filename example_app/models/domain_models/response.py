from typing import Union, Optional, List, TYPE_CHECKING

from pydantic import BaseModel, Field

from dspygen.utils.yaml_tools import uuid_factory
from soc.models.domain_models.question import Question


class Response(BaseModel):
    """
    Represents a response provided by a student to a question. Responses are evaluated for correctness and may
    include feedback to guide the student's learning process. This class captures the question ID, student response,
    correctness, and optional feedback, facilitating interaction and assessment within tutoring sessions.
    """
    id: str = Field("", description="The unique identifier for the question.")
    student_response: str = Field("", description="The response provided by the student.")
    correct: bool = Field(False, description="Indicates whether the response is correct or not.")
    feedback: str = Field("", description="Feedback on the student's response.")
    weight: float = Field(1.0, description="The weight or importance of the response in the overall assessment."
                                           "As determined by the closeness to the edge with the highest weight.")

    @property
    def question(self) -> Question:
        pass
        # return QuestionRepository().get_question_by_id(self.question_id)

    @staticmethod
    def process_student_response(question: Question, text: str):
        """
        Process the student response and update the correctness and feedback fields.
        """
        from dspygen.utils.dspy_tools import init_dspy
        from dspygen.lm.groq_lm import Groq
        # init_dspy(Groq, model="mixtral-8x7b-32768")
        init_dspy()

        from soc.prototypes.json_module import json_call
        result = json_call(Response.model_json_schema(), f"Process the student response '{text}' for the question '{question.text}'. "
                                                         f"Must provide verbose socratic feedback that does not reference the question.")
        return Response.model_validate_json(result)


def main():
    """Main function"""
    # response = Response.process_student_response(QuestionRepository().get_question_by_id("1"), "Paris")
    # print(response)


if __name__ == '__main__':
    main()
