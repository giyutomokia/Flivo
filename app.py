import google.generativeai as genai
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure API key for Generative AI
genai.configure(api_key="AIzaSyDgc78PnoUQUau0m4QbAUJtYIv9BKNbHhU")  # Replace with your actual API key

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

def generate_prompt(user_input):
    """
    Generate a prompt for the AI based on user input.
    """
    return f"AI, please respond to the following question: {user_input}"

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    """
    # Log the received event for debugging
    logging.debug(f"Received event: {event}")

    # Get user input from the event
    user_input = event.get('user_input')
    if not user_input:
        return {'statusCode': 400, 'body': 'Missing user_input in the request body.'}
    
    try:
        # Generate the prompt and get AI response
        prompt = generate_prompt(user_input)
        response = model.generate_content(prompt)
        
        # Return the AI response
        return {'statusCode': 200, 'body': response.text}
    except Exception as e:
        # Log and return the error
        logging.error(f"Error occurred: {e}")
        return {'statusCode': 500, 'body': f"An error occurred: {e}"}
