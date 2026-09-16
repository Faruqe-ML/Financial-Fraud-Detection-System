from chatbot.langchain_bot import ask_chatbot


response = ask_chatbot(
    "What can you tell me about fraud detection?"
)

print("\nAI RESPONSE:")
print(response)