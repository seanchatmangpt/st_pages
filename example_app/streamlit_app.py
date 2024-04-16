from io import StringIO

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from dspygen.utils.dspy_tools import init_dspy

from soc.models.root_aggregates.quest import create_apple_cultivation_quest

data_csv = """year,state,crop
2019,Mississippi,970
2019,Louisiana,1144
2019,Arkansas,790
2019,Alabama,738
2020,Mississippi,1062
2020,Louisiana,1030
2020,Arkansas,803
2020,Alabama,738
2021,Mississippi,1007
2021,Louisiana,1093
2021,Arkansas,851
2021,Alabama,695
2022,Mississippi,1025
2022,Louisiana,1111
2022,Arkansas,756
2022,Alabama,739
2023,Mississippi,559
2023,Louisiana,1029
2023,Arkansas,781
2023,Alabama,745
2024,Mississippi,487
2024,Louisiana,651
2024,Arkansas,494
2024,Alabama,520
"""

### Ploting ----

df = pd.read_csv(StringIO(data_csv))

# Defining a color palette
color_palette = {
    'Mississippi': '#ff7f0e',
    'Louisiana': '#1f77b4',
    'Arkansas': '#17becf',
    'Alabama': '#2ca02c'
    # Add more states and colors as needed
}

fig = go.Figure()

actual_df = df[df['year'] != 2024]
expected_df = df[(df['year'] == 2023) | (df['year'] == 2024)]

# Add a light gray rectangle to highlight the expected range (2023 to 2024 (E))
fig.add_vrect(x0=2022.9, x1=2024.1, fillcolor="lightgray", opacity=0.1, line_width=0, layer="below")

# Adding scatter plot for all data points
for state in df['state'].unique():
    state_df = df[df['state'] == state].reset_index()
    fig.add_trace(go.Scatter(
        x=state_df['year'], y=state_df['crop'], mode='markers', name=state,
        marker=dict(color=color_palette[state]),
        hovertemplate=f"{state}: <br><b>%{{y:,.0f}} thousand ton</b> (%{{x}})"
    ))
    mid_row = state_df.iloc[2]  # Selecting the third last element
    fig.add_annotation(x=mid_row['year'], y=mid_row['crop'], text=state,
                       showarrow=False, yshift=10, font=dict(color=color_palette[state]),
                       xref="x", yref="y")  # Ensure xref and yref are set to align with the axis

# Adding lines for actual and expected data
for df_subset, line_dash in [(actual_df, 'solid'), (expected_df, 'dot')]:
    for state in df_subset['state'].unique():
        state_df = df_subset[df_subset['state'] == state]
        fig.add_trace(go.Scatter(
            x=state_df['year'], y=state_df['crop'], mode='lines', name=state,
            line=dict(color=color_palette[state], dash=line_dash),
            hoverinfo='skip'  # Skip hover info for lines to avoid redundancy
        ))

# Update layout with professional theme, y-axis starting from 0, and customized zero line
fig.update_layout(
    title='Trend of apple cultivation by state',
    xaxis_title='Year',
    xaxis=dict(
        tickmode='array',
        tickvals=df['year'].unique(),
        ticktext=[str(year) if year != 2024 else '2024,<br>expected' for year in df['year'].unique()]
    ),
    yaxis_title='Crop (000 t)',
    plot_bgcolor='rgba(0,0,0,0)',  # Set plot background to transparent
    paper_bgcolor='rgba(0,0,0,0)',  # Set overall figure background to transparent
    template='plotly_white',
    yaxis=dict(range=[0, df['crop'].max() * 1.1], zeroline=True, zerolinewidth=2, zerolinecolor='gray'),
    showlegend=False,
    font=dict(size=14)  # Increase font size slightly
)

# Chat class ----

client = OpenAI()
# DEFAULT_MODEL = "gpt-4-0125-preview"
DEFAULT_MODEL = "gpt-3.5-turbo-0125"  # FOR TESTING

# App ---

_ = load_dotenv(find_dotenv())  # read local .env file

st.set_page_config(layout="wide")

col_multq, col_chat = st.columns(2)

if "phase1_submitted" not in st.session_state:
    st.session_state["phase1_submitted"] = False

with col_multq:
    st.write("The data below shows the trend in apple cultivation in major states within the US.")

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.write(
        "It is believed that the approximately 40% decrease in cultivation volume in 2023 within Mississippi is due to a new species of parasite, against which none of the existing insecticides are effective. This species of parasite reproduces very quickly and is expected to spread across the United States within 2024. Therefore, apple cultivation volume across the United States is expected to decrease by 40% in 2024.")

    options = {
        'a': "(a) Other crops in Mississippi have also been attacked by this parasite.",
        'b': "(b) The natural predator of this parasite hardly survives in Mississippi but is significantly distributed in other apple cultivation areas.",
        'c': "(c) 95% of apples cultivated across the United States are of the Granny Smith variety, which is the only variety of apple cultivated in Mississippi.",
        'd': "(d) Because the quantity of apple demand in the United States can be met with import quantities, apple prices in the United States will not increase in 2024.",
        'e': "(e) Numerous agricultural scientists in the United States are currently making significant efforts to create a genetically modified apple variety resistant to Mississippi's parasites, which could reduce damage if this variant soon becomes available.",
    }
    selected_option_id = st.radio("Which of the following options most weakens this claim?", list(options.keys()),
                                  format_func=lambda x: options[x], index=None)

    # Show the text area if an option is selected
    if selected_option_id:
        choice_rationale = st.text_area("Please explain why you made the choice.", height=150)
        if st.button('Submit'):
            st.session_state["phase1_submitted"] = True

with col_chat:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    # NOTE: for some reason, I couldn't correct the location of the chat input

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        from soc.modules.socratic_dialogue_module import socratic_dialogue_call

        init_dspy()
        result = socratic_dialogue_call(str(create_apple_cultivation_quest()), prompt)
        msg = result

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    with st.expander("Socrates thought process"):
        st.json(st.session_state.messages)