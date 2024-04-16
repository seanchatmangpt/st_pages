"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class MapConversationToDomainModel(dspy.Signature):
    """
    Maps a conversation or message to the relevant domain model, facilitating deeper understanding and processing of the user's intent.
    """
    conversation_message = dspy.InputField(desc="A message or part of the conversation to map.")
    domain_model_instance = dspy.OutputField(
        desc="The mapped domain model instance, reflecting the conversation's context.")


class MapConversationToDomainModelModule(dspy.Module):
    """MapConversationToDomainModelModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def forward(self, conversation_message):
        pred = dspy.ChainOfThought(MapConversationToDomainModel)
        self.output = pred(conversation_message=conversation_message).domain_model_instance
        return self.output


def map_conversation_to_domain_model_call(conversation_message):
    map_conversation_to_domain_model = MapConversationToDomainModelModule()
    return map_conversation_to_domain_model.forward(conversation_message=conversation_message)


def main():
    init_dspy()
    conversation_message = ""
    print(map_conversation_to_domain_model_call(conversation_message=conversation_message))


if __name__ == "__main__":
    main()
