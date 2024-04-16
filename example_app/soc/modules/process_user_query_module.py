"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ProcessUserQuery(dspy.Signature):
    """
    Processes a user's query, mapping it to relevant educational content, questions, or feedback opportunities.
    """
    user_query = dspy.InputField(desc="The query or message from the user.")
    query_response = dspy.OutputField(
        desc="The system's response, including relevant information, questions, or feedback.")


class ProcessUserQueryModule(dspy.Module):
    """ProcessUserQueryModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, user_query):
        pred = dspy.ChainOfThought(ProcessUserQuery)
        self.output = pred(user_query=user_query).query_response
        return self.output


def process_user_query_call(user_query):
    process_user_query = ProcessUserQueryModule()
    return process_user_query.forward(user_query=user_query)


def main():
    init_dspy()
    user_query = ""
    print(process_user_query_call(user_query=user_query))


if __name__ == "__main__":
    main()
