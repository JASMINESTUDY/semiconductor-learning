import json
import os
import re
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Semiconductor Learning with Jasmine",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM STYLE
# ============================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    .keyword-box {
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 8px;
        background-color: #f5f5f5;
    }

    .takeaway-box {
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 8px;
        background-color: #f8f9fa;
    }

    .quiz-question {
        font-size: 18px;
        font-weight: 600;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FIND JSON FILES
# ============================================================

def get_json_files():

    json_files = [
        f for f in os.listdir()
        if f.lower().endswith(".json")
    ]

    def module_number(filename):
        match = re.search(r"Module\s+(\d+)", filename, re.IGNORECASE)

        if match:
            return int(match.group(1))

        return 999

    json_files.sort(key=module_number)

    return json_files


# ============================================================
# LOAD JSON
# ============================================================

@st.cache_data
def load_json(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# DISPLAY TOPIC CONTENT
# ============================================================

def show_topic(topic):

    st.markdown(
        f"# 📚 {topic['title']}"
    )

    st.divider()

    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📖 Learning Content</div>',
        unsafe_allow_html=True
    )

    # Preserve line breaks from JSON
    content = topic.get("content", "")

    st.markdown(
        content.replace("\n", "  \n")
    )

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🔑 Keywords</div>',
        unsafe_allow_html=True
    )

    keywords = topic.get("keywords", [])

    if keywords:

        cols = st.columns(2)

        for i, keyword in enumerate(keywords):

            with cols[i % 2]:

                st.markdown(
                    f"""
                    <div class="keyword-box">
                    <b>{keyword['english']}</b>
                    → {keyword['chinese']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # --------------------------------------------------------
    # KEY TAKEAWAYS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">💡 Key Takeaways</div>',
        unsafe_allow_html=True
    )

    for item in topic.get("summary", []):

        st.markdown(
            f"""
            <div class="takeaway-box">
            ✓ {item}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# SHORT QUIZ
# ============================================================

def run_short_quiz(topic):

    st.markdown(
        '<div class="section-title">🧠 Short Quiz</div>',
        unsafe_allow_html=True
    )

    questions = topic.get("quiz_short", [])

    if not questions:

        st.info("No short quiz available for this topic.")

        return

    st.write(
        "Fill in the blank and check your answers."
    )

    answers = {}

    for i, q in enumerate(questions):

        st.markdown(
            f'<div class="quiz-question">{q["question"]}</div>',
            unsafe_allow_html=True
        )

        answers[i] = st.text_input(
            "Your answer:",
            key=f"short_answer_{topic['id']}_{i}"
        )

    if st.button(
        "✅ Check Answers",
        key=f"check_short_{topic['id']}"
    ):

        score = 0

        for i, q in enumerate(questions):

            user_answer = answers[i].strip().lower()

            correct_answer = (
                q["answer"]
                .strip()
                .lower()
            )

            if user_answer == correct_answer:

                score += 1

                st.success(
                    f"Question {i + 1}: Correct! ✓"
                )

            else:

                st.error(
                    f"Question {i + 1}: Incorrect."
                )

                st.write(
                    f"**Correct answer:** {q['answer']}"
                )

        st.markdown("---")

        st.subheader(
            f"🎯 Your Score: {score}/{len(questions)}"
        )

        percentage = (
            score / len(questions) * 100
        )

        if percentage == 100:

            st.balloons()

            st.success(
                "Excellent! Perfect score! 🎉"
            )

        elif percentage >= 70:

            st.success(
                "Good job! Keep reviewing the topic."
            )

        else:

            st.warning(
                "Review the learning content and try again."
            )


# ============================================================
# LONG QUIZ / DISCUSSION
# ============================================================

def run_long_quiz(topic):

    st.markdown(
        '<div class="section-title">💬 Discussion Questions</div>',
        unsafe_allow_html=True
    )

    questions = topic.get("quiz_long", [])

    if not questions:

        st.info(
            "No discussion questions available."
        )

        return

    st.write(
        "Think about your answer first, then reveal the suggested answer."
    )

    for i, q in enumerate(questions):

        with st.expander(
            f"Question {i + 1}: {q['question']}"
        ):

            st.write(
                "**Think about it before revealing the answer.**"
            )

            if st.button(
                "Show Suggested Answer",
                key=f"long_answer_{topic['id']}_{i}"
            ):

                st.info(
                    q["answer"]
                )


# ============================================================
# MAIN APP
# ============================================================

def main():

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">🧠 Semiconductor Learning with Jasmine</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'A self-learning platform for semiconductor fundamentals, '
        'industry knowledge, and technical concepts.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # FIND MODULES
    # --------------------------------------------------------

    json_files = get_json_files()

    if not json_files:

        st.error(
            "No JSON module files were found."
        )

        st.info(
            "Please make sure app.py is in the same folder "
            "as your Module JSON files."
        )

        return

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    st.sidebar.title("📚 Learning Modules")

    module_options = []

    for filename in json_files:

        module_options.append(
            filename.replace(".json", "")
        )

    selected_module_name = st.sidebar.selectbox(
        "Choose a Module",
        module_options
    )

    selected_index = module_options.index(
        selected_module_name
    )

    selected_file = json_files[selected_index]

    # --------------------------------------------------------
    # LOAD MODULE
    # --------------------------------------------------------

    try:

        data = load_json(selected_file)

    except Exception as e:

        st.error(
            f"Unable to load module: {e}"
        )

        return

    # --------------------------------------------------------
    # MODULE HEADER
    # --------------------------------------------------------

    st.header(
        f"Module {data.get('module_name', selected_module_name)}"
    )

    topics = data.get("topics", [])

    if not topics:

        st.warning(
            "No topics found in this module."
        )

        return

    # --------------------------------------------------------
    # TOPIC SELECTION
    # --------------------------------------------------------

    topic_titles = [
        topic["title"]
        for topic in topics
    ]

    selected_topic_title = st.sidebar.selectbox(
        "Choose a Topic",
        topic_titles
    )

    topic_index = topic_titles.index(
        selected_topic_title
    )

    topic = topics[topic_index]

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    progress = (
        (topic_index + 1)
        / len(topics)
    )

    st.sidebar.markdown(
        f"### Topic Progress"
    )

    st.sidebar.progress(progress)

    st.sidebar.write(
        f"Topic {topic_index + 1} / {len(topics)}"
    )

    # --------------------------------------------------------
    # SHOW TOPIC
    # --------------------------------------------------------

    show_topic(topic)

    st.divider()

    # --------------------------------------------------------
    # QUIZ
    # --------------------------------------------------------

    run_short_quiz(topic)

    st.divider()

    run_long_quiz(topic)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()