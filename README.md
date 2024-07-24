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
GROQ_API_KEY = "your-groq-api-key" <\br>
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
NGROK_AUTH_TOKEN = "your-ngrok-auth-token"

