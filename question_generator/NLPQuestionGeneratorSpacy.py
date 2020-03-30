import numpy as np
import spacy
from nlp_helpers import NLPConn

nlp = NLPConn.get_nlp_conn()


def fill_in_the_blank_question_generation(sentence):
    doc = nlp(sentence)
    questions = []
    for ent in doc.ents:
        question = sentence[:ent.start_char] + "______" + sentence[ent.end_char:]
        answer = ent.text
        questions.append((question, answer))
    return questions


def nlp_question_generation(sentence):
    """
    Creates a mix of multiple choice and wh-questions
    """
    doc = nlp(sentence)
    hasQuestionMark = False #  boolean to check if it's a wh question or fib questions
    questions = []
    for ent in doc.ents:
        questionTag = "______"
        if(ent.label_ == "PERSON" and ent.start_char == 0 ):
            questionTag = "Who"
            hasQuestionMark = True
        elif(ent.label_ == "ORG"):
            if(not ent.start_char == 0):
                questionTag = "what"
            else:
                questionTag = "What"
            hasQuestionMark = True
        elif(ent.label_ == "DATE"):
            if(not ent.start_char == 0):
                if("century" in ent.text):
                    questionTag = "which century"
                else:
                    questionTag = "which year"
            else:
                questionTag = "When"
            hasQuestionMark = True
        elif(ent.label_ == "TIME"):
            if(not ent.start_char == 0):
                questionTag = "at what time"
            else:
                questionTag = "When"
            hasQuestionMark = True
        elif(ent.label_ == "MONEY"):
            if(not ent.start_char == 0):
                questionTag = "how much"
                hasQuestionMark = True
        if(hasQuestionMark == True):
            question = sentence[:ent.start_char] + questionTag + sentence[ent.end_char:-1] + "?"
            hasQuestionMark = False
        else:
            question = sentence[:ent.start_char] + questionTag + sentence[ent.end_char:]
        answer = ent.text
        questions.append((question, answer))
    return questions


def main():
    corpus = ["Stable nuclides are nuclides that are not radioactive and so (unlike radionuclides) do not spontaneously undergo radioactive decay.",
              "Elvis Presley was a prominent singer of the 20th century.",
              "Usain Bolt, the Jamaican runner is an 11-time world champion and holds the record in the 100 and 200 meter race.",
              "The first Wimbledon Championship was held in 1877.",
              "Christian Bale reportedly studied Tom Cruise’s mannerisms to prepare for his role as a serial killer Patrick Bateman in American Psycho.",
              "Gene Autry is the only person to be awarded stars in all five categories on the Hollywood Walk of Fame.",
              "The hashtag symbol is technically called an octothorpe.",
              "It’s been said that nearly 3% of the ice in Antarctic glaciers is penguin urine.",
              "Ahmad Saad is a student at Temple University.",
              "Ahmad buys Apple stocks for 100 million dollars."]
    
    fib_questionBank = []
    nlp_questionBank = []

    #  Generating just Fill in Blanks questions
    for sentence in corpus:
        questions = fill_in_the_blank_question_generation(sentence)
        for items in questions:
            fib_questionBank.append((items[0], items[1])) 

    #Generating wh-questions and fill in the blank questions
    for sentence in corpus:
        questions = nlp_question_generation(sentence)
        for items in questions:
            nlp_questionBank.append((items[0], items[1]))           

    for items in fib_questionBank:
        print("\b Question: " + str(items[0]) + "\n")
        print("Correct Answer: " + str(items[1]) + "\n")

    for items in nlp_questionBank:
        print("\b Question: " + str(items[0]) + "\n")
        print("Correct Answer: " + str(items[1]) + "\n")


if __name__ == '__main__':
    main()
