import streamlit as st
from PIL import Image
from io import BytesIO
import textwrap
import json

from graph.final_graph import build_story_graph
from audio.narration import narrate_story

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="TaleForge",
    page_icon="📖",
    layout="wide"
)

graph = build_story_graph()


# --------------------------------------------------
# THEME ENGINE
# --------------------------------------------------

def apply_genre_theme(genre):

    themes = {
        "Comedy": {"bg": "#FFF7E6", "text": "#2B2B2B", "accent": "#FF9800"},
        "Thriller": {"bg": "#0F172A", "text": "#F8FAFC", "accent": "#EF4444"},
        "Fairy Tale": {"bg": "#FDF4FF", "text": "#3B0764", "accent": "#C084FC"},
        "Mythological": {"bg": "#FFF8E1", "text": "#3E2723", "accent": "#D4AF37"},
        "Sci-Fi": {"bg": "#020617", "text": "#E0F2FE", "accent": "#22D3EE"},
        "Mystery": {"bg": "#111827", "text": "#E5E7EB", "accent": "#A855F7"},
        "Adventure": {"bg": "#ECFDF5", "text": "#064E3B", "accent": "#10B981"},
        "Romantic": {"bg": "#FFF1F2", "text": "#831843", "accent": "#FB7185"},
        "Horror": {"bg": "#020617", "text": "#FCA5A5", "accent": "#DC2626"},
        "Morale": {"bg": "#F0FDF4", "text": "#14532D", "accent": "#22C55E"},
    }

    t = themes.get(genre, themes["Comedy"])

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-color: {t['bg']} !important;
        }}

        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] span,
        [data-testid="stAppViewContainer"] div {{
            color: {t['text']} !important;
        }}

        h1,h2,h3,h4 {{
            color: {t['accent']} !important;
        }}

        section[data-testid="stSidebar"] {{
            background:#0f172a;
        }}

        section[data-testid="stSidebar"] * {{
            color:white !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# UI ANIMATIONS
# --------------------------------------------------

st.markdown("""
<style>

.pipeline-card{
padding:14px;
border-radius:12px;
margin-bottom:10px;
background:rgba(0,0,0,0.05);
border-left:5px solid #f59e0b;
font-size:16px;
display:flex;
align-items:center;
gap:10px;
animation:fadein 0.4s ease;
}

.pipeline-done{
border-left:5px solid #22c55e;
}

.pipeline-running{
border-left:5px solid #3b82f6;
}

@keyframes fadein{
from{opacity:0; transform:translateY(10px)}
to{opacity:1; transform:translateY(0)}
}

.float-header{
animation:float 3s ease-in-out infinite;
}

@keyframes float{
0%{transform:translateY(0px)}
50%{transform:translateY(-6px)}
100%{transform:translateY(0px)}
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
"""
<h1 style='text-align:center;'>📖 TaleForge</h1>
<p style='text-align:center;'>Where Images Turn Into Stories ✨</p>
""",
unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    uploaded_files = st.file_uploader(
        "📷 Upload Images",
        type=["jpg","jpeg","png"],
        accept_multiple_files=True
    )

    genre = st.selectbox(
        "🎭 Genre",
        ["Comedy","Thriller","Fairy Tale","Mythological","Sci-Fi","Mystery","Adventure","Romantic","Horror","Morale"]
    )

    language = st.selectbox(
        "🌍 Language",
        ["English","Hindi","Spanish","French","German"]
    )

    length = st.selectbox(
        "📚 Story Length",
        ["Short","Medium","Long"]
    )

    generate = st.button("✨ Generate Story", use_container_width=True)

apply_genre_theme(genre)


# --------------------------------------------------
# IMAGE PREVIEW
# --------------------------------------------------

images = []

if uploaded_files:

    st.markdown(
        "<h2 class='float-header'>🖼 Uploaded Images</h2>",
        unsafe_allow_html=True
    )

    cols = st.columns(len(uploaded_files))

    for i, f in enumerate(uploaded_files):

        img = Image.open(f)
        images.append(img)

        cols[i].image(img, use_container_width=True)


# --------------------------------------------------
# PDF GENERATOR
# --------------------------------------------------

def generate_pdf(title, genre, story, images):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(width/2, height-120, title)

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width/2, height-170, f"Genre: {genre}")

    pdf.showPage()

    for img in images:

        img_io = BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)

        pdf.drawImage(
            ImageReader(img_io),
            50,150,
            width=width-100,
            height=height-250,
            preserveAspectRatio=True
        )

        pdf.showPage()

    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(50, height-50)

    for para in story.split("\n"):

        lines = textwrap.wrap(para, 90)

        for line in lines:

            if text.getY() < 50:
                pdf.drawText(text)
                pdf.showPage()
                text = pdf.beginText(50, height-50)

            text.textLine(line)

        text.textLine("")

    pdf.drawText(text)
    pdf.save()

    buffer.seek(0)

    return buffer


# --------------------------------------------------
# STORY GENERATION
# --------------------------------------------------

if generate:

    if not images:
        st.warning("Please upload images first.")
        st.stop()

    state = {
        "images": images,
        "genre": genre,
        "language": language,
        "story_length": length,

        "vision_descriptions": [],
        "structured_scenes": [],
        "story_outline": {},
        "generated_story": "",
        "critique_feedback": None,
        "critique_rating": None,
        "critique_decision": None,
        "final_story": None
    }

    st.subheader("🤖 AI Agent Pipeline")

    vision_box = st.empty()
    scene_box = st.empty()
    planner_box = st.empty()
    generator_box = st.empty()
    critic_box = st.empty()

    progress = st.progress(0)

    def running(box, text):
        box.markdown(
            f"<div class='pipeline-card pipeline-running'>🌀 {text}</div>",
            unsafe_allow_html=True
        )

    def done(box, text):
        box.markdown(
            f"<div class='pipeline-card pipeline-done'>✅ {text}</div>",
            unsafe_allow_html=True
        )

    running(vision_box, "Vision Agent analyzing images")
    running(scene_box, "Scene Extraction Agent structuring scenes")
    running(planner_box, "Story Planner creating narrative structure")
    running(generator_box, "Story Generator writing the story")
    running(critic_box, "Critic Agent reviewing story")

    result = None

    for step in graph.stream(state):

        node = list(step.keys())[0]
        node_state = step[node]

        if node == "vision_agent":
            done(vision_box, "Vision Agent completed")
            progress.progress(20)

        elif node == "scene_extractor_agent":
            done(scene_box, "Scene Extraction completed")
            progress.progress(40)

        elif node == "story_planner_agent":
            done(planner_box, "Story Plan generated")
            progress.progress(60)

        elif node == "story_generator_agent":
            done(generator_box, "Story generated")
            progress.progress(80)

        elif node == "critic_agent":
            done(critic_box, "Critic approved story")
            progress.progress(100)
            result = node_state

    if result is None:
        result = node_state

    story = result["final_story"]
    rating = result["critique_rating"]
    feedback = result["critique_feedback"]


    st.subheader("📜 Your Story")
    st.write(story)


    st.subheader("🧠 Critic Evaluation")

    col1, col2 = st.columns(2)
    col1.metric("Story Rating", f"{rating}/10")
    col2.info(feedback)


    st.subheader("🔊 Narration")

    audio = narrate_story(story, language)
    st.audio(audio, format="audio/mp3")


    pdf = generate_pdf("TaleForge Story", genre, story, images)

    st.download_button(
        "📄 Download Story as PDF",
        pdf,
        file_name="TaleForge_story.pdf",
        mime="application/pdf"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
"<center>✨ Built with ❤️ using LangGraph + Streamlit · TaleForge © 2025</center>",
unsafe_allow_html=True
)