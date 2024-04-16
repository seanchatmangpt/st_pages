from pydantic import BaseModel, Field

from dspygen.modules.gen_pydantic_instance import instance
from soc.models.domain_models.feedback import Feedback
from soc.models.domain_models.question import ConstructedQuestion


class SystemPrompt(BaseModel):
    quest_id: str
    conversation_id: str

    def generate_prompt_based_on_objective(self) -> str:
        """
        Generate a detailed prompt that encapsulates the educational objective,
        key concepts (exam points), and structured inquiry to guide AI in formulating
        relevant questions or feedback.
        """
        from soc.repositories.repository import quest_repository
        quest = quest_repository.get(id=self.quest_id)
        prompt_details = "Key concepts include: " + ", ".join([point.reasoning for point in quest.exam_points]) + ".\n"
        prompt_details += "Generate a Socratic question that encourages exploration into these concepts."
        return prompt_details

    def create_socratic_question(self) -> ConstructedQuestion:
        """
        Uses the generated prompt to create a Socratic question through the dspy framework.
        """
        prompt = self.generate_prompt_based_on_objective()
        # Assuming ConstructedQuestion is the desired output model and it's properly defined
        constructed_question = instance(ConstructedQuestion, prompt)
        return constructed_question

    def evaluate_student_response(self, student_response: str) -> Feedback:
        """
        Generates feedback for a student's response to a question, aiming to provide constructive
        guidance or further inquiry.
        """
        # Implementation could similarly use the instance function with a model designed for feedback
        feedback_prompt = f"Given the response '{student_response}', generate constructive feedback."
        feedback = instance(Feedback, feedback_prompt)
        return feedback

    def update_system_with_feedback(self, feedback: Feedback) -> None:
        """
        Integrates the provided feedback into the system, potentially updating educational content
        or the approach to questioning.
        """
        # This method could adjust the SystemPrompt's attributes based on the feedback or record the feedback for future analysis
        self.feedback.append(feedback)

    # Additional methods can be defined here to further interact with the dspy framework
    # and leverage AI capabilities to enhance the educational experience


def main():
    # Initialize the repository and fetch the quest with ID "1"
    from soc.repositories.repository import quest_repository

    # Initialize SystemPrompt with the fetched quest
    system_prompt = SystemPrompt(quest_id="1", conversation_id="1")

    # Generate a prompt based on the quest objective and key concepts
    generated_prompt = system_prompt.generate_prompt_based_on_objective()
    print("Generated Prompt:")
    print(generated_prompt)
    #
    # # Create a Socratic question using the generated prompt
    # socratic_question = system_prompt.create_socratic_question()
    # print("\nSocratic Question:")
    # print(socratic_question)
    #
    # # Simulate evaluating a student response
    # student_response = "I think pests are the major issue affecting apple yield."
    # feedback = system_prompt.evaluate_student_response(student_response)
    # print("\nFeedback on Student Response:")
    # print(feedback)
    #
    # # Update system with feedback (demonstration purposes, no actual implementation here)
    # system_prompt.update_system_with_feedback("Great insight on pest impact!")


if __name__ == "__main__":
    main()
