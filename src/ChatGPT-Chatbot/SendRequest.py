#use openai to send a basic hello world request
import openai
import os
import json

#key is on my desktop in PASSCODES.txt file
with open('C:\\Users\\javos\\Desktop\\PASSCODE.txt') as f:
    lines = f.readlines()
    key = lines[0].strip()

    #hash the key
    hash(key)

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

lesson_words = ["Hello", "Goodbye", "Yes", "NO", "Yikes"]

###############################################

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.3,
  messages=[
    {"role": "user", "content": "Pretend that you are a russian teacher for a second grade class. You are teaching them a lesson on TOPIC. The student will respond to you with a sentence or two, if they do not respond in russian, please respond with \"Пожалуйста, говорите по-русски.\" and then repeat the prompt. Do not count this as an exchange. Please respond to the student with a sentence or two using words from the list LESSON_WORDS within the context of what you are teaching. After 5 exhanges, stop the conversation and end the lesson. Still in the role of the teacher, please describe the students grammer, spelling, vocabulary (if they used words in TOPIC_LIST), on topicness, and overall performance. Rate each individual response from the student out of 10 extremely harshly and honestly, and explain why you gave them that score. Note that a score of 0 is the worst possible score, and a score of 10 is the best possible score, and a score of 6 is average and acceptable. Explicitly each of the 5 subscores for the responses ONLY AT the end of the 5 exchanges and make sure to explicitly state the score. Then explain why you gave them that score and explicitly state if you think that they are ready for the next unit. Please start a conversation with the student by saying \"Здравствуйте, меня зовут мистер Джозеф Джейкоб Шиллингер.\" and I will take the role of the student. AT NO POINT TRANSLATE WHAT IT BEING SAID."},
  ]
)

print(completion.choices[0].message.content)



#output the response to a file
with open('response.json', 'w') as outfile:
    json.dump(completion.choices[0].message.content, outfile)
