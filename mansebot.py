import openai
from openai import OpenAI
import streamlit as st

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI()

st.title("ManseBot")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Mitäs sulla on miälessä?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "system", "content": "Tampere on ehdoton lempikaupunkisi. Vastaat vahvalla tampereen murteella. Korvaa pilkkuja sanalla 'nääs'. Käytä muun tekstin seassa sanontoja 'Kyä näin o!' sekä 'Ny rillataan!'. Lempiruokaasi on mustamakkara. Lempijääkiekkojoukkueesi on Tappara. Ilves-niminen jääkiekkojoukkue on tosi huono. Hattu on pipa."})
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with st.spinner('Ootas kummää miätin...'):
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True):
                if response.choices[0].delta.role != "system":
                    content = response.choices[0].delta.content
                    if content is not None:
                        full_response += content
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
