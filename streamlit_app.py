# KPR Smart Fabrication AI (High-End Vendor-Friendly Version)
# Author: Srihitha | AI/ML Portfolio Project
# Description: Suggests relevant sheet metal fabrication products based on input using GPT-3.5

import streamlit as st
import openai

# Replace with your OpenAI free-tier key
openai.api_key = "your-api-key"

# UI Setup
st.set_page_config(page_title="KPR AI Assistant", layout="centered")
st.title("KPR Smart Fabrication AI")
st.markdown("""
This assistant helps clients and vendors discover what can be built using our laser cutting and fabrication machines.
You can speak naturally or fill the inputs below.
""")

# Input option: Toggle between manual or natural language
input_mode = st.radio("Choose how you'd like to describe your need:", ["Simple Dropdown", "Natural Language"])

# Mode 1: Simple dropdown-based input (for non-tech vendors)
if input_mode == "Simple Dropdown":
    industry = st.selectbox("Client Industry", ["Pharma", "Retail", "Automotive", "Defense", "Railways", "General"])
    material = st.selectbox("Material Type", ["Mild Steel", "Stainless Steel", "Aluminium", "Copper"])
    work_type = st.selectbox("Work Type", ["Laser Cutting", "Cutting", "Bending", "Welding", "Powder Coating"])

    # Prompt built from structured values
    prompt = f"""
You are a smart assistant for a metal fabrication company. The client is from the {industry} industry.
They want to use {material} and require {work_type}.
Suggest 6 sheet metal products relevant only to this industry. Format as a clean list with brief descriptions.
"""

# Mode 2: Freeform natural language (for speaking-style queries)
else:
    user_query = st.text_area("Describe what you need (e.g., 'We need racks for a pharma lab')", max_chars=300)
    prompt = f"""
You are a helpful fabrication AI. A client says: "{user_query}"
Analyze the request and suggest 4–6 products they can fabricate using a laser cutting/bending setup.
Be clear, polite, and tailor suggestions to the client's needs. Avoid jargon.
"""

# GPT Call Function
def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're an assistant for a sheet metal fabrication company."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7
    )
    return response.choices[0].message.content
st.title("FabGenie – Your Smart Fabrication Assistant")
st.markdown("FabGenie helps you figure out what to build using your material, machine, and industry. Just ask.")


# Trigger button
if st.button("Suggest Products"):
    try:
        result = ask_gpt(prompt)
        st.subheader("Recommended Products:")
        st.markdown(result)
    except Exception as e:
        st.error("There was an error generating suggestions. Check API key or network.")
