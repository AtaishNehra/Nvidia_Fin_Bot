import streamlit as st
import PyPDF2
from io import BytesIO
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from supabase import create_client, Client
import json

# Set up environment variables
os.environ['GROQ_API_KEY'] = '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'
supabase_url = 'https://isxykyawirffuarbmwsc.supabase.co'  # Full URL without trailing slash
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlzeHlreWF3aXJmZnVhcmJtd3NjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE0MjE3MTcsImV4cCI6MjAzNjk5NzcxN30.-dUat7yc7wb0-h5R_SmTnX29pWJNGsMxkgyzCfNImhA'  # Use the anon or service_role key

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Function to query Supabase for embeddings
def query_database_with_supabase(query):
    query_embedding = model.encode([query])[0].tolist()
    response = supabase.table('embeddings').select('*').execute()
    results = response.data
    if not results:
        return []
    # Calculate similarity and get the most relevant chunks
    similarities = [(res['filename'], res['text'], np.dot(query_embedding, np.array(json.loads(res['embedding'])))) for res in results]
    sorted_similarities = sorted(similarities, key=lambda x: x[2], reverse=True)
    return sorted_similarities[:3]

# Function to answer questions
def answer_question(query, result):
    context = result[0][1]  # Access the content of the top result
    response = chain.invoke({"query": query, "context": context})
    return response.content  # Directly access the content attribute of the AIMessage object

# Load Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up Groq LLM
chat = ChatGroq(
    temperature=0,
    model="llama3-70b-8192"
)

system = "You are a helpful assistant."
human = "{query}\\n\\n{context}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

# Streamlit UI
st.title("NVIDIA Financial Bot")

st.header("Ask a question about NVIDIA's financial data")
query = st.text_input("Enter your question")

answer = None  # Initialize answer to None
if st.button("Submit"):
    if query:
        result = query_database_with_supabase(query)
        if result:
            st.write("Top matching document:", result[0][0])
            st.write("Document context:", result[0][1])
            answer = answer_question(query, result)
            st.write("Answer:", answer)
        else:
            st.write("No relevant chunks found.")
    else:
        st.write("Please enter a question.")

st.header("Chat History")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if st.button("Clear History"):
    st.session_state['chat_history'] = []

if answer and st.button("Add to History"):
    st.session_state['chat_history'].append((query, answer))

for query, answer in st.session_state['chat_history']:
    st.write(f"**Question:** {query}")
    st.write(f"**Answer:** {answer}")
    st.write("---")
