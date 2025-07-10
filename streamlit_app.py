import streamlit as st
import requests
import os

# ✅ Model known to work with free API
HF_MODEL = "google/flan-t5-base"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# ✅ Load your Hugging Face token from secrets
HF_API_KEY = os.getenv("HF_API_KEY")

# 🔁 Query function
def query_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = { 
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"].strip()
        except:
            return "⚠️ Could not parse model response."
    elif response.status_code == 401:
        return "🔐 Invalid Hugging Face API key."
    elif response.status_code == 404:
        return "❌ Model not found or not available via API."
    elif response.status_code == 503:
        return "⏳ Model is loading. Try again shortly."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Streamlit UI
st.set_page_config(page_title="FabGenie – KPR AI Assistant")
st.title("FabGenie – Your Smart Fabrication Assistant")
st.markdown("FabGenie helps you decide what to build using your materials and machines.")

input_mode = st.radio("How would you like to describe your need?", ["Simple Dropdown", "Natural Language"])

if input_mode == "Simple Dropdown":
    industry = st.selectbox("Client Industry", ["Pharma", "Retail", "Automotive", "Defense", "Railways", "General"])
    material = st.selectbox("Material Type", ["Mild Steel", "Stainless Steel", "Aluminium", "Copper"])
    work_type = st.selectbox("Work Type", ["Laser Cutting", "Cutting", "Bending", "Welding", "Powder Coating"])
    
    prompt = f"""
Suggest 5 metal fabrication products using {material} and {work_type} for a client in the {industry} industry.
Only suggest relevant and practical items.
"""

else:
    user_query = st.text_area("Describe your requirement")
    prompt = f"""
A client says: "{user_query}"
Suggest 4–6 relevant fabrication items that can be made using laser cutting and sheet metal.
Use simple, non-technical language.
"""

if st.button("Suggest Products"):
    st.subheader("Recommended Fabrication Ideas:")
    output = query_huggingface(prompt)
    st.markdown(output)
