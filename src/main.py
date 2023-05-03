import os
import streamlit as st
import openai


def main():
    openai.organization = os.getenv("OPENAI_API_ORG")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    st.title("MARTHA: Your marketing & advertising expert.")

    st.write("This is your marketing & advertising expert. Ask me any related question. Ah! I have no knowledge of 2022 onwards, because I am powered by ChatGPT. So, I don't do predictions.")

    st.write("**Example:** *'What are the implications of the death of third party cookies for the industry?'*")
    st.write("I don't answer questions like *'Who was US president in 2010?'*")

    input_txt = st.text_area("Ask me your question. Answers will be limited to 256 tokens")

    prompt = (
        "You are an expert in marketing and adverting and working for WPP or one of its agencies. "
        "If a question is not related to marketing and advertising answer 'This is not a marketing & advertising question'. "
        "Limit your answer to 50 tokens if possible. "
    )

    if input_txt != "":
        prompt += input_txt

        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=256)
        # Print answer to the screen
        st.write(response["choices"][0]["text"])

    return

if __name__ == "__main__":
    main()
