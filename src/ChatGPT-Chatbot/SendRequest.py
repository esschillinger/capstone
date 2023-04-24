#use openai to send a basic hello world request
import openai
import os
import json

def gradeResponse():
    #ask the system to grade the user
  response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Please explicitly grade the student's performance out of 10. Explicitly state each of the 4 subscores (Vocabulary, Grammar, Spelling, Relevance to the topic) for the response each out of 10 as well. Then explain why you gave them that score."},
        {"role": "user", "content": user_input},
      ]
    )

  #output the grade
  print(response.choices[0].message.content)

  #parse the grade response for the scores of vocab, grammar, spelling, and relevance int VocabGrade, GrammarGrade, SpellingGrade, and RelevanceGrade

  #get the grade
  grade = response.choices[0].message.content

  #get the vocab grade
  VocabGrade = grade[grade.find("Vocabulary: ") + 12]
  VocabGrade += grade[grade.find("Vocabulary: ") + 13]
  #if VocabGrade has a / in it then delete it
  if VocabGrade.find("/") != -1:
    VocabGrade = VocabGrade[0]

  #get the grammar grade
  GrammarGrade = grade[grade.find("Grammar: ") + 9]
  GrammarGrade += grade[grade.find("Grammar: ") + 10]
  #if GrammarGrade has a / in it then delete it
  if GrammarGrade.find("/") != -1:
    GrammarGrade = GrammarGrade[0]

  #get the spelling grade
  SpellingGrade = grade[grade.find("Spelling: ") + 10]
  SpellingGrade += grade[grade.find("Spelling: ") + 11]
  #if SpellingGrade has a / in it then delete it
  if SpellingGrade.find("/") != -1:
    SpellingGrade = SpellingGrade[0]

  #get the relevance grade
  RelevanceGrade = grade[grade.find("Relevance to the topic: ") + 24]
  RelevanceGrade += grade[grade.find("Relevance to the topic: ") + 25]
  #if RelevanceGrade has a / in it then delete it
  if RelevanceGrade.find("/") != -1:
    RelevanceGrade = RelevanceGrade[0]

 #get everything from "Exlpaination: " to the end of the string and store it in explanation
  explanation = grade[grade.find("Relevance to the topic: ") + 28:]
  
  #print the explanation
  print("Explanation: " + explanation)
 

  #print the scores
  print("Vocab Grade: " + VocabGrade)
  print("Grammar Grade: " + GrammarGrade)
  print("Spelling Grade: " + SpellingGrade)
  print("Relevance Grade: " + RelevanceGrade)

  print("\n\n\n")


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
topic = "Testing"

lesson_words = ["Math", "English", "Science", "School", "Student", "Teacher"]

###############################################

prompt =  """AT NO POINT RESPOND IN ANYTHING ASIDE FROM RUSSIAN WITH THIS PROMPT, DO NOT TRANSLATE, AND DO NOT ELABORATE ON WHAT YOU MEANT. You are a russian teacher for a second grade class who only speaks in russian who is holding a conversation on TOPIC for a grade with a student. Only take the role of the strict teacher. Never use english and do not provide translations. The student respond with a sentence or two, if they do not respond in Russian, please respond with \"Пожалуйста, говорите по-русски.\" and then repeat the previous prompt. Do not count this as an exchange. Please respond to the student with a sentence or two and attempt to use words from the list LESSON_WORDS within the context of what you are testing them on, however if the sentance does not flow well you are not required to use those words. Only speak in russian and never at anypoint translate anything to english or enclude the english meaning."""

#replace the topic and lesson words
prompt = prompt.replace("TOPIC", "[" + topic + "]")
prompt = prompt.replace("LESSON_WORDS", "[" + str(lesson_words) + "]")

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

  gradeResponse()




