"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ProvideFeedback(dspy.Signature):
    """
    Provides constructive feedback based on the user's response, aiming to reinforce correct understanding or correct misconceptions.
    """
    user_response = dspy.InputField(desc="The user's response to evaluate.")
    feedback = dspy.OutputField(
        desc="Constructive feedback aimed at reinforcing or correcting the user's understanding.")


class ProvideFeedbackModule(dspy.Module):
    """ProvideFeedbackModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def forward(self, user_response):
        pred = dspy.ChainOfThought(ProvideFeedback)
        self.output = pred(user_response=user_response).feedback
        return self.output


def provide_feedback_call(user_response):
    provide_feedback = ProvideFeedbackModule()
    return provide_feedback.forward(user_response=user_response)


def main():
    init_dspy()
    user_response = ""
    print(provide_feedback_call(user_response=user_response))


if __name__ == "__main__":
    main()
