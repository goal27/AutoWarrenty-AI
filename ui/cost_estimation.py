import streamlit as st
import services.problem_analyzer
from database import database # Assuming database is needed for warranty data
from ui.components import show_warranty_details # Assuming this component is useful

def render_cost_estimation_page():
    st.title("Warranty Coverage & Cost Estimation")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.info("Please login to access this feature.")
        return

    user_id = st.session_state['user_id']
    user_warranties = database.get_user_warranties(user_id)

    if user_warranties:
        st.subheader("Your Saved Warranties")
        selected_warranty_index = st.selectbox(
            "Select a saved warranty to analyze a problem:",
            options=range(len(user_warranties)),
            format_func=lambda x: user_warranties[x]['filename']
        )

        if selected_warranty_index is not None:
            selected_warranty = user_warranties[selected_warranty_index]
            st.subheader(f"Analyze Problem for {selected_warranty['filename']}")
            problem_description = st.text_area("Describe the problem you are experiencing:")

            if st.button("Analyze Problem"):
                if problem_description:
                    with st.spinner("Analyzing problem and warranty coverage..."):
                        analysis_result = services.problem_analyzer.analyze_problem_with_warranty(
                            problem_description,
                            selected_warranty['extracted_data']
                        )
                    if analysis_result:
                        st.write(f"**Coverage Status:** {analysis_result.get('coverage_status')}")
                        st.write(f"**Estimated Repair Cost:** {analysis_result.get('estimated_repair_cost')}")
                        st.write(f"**Reasoning:** {analysis_result.get('reasoning')}")
                        st.write(f"**Cost Explanation:** {analysis_result.get('cost_explanation')}")
                    else:
                        st.error("Failed to analyze the problem. Please try again.")
                else:
                    st.warning("Please describe the problem to analyze.")

            with st.expander(f"View Details for {selected_warranty['filename']}"):
                show_warranty_details(selected_warranty['extracted_data'])
    else:
        st.info("You have no saved warranties yet. Upload a new warranty on the Dashboard.")
