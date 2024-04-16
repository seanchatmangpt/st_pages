import asyncio

import streamlit as st

from dspygen.utils.dspy_tools import init_dspy

st.title("💬 Provide Feedback")

process_prompt = st.text_area(
    "Enter User Feedback for Processing", ""
)

if st.button("Process User Feedback"):
    st.write("Processing Feedback...")

    async def run():
        from soc.modules.provide_feedback_module import provide_feedback_call
        from dspygen.lm.groq_lm import Groq
        init_dspy(Groq, model="mixtral-8x7b-32768")
        result = provide_feedback_call(process_prompt)
        st.write(result)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    st.write("Feedback Evaluated!")
