"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class SocraticQuestion(dspy.Signature):
    """
    Generates a Socratic question based on the provided context.
    """
    dialog_state = dspy.InputField(desc="The current state of the dialogue. Initial, teaching, quizzing, evaluating, or concluding.")
    context = dspy.InputField(desc="The current educational context or user's message to base the question on.")
    socratic_question = dspy.OutputField(desc="A question designed to provoke deeper thought or clarification.")


class SocraticQuestionModule(dspy.Module):
    """SocraticQuestionModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, dialog_state, context):
        pred = dspy.ChainOfThought(SocraticQuestion)
        self.output = pred(dialog_state=dialog_state, context=context).socratic_question
        return self.output
        

def socratic_question_call(dialog_state, context):
    socratic_question = SocraticQuestionModule()
    return socratic_question.forward(dialog_state=dialog_state, context=context)


def main():
    init_dspy()
    context = "Apple yield question"
    print(socratic_question_call(context=context))


if __name__ == "__main__":
    main()
