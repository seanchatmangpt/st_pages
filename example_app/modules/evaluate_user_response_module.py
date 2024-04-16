"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class EvaluateUserResponse(dspy.Signature):
    """
    Evaluates the user's response against the expected learning outcomes, providing insights into the user's understanding and misconceptions.
    """
    user_response = dspy.InputField(desc="The user's response to the previous question.")
    evaluation_result = dspy.OutputField(
        desc="Evaluation of the user's response, highlighting understanding and identifying misconceptions.")


class EvaluateUserResponseModule(dspy.Module):
    """EvaluateUserResponseModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, user_response):
        pred = dspy.ChainOfThought(EvaluateUserResponse)
        self.output = pred(user_response=user_response).evaluation_result
        return self.output
        

def evaluate_user_response_call(user_response):
    evaluate_user_response = EvaluateUserResponseModule()
    return evaluate_user_response.forward(user_response=user_response)


def main():
    init_dspy()
    user_response = ""
    print(evaluate_user_response_call(user_response=user_response))


if __name__ == "__main__":
    main()
