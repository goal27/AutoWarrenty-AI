import streamlit as st
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

from services.vision_ocr import extract_text_from_image
from services.warranty_extract import extract_warranty_structured
from ui.components import header, show_warranty_details
from ui import auth
from ui.cost_estimation import render_cost_estimation_page # Import the new page
from database import database
import services.problem_analyzer # Import the problem_analyzer module
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load prompts
with open("prompts/system_warranty_agent.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

st.set_page_config(page_title="AutoWarranty AI", layout="centered")

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

header()

# Sidebar for authentication
st.sidebar.title("Authentication")
if not st.session_state['logged_in']:
    auth_option = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])
    if auth_option == "Login":
        auth.login_page()
    else:
        auth.signup_page()
else:
    st.sidebar.write(f"Welcome, {st.session_state['username']}!")
    user_details = database.get_user_details(st.session_state['user_id'])
    if user_details:
        st.sidebar.subheader("Your Info")
        st.sidebar.write(f"Email: {user_details.get('email', 'N/A')}")
        st.sidebar.write(f"Phone: {user_details.get('phone_number', 'N/A')}")
        st.sidebar.write(f"Address: {user_details.get('address', 'N/A')}")
    auth.logout_button()

    st.sidebar.subheader("Navigation")
    page_selection = st.sidebar.radio("Go to", ["Dashboard", "Cost Estimation"])

    if page_selection == "Dashboard":
        # Original dashboard content
        st.subheader("Upload New Warranty")
        uploaded_file = st.file_uploader("Upload receipt/invoice image", type=["jpg", "jpeg", "png"])
        manual_text = st.text_area("Or paste text from your invoice/receipt")

        if st.button("Extract Warranty Details"):
            if uploaded_file:
                with st.spinner("Extracting OCR from image..."):
                    ocr_text = extract_text_from_image(uploaded_file)
                    st.success("OCR extraction complete.")
                    st.text_area("Extracted Text", value=ocr_text, height=200)
                filename = uploaded_file.name
            elif manual_text:
                ocr_text = manual_text
                filename = f"manual_entry_{uuid.uuid4().hex}.txt"
            else:
                st.error("Please upload an image or paste text.")
                st.stop()

            current_date = datetime.now().strftime("%Y-%m-%d")
            with st.spinner("Analyzing warranty details..."):
                result = extract_warranty_structured(ocr_text, SYSTEM_PROMPT, current_date)

            if result:
                database.save_warranty_data(st.session_state['user_id'], filename, result)
                st.success(f"Warranty details for {filename} saved!")
                show_warranty_details(result)
            else:
                st.error("Could not extract warranty details.")

        st.subheader("Your Saved Warranties")
        user_warranties = database.get_user_warranties(st.session_state['user_id'])
        if user_warranties:
            selected_warranty_index = st.selectbox(
                "Select a saved warranty to view details:",
                options=range(len(user_warranties)),
                format_func=lambda x: user_warranties[x]['filename']
            )
            if selected_warranty_index is not None:
                selected_warranty = user_warranties[selected_warranty_index]
                with st.expander(f"Warranty for {selected_warranty['filename']}"):
                    show_warranty_details(selected_warranty['extracted_data'])
        else:
            st.info("You have no saved warranties yet.")

    elif page_selection == "Cost Estimation":
        render_cost_estimation_page()
