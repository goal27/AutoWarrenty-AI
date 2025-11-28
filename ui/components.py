import streamlit as st

def header():
    st.markdown("<h1 style='text-align:center;'>📦 AutoWarranty AI</h1>", unsafe_allow_html=True)
    st.write("Upload your receipt (image) or paste text to auto-extract warranty details.")

def show_json_pretty(data):
    import json
    st.json(data)

def show_warranty_details(data):
    if not data:
        st.info("No warranty details extracted yet.")
        return

    st.markdown("---")
    for category, details in data.items():
        if category == "Summary":
            st.subheader(f"{category.title()}")
            for key, value in details.items():
                if key != "confidence":
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.subheader(f"{category.title()} Details")
            for key, value in details.items():
                if key != "confidence":
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    st.markdown("---")
