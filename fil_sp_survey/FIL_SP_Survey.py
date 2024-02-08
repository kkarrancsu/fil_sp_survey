import streamlit as st

st.set_page_config(
    page_title="Introduction",
    page_icon="👋",
    layout="wide",
)

st.markdown("[![CryptoEconLab](./app/static/cover.png)](https://cryptoeconlab.io)")

st.sidebar.success("Select a Page above.")

st.markdown(
"""
### Filecoin SP Survey

The following is an anonymous survey to help understand costs and revenues as a storage provider. Responses will be summarized to provide insights into Storage-Provider microeconomics.

Please select a page based on your preferred language from the sidebar 👈 to begin the survey. All fields are optional. Thank you for your time!
"""
)