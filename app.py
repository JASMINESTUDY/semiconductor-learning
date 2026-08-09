import json
import os
import re
import streamlit as st


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Semiconductor Learning Hub",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.html("""
<style>

body {
    background-color: #f4f7fb;
}

.hero {
    background: linear-gradient(
        135deg,
        #0b1220,
        #172554
    );

    padding: 40px;
    border-radius: 22px;
    color: white;
    margin-bottom: 30px;
}

.hero-badge {
    color: #93c5fd;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 17px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
}

.section-title {
    font-size: 23px;
    font-weight: 750;
    color: #0f172a;
    margin-top: 30px;
    margin-bottom: 15px;
}

.keyword {
    background: white;
    padding: 14px 16px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
    margin-bottom: 10px;
}

.takeaway {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.quiz-card {
    background: white;
    padding: 28px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    margin-top: 25px;
}

.quiz-badge {
    display: inline-block;
    background: #dbeafe;
    color: #1d4ed8;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.score {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-top: 20px;
}

.score-number {
    font-size: 36px;
    font-weight: 800;
    color: #1d4ed8;
}

</style>
""")


# ============================================================
# FIND JSON FILES
# ============================================================

def get_json_files():

    files = [
        f for f in os.listdir()
        if f.lower().endswith(".json")
    ]

    def module_number(filename):

        match = re.search(
            r"Module\s+(\d+)",
            filename,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

        return 999

    files.sort(key=module_number)

    return files


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
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        SEMICONDUCTOR LEARNING PLATFORM
    </div>

    <div class="hero-title">
        🧠 Semiconductor Learning Hub
    </div>

    <div class="hero-subtitle">
        Learn semiconductor knowledge step by step,
        from fundamentals to advanced industry concepts.
    </div>

</div>
""")


# ============================================================
# FIND MODULES
# ============================================================

json_files = get_json_files()

if not json_files:

    st.error("No JSON files found.")

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧠 Learning Hub")

st.sidebar.caption(
    "Semiconductor knowledge builder"
)

st.sidebar.divider()


module_names = [
    f.replace(".json", "")
    for f in json_files
]


selected_module = st.sidebar.selectbox(
    "📚 Choose Module",
    module_names
)


module_index = module_names.index(
    selected_module
)


selected_file = json_files[
    module_index
]


# ============================================================
# LOAD MODULE
# ============================================================

data = load_json(
    selected_file
)


topics = data.get(
    "topics",
    []
)


if not topics:

    st.error("No topics found.")

    st.stop()


# ============================================================
# TOPIC SELECTOR
# ============================================================

topic_names = [
    topic["title"]
    for topic in topics
]


selected_topic = st.sidebar.selectbox(
    "🎯 Choose Topic",
    topic_names
)


topic_index = topic_names.index(
    selected_topic
)


topic = topics[
    topic_index
]


# ============================================================
# PROGRESS
# ============================================================

progress = (
    topic_index + 1
) / len(topics)


st.sidebar.divider()

st.sidebar.markdown(
    "### 📈 Topic Progress"
)

st.sidebar.progress(
    progress
)

st.sidebar.caption(
    f"Topic {topic_index + 1} of {len(topics)}"
)


# ============================================================
# MODULE HEADER
# ============================================================

st.html(
    f"""
    <div class="card">

        <div style="
            color:#2563eb;
            font-size:13px;
            font-weight:700;
            letter-spacing:1px;
        ">
            MODULE {module_index + 1}
        </div>

        <div style="
            font-size:28px;
            font-weight:800;
            color:#0f172a;
            margin-top:5px;
        ">
            {data.get("module_name", selected_module)}
        </div>

    </div>
    """
)


# ============================================================
# TOPIC
# ============================================================

st.html(
    f"""
    <div class="card">

        <div style="
            color:#2563eb;
            font-size:13px;
            font-weight:700;
            letter-spacing:1px;
        ">
            CURRENT TOPIC
        </div>

        <div style="
            font-size:25px;
            font-weight:750;
            color:#0f172a;
            margin-top:5px;
        ">
            {topic["title"]}
        </div>

    </div>
    """
)


# ============================================================
# LEARNING CONTENT
# ============================================================

st.html("""
<div class="section-title">
    📖 Learning Content
</div>
""")


content = topic.get(
    "content",
    ""
)

# Content from your JSON is rendered as normal Markdown.
st.markdown(content)


# ============================================================
# KEYWORDS
# ============================================================

st.html("""
<div class="section-title">
    🔑 Key Terminology
</div>
""")


keywords = topic.get(
    "keywords",
    []
)


columns = st.columns(2)


for i, keyword in enumerate(keywords):

    with columns[i % 2]:

        st.html(
            f"""
            <div class="keyword">

                <strong style="color:#1e3a8a;">
                    {keyword.get("english", "")}
                </strong>

                <span style="
                    color:#60a5fa;
                    padding:0 8px;
                ">
                    →
                </span>

                <span style="color:#475569;">
                    {keyword.get("chinese", "")}
                </span>

            </div>
            """
        )


# ============================================================
# KEY TAKEAWAYS
# ============================================================

st.html("""
<div class="section-title">
    💡 Key Takeaways
</div>
""")


for item in topic.get(
    "summary",
    []
):

    st.html(
        f"""
        <div class="takeaway">
            ✓ {item}
        </div>
        """
    )


# ============================================================
# SHORT QUIZ
# ============================================================

questions = topic.get(
    "quiz_short",
    []
)


if questions:

    st.html("""
    <div class="quiz-card">

        <span class="quiz-badge">
            ACTIVE RECALL
        </span>

        <div style="
            font-size:25px;
            font-weight:800;
            color:#0f172a;
            margin-top:10px;
        ">
            🧠 Quick Check
        </div>

        <div style="
            color:#64748b;
            margin-top:5px;
        ">
            Test your understanding before moving on.
        </div>

    </div>
    """)


    answers = []


    for i, q in enumerate(questions):

        st.markdown(
            f"### Question {i + 1}"
        )

        st.info(
            q["question"]
        )

        answer = st.text_input(
            "Your answer",
            key=f"answer_{module_index}_{topic_index}_{i}"
        )

        answers.append(
            answer
        )


    if st.button(
        "🔍 Check My Answers",
        type="primary"
    ):

        score = 0


        for i, q in enumerate(questions):

            user_answer = (
                answers[i]
                .strip()
                .lower()
            )

            correct_answer = (
                str(q["answer"])
                .strip()
                .lower()
            )


            if user_answer == correct_answer:

                score += 1

                st.success(
                    f"Question {i + 1}: Correct ✓"
                )

            else:

                st.error(
                    f"Question {i + 1}: Incorrect"
                )

                st.caption(
                    f"Correct answer: {q['answer']}"
                )


        percentage = (
            score / len(questions)
        ) * 100


        st.html(
            f"""
            <div class="score">

                <div class="score-number">
                    {score} / {len(questions)}
                </div>

                <div style="color:#475569;">
                    Quiz Score · {percentage:.0f}%
                </div>

            </div>
            """
        )


# ============================================================
# DISCUSSION
# ============================================================

long_questions = topic.get(
    "quiz_long",
    []
)


if long_questions:

    st.html("""
    <div class="section-title">
        💬 Discussion & Deeper Thinking
    </div>
    """)


    st.info(
        "Think about your answer first, "
        "then reveal the suggested answer."
    )


    for i, q in enumerate(long_questions):

        with st.expander(
            f"💭 Question {i + 1}: {q['question']}"
        ):

            st.write(
                "Think first. Explain the concept "
                "in your own words."
            )

            if st.button(
                "Show Suggested Answer",
                key=f"discussion_{module_index}_{topic_index}_{i}"
            ):

                st.markdown(
                    "### Suggested Answer"
                )

                st.info(
                    q["answer"]
                )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div style="
    text-align:center;
    color:#94a3b8;
    font-size:13px;
    margin-top:50px;
    padding-top:20px;
    border-top:1px solid #e2e8f0;
">
    Semiconductor Learning Hub ·
    Built with Python + Streamlit
</div>
""")