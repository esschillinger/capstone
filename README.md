# capstone
Capstone project for CS 495 at The University of Alabama
Authors: Ethan Schillinger, H. Jacob Schenck, and Joe Vossel

# Running the App

To run the current version of the application, navigate to the src directory in a terminal and run the following command:

```sh
python application.py
```

This should locally host the web app, at which point you can open a browser and go to the indicated IP to interact with the app.

# Testing Procedures

Testing for the data persistence was performed primarily via the flash cards app route. We tested different unit selections and then navigated to the flash cards section. The correct flash cards corresponding to the current unit were pulled up, indicating that the user's choices are properly being accounted for and reflected in the content that is displayed.

The English chatbot was tested by providing various inputs in natural conversation settings. Given that our primary focus is creating specialized scenarios/environments in which the user can practice conversation, we tried to keep the bot to specific topics, such as the weather or a patron-server interaction in a restaurant. Example conversations are located in our Sprint 1 Presentation.