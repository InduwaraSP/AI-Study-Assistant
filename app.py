import os
from groq import Groq
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

history = [] 
pdf_file = "notes.pdf"
document_content = extract_text_from_pdf(pdf_file)

system_message = f"You are a study assistant for a CS student. Use these notes: {document_content[:10000]}"
history.append({"role": "system", "content": system_message})

print("🚀 Phase 2: All Core Features Active!")
print("👉 Type normally to Chat")
print("👉 '/flashcards' for Study Cards")
print("👉 '/quiz' for Multiple Choice Questions")
print("👉 '/summary' for a One-Page Overview")
print("👉 'exit' to quit")

while True:
    user_input = input("\n🎓 You: ")
    
    if user_input.lower() == "exit":
        break
    
    # --- COMMAND LOGIC ---
    if user_input.lower() == "/flashcards":
        prompt = "Generate 5 flashcards (Front/Back format) from these notes."
        print("\n🎴 Generating Flashcards...")
    elif user_input.lower() == "/quiz":
        prompt = "Generate a 3-question multiple-choice quiz based on these notes. Provide the answers at the very end."
        print("\n📝 Generating Quiz...")
    elif user_input.lower() == "/summary":
        prompt = "Provide a structured one-page summary of these notes using bullet points and bold headings."
        print("\n📑 Generating Summary...")
    else:
        prompt = user_input

    history.append({"role": "user", "content": prompt})
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history 
    )
    
    ai_response = completion.choices[0].message.content
    print(f"\n🤖 AI: {ai_response}")
    history.append({"role": "assistant", "content": ai_response})