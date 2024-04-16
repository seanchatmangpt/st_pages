from dspy import Signature, InputField, OutputField


class TranslateResponseState(Signature):
    """
    Translates the user's response into English, ensuring the preservation of the logical concept. This step forms
    the foundation for understanding and engaging with the user's input in a meaningful way. The aim is to retain the
    essence of the argument while preparing it for logical decomposition.
    """
    user_response = InputField(desc="The raw response from the user.")
    translated_response = OutputField(desc="The translated response in English with logical "
                                           "structure retained. 30 words max. S")


class DecomposeLogicState(Signature):
    """
    Breaks down the user's translated response into its logical components: conclusion, supporting reasons,
    and assumptions. This process is crucial for critically analyzing the argument and guiding the user through the
    Socratic Method effectively. It lays the groundwork for identifying areas that require further exploration or
    clarification.
    """
    translated_response = InputField(desc="The translated response from the user.")
    logical_structure = OutputField(
        desc="The decomposed logical structure consisting of Conclusion, Supporting reasons, and Assumptions.")


class IdentifyRelevantEPState(Signature):
    """
    Identifies the most relevant Exam Point (EP) based on the decomposed logical structure of the user's response.
    This class ensures that the discussion remains focused and productive, steering the conversation towards
    meaningful insights and learning outcomes.
    """
    logical_structure = InputField(desc="The logical structure of the user's response.")
    relevant_EP = OutputField(desc="The most relevant EP based on the logical structure.")


class AssessEvidenceAndReasoningState(Signature):
    """
    Evaluates the soundness of the evidence and reasoning within the user's argument. This critical assessment is key
    to fostering a deeper understanding and encouraging the user to consider alternative perspectives or strengthen
    their argumentation.
    """
    logical_structure = InputField(desc="The logical structure of the user's response.")
    evidence_and_reasoning_assessment = OutputField(desc="Assessment of the soundness of evidence and reasoning.")


class ConstructQuestionState(Signature):
    """
    Based on the current state of discussion, this class constructs a question designed to provoke thought,
    challenge assumptions, or clarify reasoning. The questions crafted here are pivotal for advancing the dialogue in
    a constructive and educational manner.
    """
    discussion_context = InputField(
        desc="Context of the discussion including logical structure, relevant EP, and assessment.")
    formulated_question = OutputField(desc="The question constructed to facilitate the discussion.")


class FeedbackReviewState(Signature):
    """
    Engages with feedback received from the RED team on the constructed questions, fostering a collaborative effort
    to refine the chatbot's inquiry and ensure the highest quality of discourse. This state embodies the chatbot's
    commitment to continuous improvement and adaptation.
    """
    original_question = InputField(desc="The original question submitted to RED.")
    red_feedback = InputField(desc="Feedback received from RED.")
    alternative_question = OutputField(desc="An alternative question based on RED's feedback.")
