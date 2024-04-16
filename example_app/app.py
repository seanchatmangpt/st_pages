import streamlit as st
from openai import OpenAI
from soc.models.root_aggregates.quest import create_apple_cultivation_quest
from soc.modules.generate_educational_content_module import generate_educational_content_call
from soc.modules.process_user_query_module import process_user_query_call
from soc.modules.provide_feedback_module import provide_feedback_call
from soc.modules.socratic_question_module import socratic_question_call

# db = FalkorDB(host='localhost', port=6379)

# res = g.query("""MATCH (r:Rider)-[:rides]->(t:Team)
#                  WHERE t.name = 'Yamaha'
#                  RETURN r.name""")


# Load your OpenAI API key from an environment variable or directly insert it (not recommended for production)
client = OpenAI()

selected_option_id = None

def app():
    quest = create_apple_cultivation_quest().model_dump()

    st.title(quest['title'])
    states = ['initial', 'teaching', 'quizzing', 'evaluating', 'concluding']
    dialogue_state = st.sidebar.selectbox("Select a Dialogue State", states)
    st.write(f"Selected State: {dialogue_state}")

    col_multq, col_chat = st.columns(2)

    with col_multq:
        if dialogue_state == 'initial' or dialogue_state == None:
            st.markdown("# Introduction")
            st.write(quest['description'])
        elif dialogue_state == 'quizzing':
            st.subheader("Questions")
            for question in quest['questions']:
                # Create a radio button for each option in question
                st.markdown(f"**{question['text']}**")
                options = {idx: option for idx, option in enumerate(question['options'])}
                selected_option_id = st.radio("Which of the following options most weakens this claim?",
                                              list(options.keys()),
                                              format_func=lambda x: options[x], index=None)

                if selected_option_id == question['correct_option']:
                    st.success("Correct!")
        else:
            st.markdown("# Teaching")
            for exam_point in quest['exam_points']:
                st.markdown(f"## Exam Point {exam_point['ep_number']}")
                st.write(exam_point['reasoning'])
                st.markdown("### Evidence")
                for evidence in exam_point['evidence']:
                    st.write(evidence)
                st.markdown("### Assumptions")
                for assumption in exam_point['assumptions']:
                    st.write(assumption)
                st.write(f"### Weight: {exam_point['weight']}")

            st.markdown("# Edges")
            for edge in quest['edges']:
                st.write(edge['bridging_concept'])
                st.write(f"### Weight: {exam_point['weight']}")

    with col_chat:
        user_input = st.chat_input("Discuss with Socrates?", key="user_input")

        print(user_input)

        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you with the apple cultivation quest?"}]

        for message in st.session_state["messages"]:
            chat = st.chat_message(message["role"])
            chat.write(message["content"])

        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            chat = st.chat_message("user")
            chat.write(user_input)

            try:
                print("Calling Socratic Question Module...")
                from soc.modules.evaluate_user_response_module import evaluate_user_response_call
                from dspygen.lm.groq_lm import Groq
                from dspygen.utils.dspy_tools import init_dspy
                init_dspy(Groq, model="mixtral-8x7b-32768")

                if dialogue_state == 'initial':
                    result = process_user_query_call(f"{quest['description']}{user_input}")
                elif dialogue_state == 'teaching':
                    result = generate_educational_content_call(f"{quest['exam_points']}{user_input}")
                elif dialogue_state == 'quizzing':
                    result = evaluate_user_response_call(f"{quest['questions']}\n{selected_option_id}\n{user_input}")
                elif dialogue_state == 'evaluating':
                    result = provide_feedback_call(f"{quest['exam_points']}{user_input}")
                elif dialogue_state == 'concluding':
                    result = provide_feedback_call(f"{quest['exam_points']}{user_input}")

                result = socratic_question_call(dialogue_state, f"{quest}{user_input}")
                print(f"Result: {result}")

                st.session_state["messages"].append({"role": "assistant", "content": result})
                chat = st.chat_message("assistant")
                chat.write(result)

            except Exception as e:
                st.error(f"Failed to generate response: {str(e)}")


if __name__ == '__main__':
    app()
