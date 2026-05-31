print("Welcome to the Rule-Based Chatbot!")
print("Type 'bye' to exit.\n")

while True:
    user_input = input("You: ").lower()

    if user_input == "hello" or user_input == "hi":
        print("Bot: Hello! How can I help you today?")

    elif "how are you" in user_input:
        print("Bot: I'm doing well. Thank you for asking!")

    elif "your name" in user_input:
        print("Bot: My name is ChatBot.")

    elif "help" in user_input:
        print("Bot: I can answer simple questions. Try asking about my name or how I am.")

    elif "thank you" in user_input or "thanks" in user_input:
        print("Bot: You're welcome!")

    elif user_input == "bye":
        print("Bot: Goodbye! Have a great day!")
        break

    else:
        print("Bot: Sorry, I don't understand that.")
