import asyncio

import streamlit as st

from dspygen.utils.dspy_tools import init_dspy

st.title("🤔 Socratic Question")

process_prompt = st.text_area(
    "Enter Source For Question", ""
)

if st.button("Process Question"):
    st.write("Processing Question...")

    async def run():
        from soc.modules.socratic_question_module import socratic_question_call
        from dspygen.lm.groq_lm import Groq
        init_dspy(Groq, model="mixtral-8x7b-32768")
        result = socratic_question_call(process_prompt)
        st.write(result)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    st.write("Question Processed!")
