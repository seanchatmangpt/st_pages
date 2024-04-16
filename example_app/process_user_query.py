import asyncio

import streamlit as st

from dspygen.utils.dspy_tools import init_dspy

st.title("🔎 Process User Query")

process_prompt = st.text_area(
    "Enter User Query for Processing", ""
)

if st.button("Process User Query"):
    st.write("Processing Query...")

    async def run():  # Changed from "async_conversion"
        from soc.modules.process_user_query_module import process_user_query_call
        from dspygen.lm.groq_lm import Groq
        init_dspy(Groq, model="mixtral-8x7b-32768")
        result = process_user_query_call(process_prompt)
        st.write(result)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())  # Changed from "async_conversion"
    st.write("Query Evaluated!")  # Changed from "Identification complete!"
