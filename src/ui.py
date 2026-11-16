
import re
import streamlit as st

from src.ai import ask_ai
from src.ingest import extract_text
from src.prompts import TASKS, build_prompt
from src.youtube import get_transcript


# =====================================================
# SESSION STATE
# =====================================================

def get_available_tasks():
    tasks = list(TASKS.keys())

    preferred = [
        "Study notes",
        "Organized notes",
        "PDF summary",
        "Shorter summary of source material",
        "Flashcards",
        "Questions and answers",
        "Quiz",
        "Practice questions",
        "Revision sheet",
        "Important revision points",
        "Slide outline",
        "Presentation structure",
        "Flowchart (Mermaid)",
    ]

    ordered = [task for task in preferred if task in tasks]
    ordered.extend(task for task in tasks if task not in ordered)

    return ordered


def init_state():
    defaults = {
        "source_text": "",
        "source_name": "",
        "outputs": [],
        "selected_task": None,
        "page_mode": "chat",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    tasks = get_available_tasks()

    if tasks and st.session_state.selected_task not in tasks:
        st.session_state.selected_task = tasks[0]


# =====================================================
# DOWNLOAD HELPERS
# =====================================================

def make_download_filename(task, index):
    safe_task = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        str(task)
    ).strip("_")

    if not safe_task:
        safe_task = "study_resource"

    return f"StudyFlow_{index + 1}_{safe_task}.txt"


def render_download_button(item, index, location="chat"):
    answer = str(item.get("answer", "")).strip()

    if not answer:
        st.warning("There is no response available to download.")
        return

    st.download_button(
        label="⬇ Download response",
        data=answer.encode("utf-8"),
        file_name=make_download_filename(
            item.get("task", "study_resource"),
            index
        ),
        mime="text/plain",
        key=f"{location}_download_{index}",
    )


# =====================================================
# THEME
# =====================================================

def load_styles():
    st.markdown("""
    <style>
    .stApp {
        background: #0B1020;
        color: #F3F4F6;
        font-family: Arial, sans-serif;
    }

    [data-testid="stMain"] {
        background: #0B1020;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263149;
    }

    [data-testid="stSidebar"] > div {
        background: #111827;
    }

    .brand {
        font-size: 25px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 8px;
    }

    .brand span,
    .main-title span {
        color: #A78BFA;
    }

    .tagline {
        color: #9CA3AF;
        font-size: 12px;
        margin-bottom: 25px;
    }

    .sidebar-heading {
        color: #9CA3AF;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
        margin-top: 22px;
        margin-bottom: 9px;
    }

    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        color: #F3F4F6 !important;
        border: none !important;
        box-shadow: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 8px 5px !important;
        min-height: 38px !important;
        font-size: 14px !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background: #202B3D !important;
        color: #FFFFFF !important;
    }

    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 12vh;
        margin-bottom: 12px;
    }

    .subtitle {
        text-align: center;
        color: #9CA3AF;
        font-size: 15px;
        margin-bottom: 32px;
    }

    [data-testid="stChatMessage"] {
        background: #151E30;
        border: 1px solid #29364B;
        border-radius: 13px;
        padding: 14px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        background: #111827 !important;
        border: 1px solid #39445F !important;
        border-radius: 18px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #F3F4F6 !important;
        font-size: 16px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #A1A1AA !important;
    }

    [data-testid="stChatInput"] button {
        color: #A78BFA !important;
    }

    .stButton button {
        background: #29364B;
        color: #FFFFFF;
        border: 1px solid #374151;
        border-radius: 9px;
        box-shadow: none;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #1F2937 !important;
        color: #FFFFFF !important;
        border-color: #374151 !important;
    }

    [data-testid="stExpander"] {
        background: #1F2937;
        border: 1px solid #374151;
        border-radius: 10px;
    }

    [data-testid="stDownloadButton"] button {
        background: #29364B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    [data-testid="stDownloadButton"] button:hover {
        background: #7C3AED !important;
        border-color: #7C3AED !important;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    @media (max-width: 600px) {
        .main-title {
            font-size: 28px;
            margin-top: 8vh;
        }

        .subtitle {
            font-size: 13px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =====================================================
# GREETING DETECTION
# =====================================================

def is_simple_greeting(message):
    cleaned = message.lower().strip()
    cleaned = re.sub(r"[^\w\s']", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    greetings = {
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "how are you doing",
        "what's up",
        "whats up",
        "hey there",
        "hi there",
    }

    return cleaned in greetings


# =====================================================
# GENERAL CHAT DETECTION
# =====================================================

def is_general_chat(question):
    """
    Recognize ordinary questions that should not be
    forced into a study-resource generation task.
    """

    text = question.lower().strip()

    general_starts = (
        "explain ",
        "what is ",
        "what are ",
        "who is ",
        "who was ",
        "why ",
        "how ",
        "when ",
        "where ",
        "can you explain ",
        "can you help ",
        "tell me ",
        "define ",
        "compare ",
        "difference between ",
    )

    return text.startswith(general_starts)


# =====================================================
# CHAT AND TASK GENERATION
# =====================================================

def add_pending_output(question, task, output_type="study"):
    st.session_state.outputs.append({
        "question": question,
        "answer": "",
        "task": task,
        "output_type": output_type,
        "status": "pending",
        "error": "",
    })


def generate_task(task):
    if not st.session_state.source_text.strip():
        st.warning(
            "Please upload study material or load a YouTube "
            "transcript before using this study tool."
        )
        return

    st.session_state.selected_task = task

    question = f"Create {task} from my uploaded study material."

    add_pending_output(
        question,
        task,
        output_type="study"
    )


def submit_question(question):
    if not question.strip():
        return

    question = question.strip()

    # Greetings use a local response.
    if is_simple_greeting(question):
        task = "General conversation"

        add_pending_output(
            question,
            task,
            output_type="greeting"
        )
        return

    # Ordinary questions use conversational AI.
    if is_general_chat(question):
        add_pending_output(
            question,
            "General conversation",
            output_type="general"
        )
        return

    # Other messages use the selected study task.
    task = st.session_state.selected_task

    if not task:
        tasks = get_available_tasks()

        if not tasks:
            st.error("No study tasks are configured.")
            return

        task = tasks[0]

    add_pending_output(
        question,
        task,
        output_type="study"
    )


# =====================================================
# AI RESPONSE GENERATION
# =====================================================

def generate_pending_answer(item):

    question = item["question"].strip()
    output_type = item.get("output_type", "study")

    try:

        # ---------------------------------------------
        # GREETING RESPONSE
        # ---------------------------------------------

        if output_type == "greeting":

            item["answer"] = (
                "Hi! 👋 How can I help you today?\n\n"
                "I'm StudyFlow AI, your personal study assistant. "
                "I can help you:\n\n"
                "- Explain difficult concepts\n"
                "- Answer your questions\n"
                "- Create study notes and summaries\n"
                "- Generate flashcards and quizzes\n"
                "- Prepare revision materials\n\n"
                "What would you like to learn today?"
            )

            item["status"] = "complete"
            item["error"] = ""
            return

        # ---------------------------------------------
        # GENERAL CONVERSATION
        # ---------------------------------------------

        if output_type == "general":

            system_prompt = (
                "You are StudyFlow AI, a friendly, helpful, "
                "accurate and educational AI assistant. "
                "Answer the user's actual question directly. "
                "Use natural conversational language. "
                "Do not automatically create study notes, "
                "flashcards or quizzes unless requested. "
                "Explain concepts clearly and use examples "
                "when useful. If the user asks a simple "
                "question, give a concise answer."
            )

            answer = ask_ai(
                question,
                system=system_prompt
            )

        # ---------------------------------------------
        # STUDY RESOURCE GENERATION
        # ---------------------------------------------

        else:

            source = (
                st.session_state.source_text
                or question
            )

            prompt = build_prompt(
                item["task"],
                source,
                question,
            )

            answer = ask_ai(prompt)

        if not answer or not answer.strip():
            raise RuntimeError(
                "The AI returned an empty response."
            )

        item["answer"] = answer.strip()
        item["status"] = "complete"
        item["error"] = ""

        print("STUDYFLOW AI: Response generated successfully.")

    except Exception as exc:

        print("STUDYFLOW AI ERROR:", repr(exc))

        item["status"] = "error"
        item["error"] = str(exc)


# =====================================================
# FILE PROCESSING
# =====================================================

def process_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return False

    try:
        with st.spinner("Reading your study material..."):
            text = extract_text(uploaded_file)

        if text and text.strip():
            st.session_state.source_text = text
            st.session_state.source_name = uploaded_file.name

            st.success("Study material loaded successfully.")
            return True

        st.warning("No readable text was found in this file.")
        return False

    except Exception as exc:
        print("STUDYFLOW FILE ERROR:", repr(exc))
        st.error(f"Unable to read the file: {exc}")
        return False


# =====================================================
# YOUTUBE
# =====================================================

def render_youtube_tools():
    with st.expander("YouTube lecture"):

        url = st.text_input(
            "YouTube video URL",
            key="youtube_url",
            placeholder="Paste a YouTube link",
        )

        if st.button("Load transcript", key="load_transcript"):

            if not url.strip():
                st.warning("Enter a YouTube URL first.")
                return

            try:
                with st.spinner("Loading transcript..."):
                    transcript = get_transcript(url)

                if transcript:
                    st.session_state.source_text = transcript
                    st.session_state.source_name = "YouTube transcript"

                    st.success("Transcript loaded.")

                else:
                    st.warning("No transcript was found.")

            except Exception as exc:
                print("STUDYFLOW YOUTUBE ERROR:", repr(exc))
                st.error(f"Unable to load transcript: {exc}")


# =====================================================
# SIDEBAR
# =====================================================

def start_new_chat():
    st.session_state.outputs = []
    st.session_state.page_mode = "chat"


def render_sidebar():
    tasks = get_available_tasks()

    with st.sidebar:

        st.markdown(
            '<div class="brand">StudyFlow <span>AI</span></div>'
            '<div class="tagline">Your personal study assistant</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            '<div class="sidebar-heading">WORKSPACE</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "＋  New Chat",
            key="new_chat",
            use_container_width=True,
        ):
            start_new_chat()
            st.rerun()

        if st.button(
            "⌕  Search",
            key="search_page",
            use_container_width=True,
        ):
            st.session_state.page_mode = "search"
            st.rerun()

        if st.button(
            "▤  My Library",
            key="library_page",
            use_container_width=True,
        ):
            st.session_state.page_mode = "library"
            st.rerun()

        st.markdown(
            '<div class="sidebar-heading">STUDY TOOLS</div>',
            unsafe_allow_html=True,
        )

        for task in tasks:

            if st.button(
                f"✦  {task}",
                key=f"task_{task}",
                use_container_width=True,
            ):
                generate_task(task)
                st.session_state.page_mode = "chat"
                st.rerun()

        st.markdown(
            '<div class="sidebar-heading">MORE TOOLS</div>',
            unsafe_allow_html=True,
        )

        with st.expander("Add study material"):

            sidebar_file = st.file_uploader(
                "Upload PDF, DOCX, PPTX, TXT, MD or CSV",
                type=["pdf", "docx", "pptx", "txt", "md", "csv"],
                key="sidebar_upload",
            )

            if st.button(
                "Use uploaded file",
                key="use_sidebar_file",
            ):
                process_uploaded_file(sidebar_file)

        render_youtube_tools()

        if st.session_state.source_name:

            st.caption("CURRENT SOURCE")
            st.write(st.session_state.source_name)

            if st.button("Remove source", key="remove_source"):
                st.session_state.source_text = ""
                st.session_state.source_name = ""
                st.rerun()

        st.divider()

        st.markdown(
            '<div class="sidebar-heading">CURRENT STUDY MODE</div>',
            unsafe_allow_html=True,
        )

        if tasks:

            current = st.session_state.selected_task
            index = tasks.index(current) if current in tasks else 0

            selected = st.selectbox(
                "Study mode",
                tasks,
                index=index,
                key="study_mode_select",
                label_visibility="collapsed",
            )

            st.session_state.selected_task = selected

        st.markdown(
            '<div style="color:#9CA3AF;font-size:11px;'
            'margin-top:25px;text-align:center;">'
            'StudyFlow AI'
            '</div>',
            unsafe_allow_html=True,
        )


# =====================================================
# CHAT HISTORY
# =====================================================

def render_chat_history():

    for index, item in enumerate(st.session_state.outputs):

        with st.chat_message("user"):
            st.write(item["question"])

        with st.chat_message("assistant", avatar="🎓"):

            st.caption(item["task"])

            if item["status"] == "pending":

                with st.spinner("StudyFlow AI is thinking..."):
                    generate_pending_answer(item)

            if item["status"] == "complete":

                st.markdown(item["answer"])

                render_download_button(
                    item,
                    index,
                    location="chat"
                )

                with st.expander("Copy response"):
                    st.code(
                        item["answer"],
                        language="markdown"
                    )

            elif item["status"] == "error":

                st.error(
                    "Unable to generate the response: "
                    + item.get("error", "Unknown error")
                )


# =====================================================
# MAIN CHAT PAGE
# =====================================================

def render_chat_page():

    if not st.session_state.outputs:

        st.markdown(
            '<div class="main-title">'
            'What would you like to <span>study?</span>'
            '</div>'
            '<div class="subtitle">'
            'Ask questions, attach documents and learn smarter.'
            '</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<div style="text-align:center;color:#A78BFA;'
            'font-size:20px;font-weight:600;margin-bottom:25px;">'
            'StudyFlow AI'
            '</div>',
            unsafe_allow_html=True,
        )

    render_chat_history()

    question = st.chat_input(
        "Ask anything about your studies..."
    )

    if question:
        submit_question(question)
        st.rerun()


# =====================================================
# SEARCH HISTORY
# =====================================================

def render_search_page():

    st.title("Search your study history")

    query = st.text_input(
        "Search",
        placeholder="Search previous questions and answers...",
    )

    if query.strip():

        matches = [
            item for item in st.session_state.outputs
            if (
                query.lower() in item["question"].lower()
                or query.lower() in item["answer"].lower()
            )
        ]

        if matches:

            for item in reversed(matches):

                st.markdown(f"**{item['question']}**")
                st.caption(item["task"])

                if item["status"] == "complete":
                    st.markdown(item["answer"])

                elif item["status"] == "error":
                    st.error(item["error"])

                else:
                    st.info(
                        "Response is waiting to be generated."
                    )

                st.divider()

        else:
            st.info("No matching results found.")


# =====================================================
# LIBRARY
# =====================================================

def render_library_page():

    st.title("My Library")
    st.caption(
        "Your generated study resources in this session."
    )

    completed = [
        (index, item)
        for index, item in enumerate(st.session_state.outputs)
        if item["status"] == "complete"
    ]

    if not completed:
        st.info(
            "Your generated study resources will appear here."
        )
        return

    for original_index, item in reversed(completed):

        with st.expander(item["question"]):

            st.caption(item["task"])
            st.markdown(item["answer"])

            render_download_button(
                item,
                original_index,
                location="library"
            )


# =====================================================
# APPLICATION ENTRY POINT
# =====================================================

def render_app():

    init_state()
    load_styles()
    render_sidebar()

    if not get_available_tasks():
        st.error(
            "No study tasks are configured. "
            "Check src/prompts.py."
        )
        return

    if st.session_state.page_mode == "chat":
        render_chat_page()

    elif st.session_state.page_mode == "search":
        render_search_page()

    elif st.session_state.page_mode == "library":
        render_library_page()

    else:
        st.session_state.page_mode = "chat"
        render_chat_page()
