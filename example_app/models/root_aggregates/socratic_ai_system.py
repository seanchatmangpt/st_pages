from typing import Optional

import dspy
from pydantic import BaseModel

from dspygen.lm.groq_lm import Groq
from dspygen.modules.gen_pydantic_instance import instance
from dspygen.utils.dspy_tools import init_dspy
from dspygen.utils.yaml_tools import YAMLMixin
from soc.models.domain_models.feedback import Feedback
from soc.models.domain_models.user import User
from soc.models.root_aggregates.educational_content import EducationalContent
from soc.models.root_aggregates.quest import Quest
from soc.models.value_objects.user_interaction import UserInteraction
from soc.modules.provide_feedback_module import provide_feedback_call
from soc.modules.socratic_question_module import socratic_question_call


class SocraticAISystem(BaseModel, YAMLMixin):
    educational_content: EducationalContent
    user_interaction: UserInteraction

    def __init__(self, **data):
        super().__init__(**data)
        # Assuming DialogueManager is appropriately defined and can be instantiated.

    def add_quest(self, quest: Quest) -> None:
        """
        Adds a new quest to the educational content.
        """
        self.educational_content.quests.append(quest)

    def process_user_message(self, user: User, message_text: str) -> Optional[str]:
        """
        Processes a message from a user, invoking the dialogue manager for evaluation
        and potential Socratic questioning. Utilizes the instance pattern for dynamic content generation.
        """
        # Construct a prompt for generating or selecting a Socratic question based on the user's message.
        prompt = f"Given the student's message '{message_text}', generate a Socratic question or feedback."
        # The instance function is utilized here to dynamically generate educational content based on the prompt.
        content = socratic_question_call(prompt)
        return content

    def evaluate_user_response(self, user: User, response_text: str) -> None:
        """
        Evaluates a user's response to a question, using the instance pattern to generate feedback or further questions.
        """
        # Placeholder logic for extracting the response ID and finding the corresponding question and response.
        prompt = f"Evaluate the following response from the user {user.name}: '{response_text}'."
        evaluation_result = instance(Feedback, prompt)  # Using the instance function to dynamically generate evaluation.
        self.integrate_feedback(evaluation_result)

    def integrate_feedback(self, feedback: Feedback) -> None:
        """
        Integrates feedback into the system, updating educational content or dialogue strategies as necessary.
        """
        self.feedback_and_evaluation.feedback.append(feedback)
        # Further logic to integrate feedback into educational content or update dialogue strategies.

    def generate_insights(self, user: User) -> None:
        """
        Analyzes interactions and feedback to generate insights for improving educational content and strategies.
        Utilizes the instance pattern for AI-driven insights generation.
        """
        prompt = "Analyze the following interactions and feedback to generate insights for educational improvement."
        insights = provide_feedback_call(prompt)  # Assuming FeedbackAndEvaluation has a method or format to encapsulate insights.
        # Logic to apply insights for improving the system.


def main():
    """Main function"""
    init_dspy(lm_class=Groq, model="llama2-70b-4096")
    prompt = f" What do you think?. Given the student's message 'What factors have the biggest impact on apple yield?', generate a Socratic question or feedback."

    question = "Speaking of technological development, I think there are problems with President Yoon Seok-yeol of South Korea's R&D policy."
    context = "Understanding the motivation behind questions."
    follow_up = "How does this topic relate to your current learning objectives?"

    prompt = f"Given the student's message '{question}', generate a Socratic question or feedback if it relates to apple yield. If off topic or inappropriate, provide feedback."

    content = socratic_question_call(prompt)
    print(content)


if __name__ == '__main__':
    main()
