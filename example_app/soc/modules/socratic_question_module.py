"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class SocraticDialogue(dspy.Signature):
    """
    Generates a Socratic dialogue based on the provided context.
    """
    dialog_subject = dspy.InputField(desc="The current subject of the dialogue.")
    user_context = dspy.InputField(desc="The current educational context or user's message to base the dialogue on.")
    socratic_dialogue = dspy.OutputField(desc="Engage in a Socratic dialogue by considering the user's context")


class SocraticDialogueModule(dspy.Module):
    """SocraticDialogueModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, dialog_state, context):
        pred = dspy.ChainOfThought(SocraticDialogue)
        self.output = pred(dialog_state=dialog_state, context=context).socratic_dialogue
        return self.output
        

def socratic_dialogue_call(dialog_state, context):
    socratic_dialogue = SocraticDialogueModule()
    return socratic_dialogue.forward(dialog_state=dialog_state, context=context)


def main():
    init_dspy()
    context = "Apple yield dialogue"
    print(socratic_dialogue_call(context=context))


if __name__ == "__main__":
    main()
