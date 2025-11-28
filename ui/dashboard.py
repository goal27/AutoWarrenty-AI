import streamlit as st
from .components import show_warranty_details

def render_dashboard(data):
    st.subheader("Extracted Warranty Details")
    show_warranty_details(data)
