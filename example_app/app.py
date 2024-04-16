from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons should be
show_pages(
    [
        Page("src/soc/mockup.py", "Mockup", "📐"),
        Page("src/soc/school.py", "School", "🏫"),
        Page("src/soc/assess.py", "Learning Assessment", "📊"),
        Page("src/soc/evaluate.py", "Evaluate Response Progress", "📈"),
        Page("src/soc/generate_content.py", "Generate Content", "🧠"),
        Page("src/soc/process_user_query.py", "Process User Query", "🔎"),
        Page("src/soc/provide_feedback.py", "Provide Feedback", "💬"),
        Page("src/soc/socratic_question.py", "Socratic Question", "🤔"),
    ]
)
