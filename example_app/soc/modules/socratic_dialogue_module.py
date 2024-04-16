"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class SocraticDialogueSignature(dspy.Signature):
    """
    A Signature for generating Socratic dialogue responses based on the current lesson state and student message.

    This module aims to facilitate educational dialogues by prompting students with thought-provoking questions or statements, encouraging deeper understanding and critical thinking.
    """
    lesson_state = dspy.InputField(
        desc="A representation of the current state of the lesson, including any relevant context or content that has been covered.")
    student_message = dspy.InputField(
        desc="The message or question posed by the student, to which the Socratic dialogue response should be tailored.")

    socratic_teacher_message = dspy.OutputField(
        desc="The generated message from the Socratic teacher, designed to provoke further thought, challenge assumptions, or clarify understanding.")




class SocraticDialogueModule(dspy.Module):
    """SocraticDialogueModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, lesson_state, student_message):
        pred = dspy.ChainOfThought(SocraticDialogueSignature)
        self.output = pred(lesson_state=lesson_state, student_message=student_message).socratic_teacher_message
        return self.output

    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer

app = Typer()


@app.command()
def call(lesson_state, student_message):
    """SocraticDialogueModule"""
    init_dspy()

    print(socratic_dialogue_call(lesson_state=lesson_state, student_message=student_message))


def socratic_dialogue_call(lesson_state, student_message):
    socratic_dialogue = SocraticDialogueModule()
    return socratic_dialogue.forward(lesson_state=lesson_state, student_message=student_message)


def main():
    init_dspy()
    from soc.models.root_aggregates.quest import create_apple_cultivation_quest
    lesson_state = str(create_apple_cultivation_quest())
    student_message = "Which state has the most problems?"
    print(socratic_dialogue_call(lesson_state=lesson_state, student_message=student_message))


from fastapi import APIRouter

router = APIRouter()


@router.post("/socratic_dialogue/")
async def socratic_dialogue_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return socratic_dialogue_call(**data)


"""
import streamlit as st


# Streamlit form and display
st.title("SocraticDialogueModule Generator")
lesson_state = st.text_input("Enter lesson_state")
student_message = st.text_input("Enter student_message")

if st.button("Submit SocraticDialogueModule"):
    init_dspy()

    result = socratic_dialogue_call(lesson_state=lesson_state, student_message=student_message)
    st.write(result)
"""

if __name__ == "__main__":
    main()
