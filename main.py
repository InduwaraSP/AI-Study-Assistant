import streamlit as st
import os
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(page_title="NoteLux PDF to Summary", page_icon="🎓", layout="wide")
st.title("🎓 NoteLux PDF to Summary")

# --- INITIALIZE GROQ ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- PDF PROCESSING ---
def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.header("📂 Setup")
    uploaded_file = st.file_uploader("Upload your lecture notes", type="pdf")
    
    st.divider()
    st.header("⚡ Quick Actions")
    
    # Buttons for Phase 2 features
    gen_summary = st.button("📑 Generate Summary")
    gen_flashcards = st.button("🎴 Make Flashcards")
    gen_quiz = st.button("📝 Take a Quiz")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLING BUTTON ACTIONS ---
if uploaded_file:
    context = get_pdf_text(uploaded_file)
    action_prompt = None

    if gen_summary:
        action_prompt = "Provide a structured one-page summary of these notes using bullet points and bold headings."
    elif gen_flashcards:
        action_prompt = "Generate 5 high-quality flashcards (Front/Back format) from these notes."
    elif gen_quiz:
        action_prompt = "Generate a 3-question multiple-choice quiz based on these notes. Give answers at the end."

    if action_prompt:
        with st.chat_message("user"):
            st.markdown(f"**Running Action:** {user_input if 'user_input' in locals() else action_prompt}")
        
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Context: {context[:15000]}"},
                          {"role": "user", "content": action_prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# --- NORMAL CHAT INPUT ---
if prompt := st.chat_input("Ask a specific question..."):
    if not uploaded_file:
        st.error("Please upload a PDF first!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            context = get_pdf_text(uploaded_file)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Use these notes: {context[:15000]}"},
                          {"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})