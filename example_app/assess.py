import asyncio

import streamlit as st

from dspygen.utils.dspy_tools import init_dspy

# Set the title for the Assess Learning Progress Dashboard
st.title("📊 Assess Learning Progress")

# Interface for different Assess Learning Progress subcommands
process_prompt = st.text_area(
    "Enter Learning Progress for Assessment", ""
)  # Changed from "Enter Process Description for Identification"

if st.button("Assess Learning"):  # Changed from "Identify"
    st.write("Assessing Learning...")  # Changed from "Identifying..."

    # Run the assessing asynchronously
    async def async_assessing():  # Changed from "async_conversion"
        from soc.modules.assess_learning_progress_module import assess_learning_progress_call
        init_dspy()
        result = assess_learning_progress_call(process_prompt)
        st.write(result)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_assessing())  # Changed from "async_conversion"
    st.write("Learning Assessmentcomplete!")  # Changed from "Identification complete!"
