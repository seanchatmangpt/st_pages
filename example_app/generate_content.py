import asyncio

import streamlit as st

from dspygen.utils.dspy_tools import init_dspy

st.title("🧠 Generate Educational Content")


process_prompt = st.text_area(
    "Source for Content", ""
)

if st.button("Generate Content"):
    st.write("Generating...")

    async def run():
        from soc.modules.generate_educational_content_module import generate_educational_content_call
        from dspygen.lm.groq_lm import Groq
        init_dspy(Groq, model="mixtral-8x7b-32768")
        result = generate_educational_content_call(process_prompt)
        st.write(result)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    st.write("Response Evaluated!")
