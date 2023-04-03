from googletrans import Translator


def translate(text, native, target):
    ts = Translator()
    result = ts.translate(text, src=target[:2], dest=native[:2])
    
    return result.text


temp_grades = [{
        'data' : 'Это место переводит текст, что под находится когда GPT ответит.',
        'grade_msg' : '<p>Spelling: 0/10. Bad response.</p>\n<p>Grammar: 0/10. Equally bad response. You\'re just not that guy.</p>',
        'spelling' : 0,
        'grammar' : 0
    },
    {
        'data' : 'Вам невозможно это читать. Так, мне можно сказать что-либо, что я хочу.',
        'grade_msg' : '<p>Spelling: 8/10. Random placeholder text here bruh bruh bruh</p>\n<p>Grammar: 7/10. Bruh buh bruh bruh bruh, bruh bruh bruh.</p>',
        'spelling' : 8,
        'grammar' : 7
    },
    {
        'data' : 'Сегодня утром я купил очень дорогое молоко. Просто такое дорогое, что тебе невозможно оно полагать.',
        'grade_msg' : '<p>Spelling: 10/10. There were no spelling mistakes in your response.</p>\n<p>Grammar: 10/10. Your response was well-formed, and does not contain any grammatical errors.</p>',
        'spelling' : 10,
        'grammar' : 10
    }]



# if __name__ == "__main__":
#     print(translate("Hello", native="russian", target="english"))