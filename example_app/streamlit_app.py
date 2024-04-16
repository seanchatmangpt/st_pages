from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons should be
show_pages(
    [
        Page("mockup.py", "Mockup", "📐"),
        Page("school.py", "School", "🏫"),
        Page("assess.py", "Learning Assessment", "📊"),
        Page("evaluate.py", "Evaluate Response Progress", "📈"),
        Page("generate_content.py", "Generate Content", "🧠"),
        Page("process_user_query.py", "Process User Query", "🔎"),
        Page("provide_feedback.py", "Provide Feedback", "💬"),
        Page("socratic_question.py", "Socratic Question", "🤔"),
    ]
)

