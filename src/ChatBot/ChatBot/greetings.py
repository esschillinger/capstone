import os.path
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.storage import SQLStorageAdapter

# Define the filename for the saved ChatBot
BOT_FILENAME = 'saved_bot.json'

# Check if a saved ChatBot exists
if os.path.isfile(BOT_FILENAME) and os.path.getsize(BOT_FILENAME) > 0:
    with open(BOT_FILENAME, 'r') as f:
        bot_data = json.load(f)
        bot = ChatBot('MyChatBot', **bot_data)
else:
    # Create a new ChatBot instance with a SQLStorageAdapter
    bot = ChatBot(
        'MyChatBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
    )

    # Read the training data from the "human_chat.txt" file
    with open('human_chat.txt', 'r', encoding='utf-8') as f:
        training_data = f.read().splitlines()


    # Train the bot on the training data
    trainer = ListTrainer(bot)
    trainer.train(training_data)

# Define a function to greet the user
def greet():
    print("Hello! My name is Chatbot. I have been trained on human_chat.txt. What can I help you with today?")

# Define a main function to run the chatbot
def main():
    # Greet the user
    greet()

    # Start the conversation loop
    while True:
        try:
            # Get the user's input
            user_input = input("> ")

            # Check if the user input is empty
            if not user_input:
                continue  # Skip to the next iteration of the loop

            # Get the bot's response
            bot_response = bot.get_response(user_input)

            #parse the bots response to remove all refremces to the "Human 1:" or "Human 2:" tags
            bot_response = str(bot_response).replace("Human 1: ", "")
            bot_response = str(bot_response).replace("Human 2: ", "")

            # Print the bot's response
            print(bot_response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break


# Run the main function
if __name__ == '__main__':
    main()
