"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class UpdateUserModel(dspy.Signature):
    """
    Updates the user model based on the latest interaction, adjusting the model to better reflect the user's current understanding and needs.
    """
    user_interaction = dspy.InputField(desc="Details of the user's latest interaction.")
    updated_user_model = dspy.OutputField(desc="An updated model of the user's understanding and learning progress.")


class UpdateUserModelModule(dspy.Module):
    """UpdateUserModelModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def forward(self, user_interaction):
        pred = dspy.Predict(UpdateUserModel)
        self.output = pred(user_interaction=user_interaction).updated_user_model
        return self.output


def update_user_model_call(user_interaction):
    update_user_model = UpdateUserModelModule()
    return update_user_model.forward(user_interaction=user_interaction)


def main():
    init_dspy()
    user_interaction = ""
    print(update_user_model_call(user_interaction=user_interaction))


if __name__ == "__main__":
    main()
