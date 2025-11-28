import streamlit as st
from database import database

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id = database.verify_user(username, password)
        if user_id:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['user_id'] = user_id
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def signup_page():
    st.title("Sign Up")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_email = st.text_input("Email (Optional)")
    new_phone_number = st.text_input("Phone Number (Optional)")
    new_address = st.text_area("Address (Optional)")

    if st.button("Sign Up"):
        if database.add_user_details(new_username, new_password, new_email, new_phone_number, new_address):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists. Please choose a different one.")

def logout_button():
    if st.session_state.get('logged_in'):
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.session_state['user_id'] = None
            st.rerun()
