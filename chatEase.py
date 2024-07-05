import nltk
import re
import random
from nltk.corpus import stopwords

# Ensure stopwords are downloaded
nltk.download('stopwords')

# Define some responses
R_ADVICE = "Here's some advice: Do your best!"
R_EATING = "I'm eating virtual food right now."
UNKNOWN_RESPONSE = "I'm sorry, I didn't understand that."

# List of predefined responses
responses = {
    "hello": ["Hello!!", "Hi there!", "Hey!", "Hi!"],
    "bye": ["Goodbye!", "See you later!", "Bye!"],
    "how are you": ["I'm doing fine, and you?", "I'm good, how about you?", "Doing well, thanks for asking!"],
    "thank you": ["You're welcome!", "No problem!", "My pleasure!"],
    "advice": [R_ADVICE],
    "eat": [R_EATING]
}

# Function to check message probability
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainity = 0
    has_required_words = True
    
    # Count how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainity += 1
    
    # Calculate the percent of recognised words in the user message
    percentage = float(message_certainity) / float(len(recognised_words))
    
    # Check that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    
    # Must either have the required words or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

# Function to check all messages
def check_all_messages(message):
    highest_prob_list = {}
    
    # Simplifies response creation / add it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)
        
    # Responses
    response("Hello!!", ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response("See you!", ['bye', 'good bye', 'good night'], single_response=True)
    response("I'm doing fine, and you?", ['how', 'are', 'you', 'doing'], required_words=['how'])
    response("You're welcome!", ['thank', 'thanks'], single_response=True)
    
    # Longer responses
    response(R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return UNKNOWN_RESPONSE if highest_prob_list[best_match] < 1 else best_match

# Function to get a response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

# Main loop
if __name__ == "__main__":
    print("ChatBot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("ChatBot: Goodbye! Have a great day!")
            break
        print(f"ChatBot: {get_response(user_input)}")
