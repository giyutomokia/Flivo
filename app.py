import google.generativeai as genai
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# User-specific details
ai_name = "Flivo AI"

# Define the prompt structure
prompt_template = [
    "You are a helpful assistant providing answers to user queries.",
    "Make sure your answers are concise and clear.",
]

# Hardcoded API key (for testing purposes only)
api_key = "AIzaSyDgc78PnoUQUau0m4QbAUJtYIv9BKNbHhU"

# Configure API key for the Generative AI model
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring the Generative AI model with the API key: {e}")
    api_key = None

# Initialize the model outside of the function
try:
    if api_key:
        model = genai.GenerativeModel('gemini-pro')
    else:
        model = None
except Exception as e:
    st.error(f"Error initializing the Generative Model: {e}")
    model = None

# Initialize conversation history log
conversation_log = []

# Function to summarize AI response
def summarize_response(ai_response):
    summary_prompt = f"""
    Please summarize the following response in less than 100 characters:
    "{ai_response}"
    """
    try:
        summary_response = model.generate_content(summary_prompt)
        return summary_response.text.strip()
    except Exception as e:
        st.error(f"Error summarizing response: {e}")
        return "Summary could not be generated."

# Function to save conversation
def save_conversation(question, ai_response):
    summarized_response = summarize_response(ai_response)
    conversation_log.append({'question': question, 'response_summary': summarized_response})

# Function to generate a prompt
def generate_prompt(question_input):
    conversation_summary = "\n".join(
        [f"User asked: '{log['question']}', AI responded: '{log['response_summary']}'"
         for log in conversation_log]
    ) if conversation_log else "No previous conversation history yet."
    
    prompt = "\n".join(prompt_template) + \
             f"\nNow the question is: {question_input}\nPrevious conversation was: {conversation_summary}"
    return prompt

# Streamlit UI
st.title(f"Chat with {ai_name}")

user_input = st.text_input("Enter your question", "")

if user_input:
    # Generate prompt from user input and conversation log
    Question = generate_prompt(user_input)

    if not Question.strip():
        st.error("Generated prompt is empty. Please check your input.")
    else:
        logging.debug(f"Generated Question: {Question}")
        with st.spinner(f"{ai_name} is thinking..."):
            if model:
                try:
                    response = model.generate_content(Question)
                    st.write(f"**{ai_name}:** {response.text}")
                    save_conversation(user_input, response.text)
                except Exception as e:
                    st.error(f"An error occurred while generating a response: {e}")
            else:
                st.error("The generative model is not initialized. Please fix the configuration.")
