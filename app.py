import streamlit as st
from main import run_live_analysis # Your File 6 logic
from Services.config_loader import get_config

# 1. Page Configuration
st.set_page_config(page_title="AI Stock Assistant", page_icon="📈")

# 2. Sidebar - Portfolio & Controls
with st.sidebar:
    st.title("My Portfolio 💼")
    ticker = st.text_input("Enter Ticker to Analyze", value="NVDA").upper()
    if st.button("Run AI Analysis"):
        with st.spinner("Gemini is thinking..."):
            # We'll call your existing logic here
            result = run_live_analysis(ticker)
            st.success("Analysis Complete!")

# 3. Main Chat Interface
st.title("💬 Chat with your Stock Bot")

# Initialize chat history (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. React to user input
if prompt := st.chat_input("What's on your mind?"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        # For now, we connect it to your analysis logic
        response = f"I've analyzed {ticker}. Check the sidebar for the full report!"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})