import streamlit as st
import requests
import os

# Read the backend URL from an environment variable.
# If the variable is not set, default to the local address for testing.
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/")

# Wake up the backend (especially for Render free tier)
try:
    requests.get(f"{BACKEND_URL}/ping", timeout=5)
    st.info("✅ Backend is awake!")
except Exception:
    # Use a more specific message for localhost
    if "127.0.0.1" in BACKEND_URL:
        st.warning("⚠️ Cannot connect to local backend. Is it running?")
    else:
        st.warning("⚠️ Backend might be sleeping, please retry shortly.")

st.title("🧠 RAG Assistant")

# File Upload Section
uploaded_file = st.file_uploader("📄 Upload a document", type=["pdf", "txt", "md", "html"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    try:
        response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        if response.status_code == 200:
            st.success(f"✅ File parsed: {response.json().get('filename')}")
        else:
            st.error("❌ Upload failed.")
    except Exception as e:
        st.error(f"⚠️ Error uploading file: {e}")

# Q&A Section
st.markdown("---")
question = st.text_input("💬 Ask a question about the document:")

if st.button("Get Answer") and question:
    try:
        # FIX: backend expects "query" not "question"
        res = requests.post(f"{BACKEND_URL}/ask/", json={"query": question})
        if res.status_code == 200:
            st.markdown(f"🧠 **Answer:** {res.json().get('answer')}")
        else:
            st.error("❌ Backend returned an error.")
    except Exception as e:
        st.error(f"⚠️ Error contacting backend: {e}")
