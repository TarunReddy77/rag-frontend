import streamlit as st
import requests

BACKEND_URL = "https://your-backend.onrender.com"  # Replace with your deployed backend URL

st.title("🧠 RAG Assistant")

# Upload section
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "md", "html"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    try:
        response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        if response.status_code == 200:
            st.success(f"File sent to backend: {response.json().get('filename')}")
        else:
            st.error("❌ Failed to upload file to backend")
    except Exception as e:
        st.error(f"⚠️ Error connecting to backend: {e}")

# Q&A section
question = st.text_input("Ask a question about your document:")

if st.button("Get Answer") and question:
    try:
        res = requests.post(f"{BACKEND_URL}/ask/", json={"question": question})
        if res.status_code == 200:
            st.markdown(f"💬 **Answer:** {res.json().get('answer')}")
        else:
            st.error("❌ Failed to get an answer from backend.")
    except Exception as e:
        st.error(f"⚠️ Error contacting backend: {e}")
