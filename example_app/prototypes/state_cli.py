from transitions import Machine
from soc.models.root_aggregates.quest import create_apple_cultivation_quest

class DialogueState(Machine):
    states = ['initial', 'teaching', 'quizzing', 'evaluating', 'concluding']

    transitions = [
        {'trigger': 'start', 'source': 'initial', 'dest': 'teaching'},
        {'trigger': 'next', 'source': 'teaching', 'dest': 'quizzing'},
        {'trigger': 'answer', 'source': 'quizzing', 'dest': 'evaluating'},
        {'trigger': 'evaluate', 'source': 'evaluating', 'dest': 'quizzing', 'conditions': 'has_more_questions'},
        {'trigger': 'evaluate', 'source': 'evaluating', 'dest': 'concluding', 'unless': 'has_more_questions'},
        {'trigger': 'exit', 'source': '*', 'dest': 'concluding'}  # Can exit from any state (except 'initial')
    ]

    def __init__(self, quest):
        self.quest = quest
        self.current_question_index = 0
        super().__init__(states=DialogueState.states, transitions=DialogueState.transitions, initial='initial')
        self.answers = [q.correct_option for q in quest.questions]  # Simulating correct answers

    def on_enter_teaching(self):
        """Prepares and displays teaching content for the current part of the quest."""
        print("Entering teaching state. Preparing content...")
        # ... Logic to fetch and display educational material ...

    def on_enter_quizzing(self):
        """Displays the current quiz question."""
        question = self.quest.questions[self.current_question_index]
        print(f"Question {self.current_question_index + 1}: {question.text}")
        # ... Display options ...

    def on_enter_evaluating(self, answer):
        """Evaluates the provided answer."""
        print(f"Evaluating answer for question {self.current_question_index + 1}...")
        correct_answer = self.answers[self.current_question_index]
        if answer == correct_answer:
            print("Correct!")
        else:
            print("Incorrect.")
        self.current_question_index += 1

    def has_more_questions(self):
        """Determines if there are more questions in the quest."""
        return self.current_question_index < len(self.quest.questions)

    def on_enter_concluding(self):
        """Handles the conclusion of the quest."""
        print("All questions answered. Concluding quest.")
        # ... Logic to display summary, calculate scores (if applicable), etc. ...

# Example usage (similar to before)
def main2():
    """Simulates a happy path interaction with the Socratic AI Tutoring System."""
    quest = create_apple_cultivation_quest()
    dialogue_state = DialogueState(quest=quest)

    print(">>> Starting the quest...")
    dialogue_state.start()
    print(f"State: {dialogue_state.state}")

    print(">>> Moving to the next part (quizzing)...")
    dialogue_state.next()
    print(f"State: {dialogue_state.state}")

    # Simulate answering all questions correctly
    for i in range(len(quest.questions)):
        print(">>> Answering a question correctly...")
        answer = dialogue_state.answers[dialogue_state.current_question_index]  # Get correct answer
        dialogue_state.answer(answer)
        dialogue_state.evaluate()
        print(f"State: {dialogue_state.state}")

    print(">>> Concluding the quest...")
    dialogue_state.exit()
    print(f"State: {dialogue_state.state}")


def parse_command(user_input):
    """Simplifies command parsing for this example."""
    if not user_input.startswith('/'):
        return user_input
    return user_input.strip().lower()[1:]  # Remove leading '/' and convert to lowercase

def main():
    """Simulates a happy path interaction with the Socratic AI Tutoring System."""
    quest = create_apple_cultivation_quest()
    dialogue_state = DialogueState(quest=quest)

    # Print the /commands to move to states
    print(">>> Use /commands to move to states: /start")

    while dialogue_state.state != 'concluding':
        user_input = input("Enter command or talk: ")
        command = parse_command(user_input)
        if getattr(dialogue_state, command, None):
            print(f"Executing command: {command}")
            print(f"State: {dialogue_state.state}")

        if dialogue_state.state == "initial" and command == "start":
            print(f">>> Starting the quest... {quest.description}")
            print(f">>> Use the /next command to move to the next part (teaching)...")
        elif dialogue_state.state == "teaching":
            print(f">>> Use the /answer command to answer the question...")
        elif dialogue_state.state == "quizzing":
            print(f">>> Use the /answer command to answer the question...")
        elif dialogue_state.state == "evaluating":
            print(f">>> Use the /evaluate command to evaluate the answer...")
        elif dialogue_state.state == "concluding":
            print(f">>> Quest concluded. Exiting...")

        # print(">>> Starting the quest...")
        # dialogue_state.start()
        # print(f"State: {dialogue_state.state}")
        #
        # print(">>> Moving to the next part (quizzing)...")
        # dialogue_state.next()
        # print(f"State: {dialogue_state.state}")
        #
        # # Simulate answering all questions correctly
        # for i in range(len(quest.questions)):
        #     print(">>> Answering a question correctly...")
        #     answer = dialogue_state.answers[dialogue_state.current_question_index]  # Get correct answer
        #     dialogue_state.answer(answer)
        #     dialogue_state.evaluate()
        #     print(f"State: {dialogue_state.state}")
        #
        # print(">>> Concluding the quest...")
        # dialogue_state.exit()
        # print(f"State: {dialogue_state.state}")


if __name__ == "__main__":
    main()