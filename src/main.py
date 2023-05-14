import os

import openai
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_text():
    """Input text by the user"""
    input_text = st.text_input(
        "Ask me your question. Answers will be limited to 256 tokens", "", key="input"
    )
    return input_text


def generate_response_chat(messages):
    """Generate Reponse using GPT3.5 API"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301", messages=messages, max_tokens=256, temperature=0
    )
    return response["choices"][0]["message"]


def chatbot():
    """Main chatbox function based on ChatCompletion API and GPT-3.5-turbo model"""
    st.title("MARTHA: Your marketing and advertising expert chatbox.")

    greeting_bot_msg = (
        "Hi, I am MARTHA, your marketing & advertising expert. Ask me any related question.\n"
        "Ah! I have no knowledge of 2022 onwards, because I am powered by ChatGPT. "
        "So, I don't do predictions.\n"
        "*Example*: 'What are the implications of the death of third party cookies for the industry?'\n"
        "I don't answer questions like 'Who was US president in 2010?'"
    )

    # Storing the chat
    if "generated" not in st.session_state:
        st.session_state["generated"] = [greeting_bot_msg]

    if "past" not in st.session_state:
        st.session_state["past"] = []

    prompt = (
        "Classify if the following prompt questions are related to marketing and advertising. "
        "If they are, answer the question. If they are not, reply only "
        "'This is not a marketing question' and do not answer the question. "
        "Limit your answer to 50 tokens if possible."
    )
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": prompt},
        ]

    user_input = get_text()

    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        response = generate_response_chat(st.session_state["messages"])
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response["content"])
        st.session_state["messages"].append(response)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            if i - 1 >= 0:
                message(
                    st.session_state["past"][i - 1], is_user=True, key=str(i) + "_user"
                )


if __name__ == "__main__":
    chatbot()
