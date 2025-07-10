# FabGenie – KPR Smart Fabrication AI using Hugging Face (Free, No Billing)
# Author: Srihitha | GenAI Engineer (MSME Project)

# Import required libraries
import streamlit as st
import requests  # Used to call Hugging Face model via REST API

# Load Hugging Face API key securely from Streamlit secrets
HF_API_KEY = st.secrets["HF_API_KEY"]

# Select free Hugging Face model — Zephyr is a conversational, chat-optimized model
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# Define a function to call the Hugging Face API
def query_huggingface(prompt):
    # Authorization and payload setup
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,     # Limit response length
            "temperature": 0.7         # Creativity of output
        }
    }

    # Send POST request to Hugging Face model endpoint
    response = requests.post(API_URL, headers=headers, json=payload)

    # Return the generated text, removing the original prompt from the start
    if response.status_code == 200:
        return response.json()[0]["generated_text"][len(prompt):].strip()
    else:
        return "Error generating response. Check your Hugging Face key or model availability."

# Streamlit app UI setup
st.set_page_config(page_title="FabGenie – KPR AI Assistant", layout="centered")
st.title("FabGenie – Your Smart Fabrication Assistant")
st.markdown(
    "FabGenie helps you figure out what to build using your material, machines, and client industry. "
    "You can either fill in dropdowns or speak in simple natural language."
)

# Choose input mode (dropdown for vendors / natural language for internal staff)
input_mode = st.radio("Choose how you'd like to describe your need:", ["Simple Dropdown", "Natural Language"])

# ---- MODE 1: STRUCTURED DROPDOWNS (FOR VENDORS) ----
if input_mode == "Simple Dropdown":
    # Dropdown selections
    industry = st.selectbox("Client Industry", ["Pharma", "Retail", "Automotive", "Defense", "Railways", "General"])
    material = st.selectbox("Material Type", ["Mild Steel", "Stainless Steel", "Aluminium", "Copper"])
    work_type = st.selectbox("Work Type", ["Laser Cutting", "Cutting", "Bending", "Welding", "Powder Coating"])

    # Prompt for Hugging Face model
    prompt = f"""
You are a smart assistant for a sheet metal fabrication company. 
The client is from the {industry} industry and wants to use {material} for {work_type}. 
Suggest 6 fabrication products relevant only to the {industry} domain. 
Format them as a numbered list with short descriptions.
"""

# ---- MODE 2: NATURAL LANGUAGE (FOR INTERNAL STAFF) ----
else:
    # Freeform user input
    user_query = st.text_area("Describe what you need (e.g., 'We need racks for a pharma lab')", max_chars=300)
    
    # Prompt built dynamically
    prompt = f"""
You are a helpful AI assistant for a metal fabrication company.
A client says: "{user_query}"
Interpret the request and suggest 4–6 relevant sheet metal products they could fabricate using laser cutting and bending.
Explain clearly, using simple language without industry jargon.
"""

# ---- GPT TRIGGER ----
# Button click: trigger Hugging Face response generation
if st.button("Suggest Products"):
    st.subheader("Recommended Fabrication Ideas:")
    try:
        result = query_huggingface(prompt)
        st.markdown(result)
    except Exception as e:
        st.error("Something went wrong. Check API key or model availability.")
