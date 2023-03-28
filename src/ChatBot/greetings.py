import os.path
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.storage import SQLStorageAdapter
from chatterbot.search import IndexedTextSearch
import chatterbot.comparisons
import chatterbot.response_selection
import nltk


# Define the filename for the saved ChatBot
BOT_FILENAME = 'saved_bot.json'

# Check if a saved ChatBot exists
if os.path.isfile(BOT_FILENAME):
    # Load the saved ChatBot
    with open(BOT_FILENAME, 'r') as f:
        bot_dict = json.load(f)
        
        #load the bot
        bot = ChatBot(BOT_FILENAME)


else:
    # Create a new ChatBot instance with a SQLStorageAdapter
    bot = ChatBot(
        'MyChatBot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter'
    )

    # Read the training data from the "human_chat.txt" file
    with open('human_chat.txt', 'r', encoding='utf-8') as f:
        training_data = f.read().splitlines()


    # Train with many data sources mentioned https://github.com/PolyAI-LDN/conversational-datasets
    nltk.download('twitter_samples')
    nltk.download('webtext')
    nltk.download('movie_reviews')
    nltk.download('punkt')

    training_data.extend(nltk.corpus.twitter_samples.strings())
    training_data.extend(nltk.corpus.webtext.words())
    training_data.extend(nltk.corpus.movie_reviews.words())

    # Train the bot on the training data
    trainer = ListTrainer(bot)
    trainer.train(training_data)
print("Training complete!")

# Define a function to greet the user
def greet():
    print("Hello! I am here to help you learn about the weather.")

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

            if user_input == "exit":
                break

            # Get the bot's response
            bot_response = bot.get_response(user_input)

            #parse the bots response to remove all references to the "Human 1:" or "Human 2:" tags
            bot_response = str(bot_response).replace("Human 1: ", "")
            bot_response = str(bot_response).replace("Human 2: ", "")

            # Print the bot's response
            print(bot_response)

        # Handle user saying exit and keyboard interrupts
        except (KeyboardInterrupt, EOFError, SystemExit):
            break

    # Save the trained bot to a file
    with open(BOT_FILENAME, 'w') as f:
        bot_dict = bot.__dict__
        # Remove the IndexedTextSearch object from the dictionary
        bot_dict.pop('search_algorithm', None)
        bot_dict['name'] = bot.name
        json.dump(bot_dict, f, default=str)


# Run the main function
if __name__ == '__main__':
    main()
