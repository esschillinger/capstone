#use openai to send a basic hello world request
import openai
import os
import json

#key is on my desktop in PASSCODES.txt file
with open('C:\\Users\\javos\\Desktop\\PASSCODE.txt') as f:
    lines = f.readlines()
    key = lines[0].strip()

#set the key
openai.api_key = key

###############################################
#THIS IS WHERE WE PASS IN THE TOPIC
# Prompt is roughly below
# Pretend that you are a russian teacher for a second grade class. 
# You are teaching them a lesson on TOPIC
# Please start a conversation with the student by saying "Здравствуйте, меня зовут мистер Джозеф Джейкоб Шиллингер.""
# The student will respond to you with a sentence or two, if they do not respond in russian, please respond with "Пожалуйста, говорите по-русски." and then repeat the prompt. Do not count this as an exchange.
# Please respond to the student with a sentence or two using words from the list LESSON_WORDS within the context of what you are teaching 
# After 5 exhanges, stop the conversation and end the lesson.
# Still in the role of the teacher, please describe the students grammer, spelling, vocabulary, on topicness, and overall performance.
# rate each individual response from the student out of 10 extremely harshly and honestly, and explain why you gave them that score.
# Note that a score of 0 is the worst possible score, and a score of 10 is the best possible score, and a score of 6 is average and acceptable.
topic = "Greetings"

lesson_words = ["Math", "English", "Science", "School", "Student", "Teacher"]

###############################################

prompt =  """Pretend that you are a russian teacher for a second grade class who only speaks in russian who is holding a mock conversation on TOPIC for a grade with a student. The student will respond to you with a sentence or two, if they do not respond in Russian, please respond with \"Пожалуйста, говорите по-русски.\" and then repeat the prompt. Do not count this as an exchange. Please respond to the student with a sentence or two using words from the list LESSON_WORDS within the context of what you are testing them on. Only speak in russian and do not translate anything."""

#replace the topic and lesson words
prompt = prompt.replace("TOPIC", topic)
prompt = prompt.replace("LESSON_WORDS", str(lesson_words))

#send a request to openai giving it the prompt as context and asking for 1 response, and then output it. 
#then wait for user input to continue, and then send the user input back to the api as context and ask for 1 response, and then output it.
#repeat this 5 times
user_input = ""
total_input = ""
for i in range(5):
 # print(prompt)
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_input},
      ]
    
    )

  #print the response
  test = response.choices[0].message.content
  print(test)

    #get user input
  user_input = input("Enter your response: ")

  #add the user input to the prompt
  prompt += user_input
  total_input += user_input

  #add 2 newlines to the prompt
  prompt += "\n\n"

#ask the system to grade the user


response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Please grade the student's performance out of 10. Explicitly state each of the 4 subscores (Vocabulary, Grammar, Spelling, Relevance to the topic) for the responses. Then explain why you gave them that score and if they are ready to move on to the next lesson or need more practice."},
        {"role": "user", "content": total_input},
      ]
    )

#output the grade
print(response.choices[0].message.content)
