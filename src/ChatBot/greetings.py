import json
import os.path
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.storage import SQLStorageAdapter
from nltk.corpus import brown

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

    # Create a new trainer and train the bot on the Brown corpus from NLTK
    trainer = ListTrainer(bot)
    trainer.train(' '.join([' '.join(sentence) for sentence in brown.sents()]))

    #trainer = ListTrainer(bot)
    #trainer.train(['Hello, how are you doing today? I am doing well, thank you for asking.', 
                  # 'What is your favorite color? Mine is blue.', 
                   #'What do you like to do in your free time?', 
                   #'Do you have any pets? I have a cat named Fluffy.', 
     #              'What is your favorite food?', 
           #        'Do you have any siblings?', 
          #         'What is the weather like today?', 
         #          'How old are you?', 
        #           'What is your favorite book?', 
     #              'What is your favorite movie?', 
      #             'What is your favorite song?', 
       #            'Do you like to travel?', 
        #           'What is your favorite place to visit?', 
         #          'What is your favorite hobby?'])

    # Get the bot's data and save it to a JSON file
    bot_data = bot.get_response('Hello').serialize()
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


# Run the chatbot
if __name__ == '__main__':
    main()
