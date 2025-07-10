import streamlit as st
import requests
import os

# Model info
HF_MODEL = "HF_MODEL = "google/flan-t5-large"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_API_KEY = os.getenv("HF_API_KEY")

# Function to query Hugging Face
def query_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            result = response.json()
            return result[0]["generated_text"].strip()
        except:
            return "⚠️ Could not parse response."
    elif response.status_code == 404:
        return "❌ Model not found or not available via API."
    elif response.status_code == 401:
        return "🔐 Invalid API key."
    elif response.status_code == 503:
        return "⏳ Model is loading. Try again shortly."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Streamlit UI
st.set_page_config(page_title="FabGenie – KPR AI Assistant")
st.title("FabGenie – Your Smart Fabrication Assistant")
st.markdown("Enter fabrication requirements using dropdowns or natural language.")

input_mode = st.radio("Select Input Type", ["Simple Dropdown", "Natural Language"])

if input_mode == "Simple Dropdown":
    industry = st.selectbox("Client Industry", ["Pharma", "Retail", "Automotive", "Defense", "Railways", "General"])
    material = st.selectbox("Material Type", ["Mild Steel", "Stainless Steel", "Aluminium", "Copper"])
    work_type = st.selectbox("Work Type", ["Laser Cutting", "Cutting", "Bending", "Welding", "Powder Coating"])

    prompt = f"""
You are a smart assistant for a metal fabrication company.
The client is in the {industry} industry, using {material} for {work_type}.
Suggest 5 sheet metal products for this domain.
"""
else:
    user_query = st.text_area("Describe your requirement (e.g., racks for a pharma lab)")
    prompt = f"""
You are a helpful AI assistant for a fabrication company.
A client says: "{user_query}"
Suggest 4–6 suitable products that can be fabricated using laser cutting.
"""

if st.button("Suggest Products"):
    st.subheader("Recommended Fabrication Ideas:")
    response = query_huggingface(prompt)
    st.markdown(response)
