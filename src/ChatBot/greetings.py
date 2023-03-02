import json
import os.path
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

    # Define the training data
    training_data = [
        'Hi',
        'Hello',
        'What is your name?',
        'My name is Chatbot',
        'What can you do?',
        'I can help you with tasks or answer questions',
        'How are you?',
        'I am doing well, thank you for asking',
        'Goodbye',
        'Goodbye, have a nice day!'
    ]

    # Create a new trainer and train the bot on the training data
    trainer = ListTrainer(bot)
    trainer.train(training_data)

    # Get the bot's data and save it to a JSON file


    #ESTABLISH SETTING BELOW
    bot_data = bot.get_response('Hello').serialize()

    # Convert the datetime object to a string and save the bot's data
    bot_data['created_at'] = bot_data['created_at'].isoformat() # convert datetime to string
    with open(BOT_FILENAME, 'w') as f:
        json.dump(bot_data, f)

# Define a function to greet the user
def greet():
    print("Hello! My name is Chatbot. What can I help you with today?")

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

            # Print the bot's response
            print(bot_response)

        except (KeyboardInterrupt, EOFError, SystemExit):
            break


# Run the main function
if __name__ == '__main__':
    main()
