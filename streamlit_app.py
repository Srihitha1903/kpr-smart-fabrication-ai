# FabGenie – KPR Smart Fabrication AI using Hugging Face (Free, No Billing)
# Author: Srihitha | GenAI Engineer (MSME Project)

import streamlit as st
import requests
import os

# Load Hugging Face API key securely from Streamlit secrets
HF_API_KEY = os.getenv("HF_API_KEY")

# Select free Hugging Face model — Zephyr is chat-optimized and available via free Inference API
HF_MODEL = "tiiuae/falcon-7b-instruct"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
# Function to call the Hugging Face API
def query_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.7}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"].strip()
            else:
                return "⚠️ No valid response from model."
        except Exception as e:
            return f"⚠️ Failed to parse output: {str(e)}"
    elif response.status_code == 401:
        return "🔐 Invalid Hugging Face API key."
    elif response.status_code == 503:
        return "⏳ Model is loading. Try again in a few seconds."
    else:
        return f"❌ API Error {response.status_code}: {response.text}"

# Streamlit app UI setup
st.set_page_config(page_title="FabGenie – KPR AI Assistant", layout="centered")
st.title("FabGenie – Your Smart Fabrication Assistant")
st.markdown("""
FabGenie helps you figure out what to build using your material, machines, and client industry.

You can either fill in dropdowns or speak in simple natural language.
""")

# Choose input mode
input_mode = st.radio("Choose how you'd like to describe your need:", ["Simple Dropdown", "Natural Language"])

# ---- MODE 1: STRUCTURED DROPDOWNS (FOR VENDORS) ----
if input_mode == "Simple Dropdown":
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
    user_query = st.text_area("Describe what you need (e.g., 'We need racks for a pharma lab')", max_chars=300)
    prompt = f"""
You are a helpful AI assistant for a metal fabrication company.
A client says: "{user_query}"
Interpret the request and suggest 4–6 relevant sheet metal products they could fabricate using laser cutting and bending.
Explain clearly, using simple language without industry jargon.
"""

# ---- GPT TRIGGER ----
if st.button("Suggest Products"):
    st.subheader("Recommended Fabrication Ideas:")
    try:
        result = query_huggingface(prompt)
        st.markdown(result)
    except Exception as e:
        st.error("Something went wrong. Check API key or model availability.")
