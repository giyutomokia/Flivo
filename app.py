import google.generativeai as genai
import justiceAI_prompt as jp
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# User-specific details
ai_name = "Flivo AI"

# Configure API key
api_key = "AIzaSyDgc78PnoUQUau0m4QbAUJtYIv9BKNbHhU"
genai.configure(api_key=api_key)

# Initialize the model outside of the function
model = genai.GenerativeModel('gemini-pro')

# Initialize conversation history log
conversation_log = []


def summarize_response(ai_response):
    """Summarizes AI responses to less than 100 characters."""
    summary_prompt = f"""
    Please summarize the following response in less than 100 characters:
    "{ai_response}"
    """
    try:
        summary_response = model.generate_content(summary_prompt)
        return summary_response.text.strip()
    except Exception as e:
        logging.error(f"Error summarizing response: {e}")
        return "Summary could not be generated."


def save_conversation(question, ai_response):
    """Saves the conversation by summarizing and logging it."""
    summarized_response = summarize_response(ai_response)
    conversation_log.append({'question': question, 'response_summary': summarized_response})


def generate_prompt(Question_input):
    """Generates the prompt for the AI model."""
    summary = "\n".join(
        [f"User asked: '{log['question']}', AI responded: '{log['response_summary']}'"
         for log in conversation_log]
    ) if conversation_log else "No previous conversation history yet."
    prompt = jp.prompt + "\n now the question is " + Question_input + "\n and the previous conversation was this " + summary
    return prompt


def main():
    """Main loop for the interactive console-based chat."""
    print(f"Welcome to {ai_name}! Type 'exit' to quit.")
    while True:
        user_input = input("Enter your question: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        Question = generate_prompt(user_input)

        if not Question.strip():
            print("Generated prompt is empty. Please check your input.")
            continue

        logging.debug(f"Generated Question: {Question}")

        try:
            print(f"{ai_name} is thinking...")
            response = model.generate_content(Question)
            print(f"{ai_name}: {response.text}")
            save_conversation(user_input, response.text)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print("An error occurred. Please try again.")


if __name__ == "__main__":
    main()
