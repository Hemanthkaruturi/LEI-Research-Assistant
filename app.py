"""
LEI Research Assistant - Streamlit Frontend
A web application to find and verify Legal Entity Identifiers (LEI).
"""

import os
import streamlit as st
from backend.lei_lookup import LEILookup


def main():
    """Main Streamlit application."""

    # Page configuration
    st.set_page_config(
        page_title="LEI Research Assistant",
        page_icon="🔍",
        layout="centered"
    )

    # Title and description
    st.title("🔍 LEI Research Assistant")
    st.markdown(
        "Find and verify Legal Entity Identifiers (LEI) for companies using "
        "GLEIF data and AI-powered verification."
    )
    st.markdown("---")

    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error(
            "⚠️ GEMINI_API_KEY environment variable not set. "
            "Please configure your API key to use this application."
        )
        st.info(
            "💡 To set up:\n"
            "1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)\n"
            "2. Create a `.env` file with `GEMINI_API_KEY=your_key_here`\n"
            "3. Restart the application"
        )
        return

    # Initialize LEI lookup service
    if "lei_lookup" not in st.session_state:
        st.session_state.lei_lookup = LEILookup(api_key)

    # Search form
    st.subheader("Search for LEI")

    with st.form("search_form"):
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Google",
            help="Enter the name of the company you want to search for"
        )

        website = st.text_input(
            "Website / Domain",
            placeholder="e.g., google.com",
            help="Enter the company's website or domain (accuracy is important for verification)"
        )

        submit_button = st.form_submit_button(
            "🔍 Search LEI",
            use_container_width=True
        )

    # Handle form submission
    if submit_button:
        if not company_name or not website:
            st.warning("⚠️ Please fill in both Company Name and Website fields.")
            return

        # Show loading state
        with st.spinner("🔄 Researching... this may take a moment"):
            result = st.session_state.lei_lookup.find_lei(company_name, website)

        # Display results
        st.markdown("---")

        if result["success"]:
            # Success - display LEI information
            st.success("✅ LEI Found and Verified!")

            # LEI Code (prominent display)
            st.markdown("### LEI Code")
            st.code(result["lei"], language=None)

            # Legal Name
            st.markdown("### Verified Legal Name")
            st.write(result["legal_name"])

            # Address
            if result.get("address"):
                st.markdown("### 🏢 Legal Address")
                st.write(result["address"])

            # Sources
            if result.get("sources"):
                st.markdown("### 🔗 Verification Sources")
                for idx, source in enumerate(result["sources"], 1):
                    title = source.get("title", "Source")
                    url = source.get("url", "")
                    if url:
                        st.markdown(f"{idx}. [{title}]({url})")

            # Cost
            if result.get("estimated_cost") is not None:
                st.markdown("### 💰 Estimated API Cost")
                st.write(f"${result['estimated_cost']:.6f} USD")

        else:
            # Error or no match found
            st.info(f"ℹ️ {result.get('message', 'No LEI found')}")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
        "Data from <a href='https://www.gleif.org/' target='_blank'>GLEIF</a> | "
        "Powered by <a href='https://ai.google.dev/' target='_blank'>Google Gemini</a>"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
