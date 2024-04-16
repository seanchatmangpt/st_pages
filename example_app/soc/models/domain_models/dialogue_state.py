from typing import List, Optional
from pydantic import BaseModel, Field

from soc.models.domain_models.conversation import Conversation
from soc.models.domain_models.user import User
from soc.models.value_objects.action import Action
from transitions import Machine

from soc.models.value_objects.message import Message


class DialogueState(Machine):
    states = ['initial', 'teaching', 'quizzing', 'evaluating', 'concluding']

    transitions = [
        {'trigger': 'start_teaching', 'source': '*', 'dest': 'teaching'},
        {'trigger': 'start_quizzing', 'source': 'teaching', 'dest': 'quizzing'},
        {'trigger': 'evaluate', 'source': 'quizzing', 'dest': 'evaluating'},
        {'trigger': 'conclude', 'source': '*', 'dest': 'concluding'}
    ]

    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.current_state = "initial"
        self.previous_action: Optional[Action] = None
        self.next_actions: List[Action] = []
        self.current_question_index = 0
        self.conversation = Conversation()


        # Initialize the state machine
        Machine.__init__(self, model=self, states=DialogueState.states, transitions=DialogueState.transitions,
                         initial='initial')

    # Transition methods
    def on_enter_teaching(self, content):
        teaching_action = Action(action_name="Teach", action_type="teach", response=content)
        self.next_actions = [teaching_action]

    def on_enter_quizzing(self, question):
        quiz_action = Action(action_name="Quiz", action_type="quiz", response=question)
        self.next_actions = [quiz_action]

    def on_enter_evaluating(self, user_answer, correct_answer):
        is_correct = user_answer == correct_answer
        feedback_action = Action(action_name="Feedback", action_type="feedback",
                                 response="Correct!" if is_correct else "Try again!")
        self.previous_action = self.next_actions[-1]
        self.next_actions = [feedback_action]

    def add_to_conversation(self, message: Message):
        self.conversation.add_message(message)
        self.conversation.save()

    # Additional methods to handle other logic...

from soc.models.value_objects.action import Action

def main():
    # Create an instance of DialogueState
    dialogue_state = DialogueState(conversation_id="1")

    # Load the quest from the repository
    from soc.repositories.repository import quest_repository
    quest = quest_repository.get(id="1")

    print(f"Welcome to the Socratic AI Tutoring System!")
    print(f"Quest: {quest.title}")
    print("Available commands:")
    print("/start - Start the quest")
    print("/next - Move to the next question")
    print("/answer <option> - Answer the current question")
    print("/exit - Exit the program")

    current_question_index = 0

    while True:
        command = input("Enter a command: ")
        print(f"Current state: {dialogue_state.state}")
        print(f"Current question index: {current_question_index}")
        question = socratic_question_call()

        if command == "/start":
            if current_question_index == 0:
                dialogue_state.start_teaching(quest.title)
                discuss(dialogue_state, quest)

                print(f"Current state: {dialogue_state.state}")
                print(f"Next actions: {dialogue_state.next_actions}")
            else:
                print("Quest has already started.")
        elif command == "/next":
            if current_question_index < len(quest.questions):
                question = quest.questions[current_question_index]
                if dialogue_state.state == 'teaching':
                    dialogue_state.start_quizzing(question.text)
                    discuss(dialogue_state, quest)
                elif dialogue_state.state == 'evaluating':
                    dialogue_state.start_quizzing(question.text)
                    discuss(dialogue_state, quest)
                else:
                    print("Invalid state transition. Please answer the current question first.")
                    continue
                print(f"Current state: {dialogue_state.state}")
                print(f"Next actions: {dialogue_state.next_actions}")
                print(f"\nQuestion: {question.text}")
                for idx, option in enumerate(question.options):
                    print(f"{idx + 1}. {option}")
            else:
                print("No more questions in the quest.")
        elif command.startswith("/answer"):
            if current_question_index < len(quest.questions):
                question = quest.questions[current_question_index]
                print(f"Current question: {question.options}")
                if dialogue_state.state != 'quizzing':
                    print("Invalid state. Please use /next to move to the next question.")
                    continue
                try:
                    user_answer_index = int(command.split(" ")[1]) - 1
                    if 0 <= user_answer_index < len(question.options):
                        correct_answer_index = question.correct_option
                        dialogue_state.evaluate(question.options[user_answer_index], question.options[correct_answer_index])
                        print(f"Current state: {dialogue_state.state}")
                        print(f"Previous action: {dialogue_state.previous_action}")
                        print(f"Next actions: {dialogue_state.next_actions}")
                        current_question_index += 1
                    else:
                        print("Invalid answer option.")
                except (IndexError, ValueError):
                    print("Invalid answer command.")
            else:
                print("No question available to answer.")
        elif command == "/exit":
            dialogue_state.conclude()
            print(f"Current state: {dialogue_state.state}")
            print("Exiting the program...")
            break


def discuss(dialogue_state, quest):
    if dialogue_state.state == 'teaching':
        while True:
            from dspygen.utils.dspy_tools import init_dspy
            from dspygen.lm.groq_lm import Groq
            init_dspy(Groq, model="mixtral-8x7b-32768")
            from soc.modules.socratic_question_module import socratic_question_call

            question = socratic_question_call(
                context=f"Quest: {quest}\n\nConversation History: {dialogue_state.conversation.history()}")
            print(question)

            user_message = input("Discuss with Socrates and press Enter to continue... q to quit: ")

            if user_message == 'q':
                return

            message = Message(text=user_message, user=User(name="User"))
            dialogue_state.add_to_conversation(message)

            from soc.modules.evaluate_user_response_module import evaluate_user_response_call
            evaluation = evaluate_user_response_call(
                f"Quest: {quest}\n\nConversation History: {dialogue_state.conversation.history()}")
            # print(evaluation)

            message = Message(text=evaluation, user=User(name="Socrates"))
            dialogue_state.add_to_conversation(message)

            from soc.modules.process_user_query_module import process_user_query_call
            response = process_user_query_call(
                f"Quest: {quest}\n\nConversation History: {dialogue_state.conversation.history()}")
            print(response)
            message = Message(text=response, user=User(name="Socrates"))
            dialogue_state.add_to_conversation(message)

            # print(f"Conversation saved.\n\n{dialogue_state.conversation.history()}")


def main2():
    # Create an instance of DialogueState
    dialogue_state = DialogueState(conversation_id="1")

    # Test initial state
    print(f"Current state: {dialogue_state.state}")

    # Transition to teaching state
    content = "Welcome to the Socratic AI Tutoring System!"
    dialogue_state.start_teaching(content)
    print(f"Current state: {dialogue_state.state}")
    print(f"Next actions: {dialogue_state.next_actions}")

    # Transition to quizzing state
    question = "What is the capital of France?"
    dialogue_state.start_quizzing(question)
    print(f"Current state: {dialogue_state.state}")
    print(f"Next actions: {dialogue_state.next_actions}")

    # Transition to evaluating state
    user_answer = "Paris"
    correct_answer = "Paris"
    dialogue_state.evaluate(user_answer, correct_answer)
    print(f"Current state: {dialogue_state.state}")
    print(f"Previous action: {dialogue_state.previous_action}")
    print(f"Next actions: {dialogue_state.next_actions}")

    # Transition to concluding state
    dialogue_state.conclude()
    print(f"Current state: {dialogue_state.state}")


if __name__ == "__main__":
    main()