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

# Load environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    model="llama3-70b-8192",
    api_key=GROQ_API_KEY  # Use environment variable
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
