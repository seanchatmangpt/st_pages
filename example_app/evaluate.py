import asyncio

import streamlit as st

from dspygen.utils.dspy_tools import init_dspy

st.title("📈 Evaluate Response Progress")

process_prompt = st.text_area(
    "Enter Response Progress for Evaluation",  ""
)

if st.button("Evaluate Response"):
    st.write("Evaluating Response...")


    async def run():
        from soc.modules.evaluate_user_response_module import evaluate_user_response_call
        from dspygen.lm.groq_lm import Groq
        init_dspy(Groq, model="mixtral-8x7b-32768")
        result = evaluate_user_response_call(process_prompt)
        st.write(result)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    st.write("Response Evaluated!")
