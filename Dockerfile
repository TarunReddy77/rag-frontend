# Step 1: Use the same official Python base image
FROM python:3.11-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy your application code
COPY . .

# Step 5: Expose Streamlit's default port
# Streamlit runs on port 8501 by default
EXPOSE 8501

# Step 6: Define the command to run your Streamlit application
# Replace "app.py" if your main Streamlit file has a different name
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]