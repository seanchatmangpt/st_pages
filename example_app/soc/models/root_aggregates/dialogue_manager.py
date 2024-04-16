# dialogue_manager.py
from typing import List, Optional
from soc.models.domain_models.conversation import Conversation
from soc.models.domain_models.dialogue_state import DialogueState

from soc.models.domain_models.question import Question
from soc.models.domain_models.response import Response
from soc.models.root_aggregates.quest import Quest
from soc.models.value_objects.message import Message
from soc.modules.provide_feedback_module import provide_feedback_call
from soc.modules.socratic_question_module import socratic_question_call
from soc.modules.evaluate_user_response_module import evaluate_user_response_call
from soc.modules.process_user_query_module import process_user_query_call
from soc.models.domain_models.user import User


class DialogueManager:
    """
    Manages dialogues within the Socratic AI Tutoring System, handling conversation flow,
    question answering, and interactive discussions, utilizing AI-driven methods for dynamic interaction.
    """

    def __init__(self, quest: Quest):
        self.quest = quest
        self.current_conversation: Optional[Conversation] = None
        self.dialogue_state: Optional[DialogueState] = None

    def start_conversation(self, conversation_id: str, user_id: str) -> None:
        """
        Initializes a new conversation, setting it as the current conversation.
        """
        self.current_conversation = Conversation(conversation_id=conversation_id, user_id=user_id)
        self.dialogue_state = DialogueState(conversation_id=conversation_id)

    def start_quest(self) -> None:
        """
        Starts the quest by transitioning to the teaching state and initiating the interactive discussion.
        """
        if self.dialogue_state.current_question_index == 0:
            self.dialogue_state.start_teaching(self.quest.title)
            self.discuss()
        else:
            print("Quest has already started.")

    def next_question(self) -> Optional[Question]:
        """
        Moves to the next question in the quest.
        Returns the next question if available, otherwise returns None.
        """
        if self.dialogue_state.current_question_index < len(self.quest.questions):
            question = self.quest.questions[self.dialogue_state.current_question_index]
            if self.dialogue_state.state == 'teaching':
                self.dialogue_state.start_quizzing(question.text)
            elif self.dialogue_state.state == 'evaluating':
                self.dialogue_state.start_quizzing(question.text)
            else:
                print("Invalid state transition. Please answer the current question first.")
                return None
            return question
        else:
            print("No more questions in the quest.")
            return None

    def answer_question(self, answer_index: int) -> None:
        """
        Processes the user's answer to the current question.
        """
        if self.dialogue_state.current_question_index < len(self.quest.questions):
            question = self.quest.questions[self.dialogue_state.current_question_index]
            if self.dialogue_state.state != 'quizzing':
                print("Invalid state. Please use next_question() to move to the next question.")
                return
            if 0 <= answer_index < len(question.options):
                correct_answer_index = question.correct_option
                self.dialogue_state.evaluate(question.options[answer_index], question.options[correct_answer_index])
                self.dialogue_state.current_question_index += 1
            else:
                print("Invalid answer option.")
        else:
            print("No question available to answer.")

    def conclude_conversation(self) -> None:
        """
        Concludes the current conversation and resets the dialogue state.
        """
        self.dialogue_state.conclude()
        print("Conversation concluded.")

    def discuss(self) -> None:
        """
        Engages in an interactive discussion with the user, providing Socratic questions and evaluating responses.
        """
        if self.dialogue_state.state == 'teaching':
            question = socratic_question_call(
                context=f"Quest: {self.quest}\n\nConversation History: {self.current_conversation.history()}")
            print(question)

            message = Message(text=question, user=User(name="Socrates"))
            self._update_conversation(message)

            evaluation = evaluate_user_response_call(
                f"Quest: {self.quest}\n\nConversation History: {self.current_conversation.history()}")

            message = Message(text=evaluation, user=User(name="Socrates"))
            self._update_conversation(message)

            response = process_user_query_call(
                f"Quest: {self.quest}\n\nConversation History: {self.current_conversation.history()}")
            print(response)
            message = Message(text=response, user=User(name="Socrates"))
            self._update_conversation(message)

    def _update_conversation(self, message: Message) -> None:
        """
        Appends a new message to the current conversation, maintaining the flow of dialogue.
        """
        if self.current_conversation:
            self.current_conversation.messages.append(message)

    def get_current_question(self) -> Optional[Question]:
        """
        Returns the current question if available, otherwise returns None.
        """
        if self.dialogue_state.current_question_index < len(self.quest.questions):
            return self.quest.questions[self.dialogue_state.current_question_index]
        else:
            return None

    def get_dialogue_state(self) -> Optional[DialogueState]:
        """
        Returns the current dialogue state.
        """
        return self.dialogue_state


def main():
    """Main function"""
    # Load the apple cultivation quest from the repository
    from soc.repositories.repository import quest_repository
    apple_cultivation_quest = quest_repository.get(id="1")

    # Create an instance of DialogueManager with the apple cultivation quest
    dm = DialogueManager(apple_cultivation_quest)

    # Start a new conversation
    dm.start_conversation(conversation_id="1", user_id="user1")

    # Display welcome message
    print(f"Welcome to the Socratic AI Tutoring System!")
    print(f"Quest: {apple_cultivation_quest.title}")

    # Start the quest
    dm.start_quest()

    # Go through each question in the quest
    while True:
        # Get the current question
        question = dm.get_current_question()

        if question is None:
            # No more questions, conclude the conversation
            dm.conclude_conversation()
            break

        # Display the question and options
        print(f"\nQuestion: {question.text}")
        for idx, option in enumerate(question.options):
            print(f"{idx + 1}. {option}")

        # Get the user's answer (in this example, we assume the user always selects the first option)
        user_answer_index = 0

        # Process the user's answer
        dm.answer_question(user_answer_index)

        # Display the answer result
        print(f"Current state: {dm.dialogue_state.state}")
        print(f"Previous action: {dm.dialogue_state.previous_action}")
        print(f"Next actions: {dm.dialogue_state.next_actions}")

        # Move to the next question
        dm.next_question()

    # Display quest completion message
    print("Congratulations! You have completed the apple cultivation quest.")


if __name__ == '__main__':
    main()
