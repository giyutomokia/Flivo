import google.generativeai as genai
import streamlit as st
import justiceAI_prompt as jp
import os

# Load environment variables from .env file

# User-specific details
ai_name = "Justice Ai"
# user_name = "Pavan"
# project = "building an AI assistant using Bard API"
# preference = "concise answers and daily updates"

# Configure API key
test_string = st.secrets["test_string"] 
genai.configure(api_key=test_string)

# Initialize conversation history log (in-memory list for now)
conversation_log = []

def summarize_response(ai_response):
    """
    Function to send the AI's response back to the AI and ask it to summarize the text.
    """
    summary_prompt = f"""
    Please summarize the following response in less than 100 characters:

    "{ai_response}"
    """
    model = genai.GenerativeModel('gemini-pro')
    summary_response = model.generate_content(summary_prompt)
    
    # Return the summarized version
    return summary_response.text.strip()

def save_conversation(question, ai_response):
    # Summarize the AI's response using the AI
    summarized_response = summarize_response(ai_response)
    
    # Store the interaction in a concise format
    conversation_log.append({
        'question': question,
        'response_summary': summarized_response
    })

def generate_prompt(Question_input):
    # Concisely summarize the previous conversation for context
    summary = ""
    if conversation_log:
        summary = "\n".join([f"User asked: '{log['question']}', AI responded: '{log['response_summary']}'" 
                             for log in conversation_log])
    else:
        summary = "No previous conversation history yet."

    # Create the prompt by integrating the summarized history
    prompt = jp.prompt + "\n now the question is " + Question_input + "\n and the previous conversation was this " + summary
    return prompt

# Streamlit UI
st.title(f"Chat with {ai_name}")

# Create a text input box for the user to ask questions
user_input = st.text_input("Enter your question", "")

if user_input:
    # Generate the prompt with memory
    Question = generate_prompt(user_input)

    # Show a loading spinner while generating the response
    with st.spinner(f"{ai_name} is thinking..."):
        # Use the generative AI model to get the response
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(Question)

    # Display the AI's response on Streamlit
    st.write(f"**{ai_name}:** {response.text}")

    # Save the interaction in the log by summarizing the AI's response
    save_conversation(user_input, response.text)

# Display the chat history
# if conversation_log:
#     st.write("### Conversation History")
#     for log in conversation_log:
#         st.write(f"**You:** {log['question']}")
#         st.write(f"**{ai_name}:** {log['response_summary']}")
