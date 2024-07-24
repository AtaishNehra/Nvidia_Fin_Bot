# NVIDIA Financial Bot

This project is a Streamlit application that answers questions about NVIDIA's financial data using a pre-built database of financial documents stored in Supabase and leveraging Groq's language model for processing queries.

## Features
- Query NVIDIA financial documents.
- Retrieve relevant document excerpts.
- Provide detailed answers based on the content of the documents.

## Setup Instructions

### Prerequisites

1. **Git**: Ensure you have Git installed. [Download Git](https://git-scm.com/downloads)
2. **Python**: Ensure you have Python 3.7 or later installed. [Download Python](https://www.python.org/downloads/)

### Clone the Repository

```bash
git clone https://github.com/your-username/nvidia-financial-bot.git
cd nvidia-financial-bot
```

## Create API Keys and URLs

### Groq API Key
- Sign up at [Groq](https://groq.com/) and generate an API key.

### Supabase
- Sign up at [Supabase](https://supabase.com/) and create a new project.
- Note down your Supabase URL and API Key.
- Create a table named `embeddings` with columns `filename`, `text`, and `embedding`.

### Ngrok
- Sign up at [Ngrok](https://ngrok.com/) and get your auth token.

## Add Secrets to Streamlit

### Create `.streamlit` Directory
```bash
mkdir .streamlit
```

### Create secrets.toml
```bash
nano .streamlit/secrets.toml
```
#### Add the following content:
GROQ_API_KEY = "your-groq-api-key" </br>
SUPABASE_URL = "your-supabase-url" </br>
SUPABASE_KEY = "your-supabase-key" </br>
NGROK_AUTH_TOKEN = "your-ngrok-auth-token" </br>

## Install Dependencies 

### Create a requirements.txt file with the following content:

streamlit </br>
PyPDF2 </br>
sentence-transformers </br>
supabase </br>
langchain-core </br>
langchain-groq </br>

### Install the dependencies:
```bash
pip install -r requirements.txt
```

## Run the Application
```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
### Sign Up and Log In
- Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign up or log in. </br>

## New Deployment
- Click on "New app" in the dashboard.
- Connect to your GitHub repository.
- Select the branch and file (app.py).

### Add Secrets
- In the "Advanced Settings" section, click on "Manage Secrets".
- Add your secrets in the format:
