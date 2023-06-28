import json
import random
f = open('ngram.json')
f2 = json.load(f)
question_words = ["siapa", "apa", "kapan",
                  "dimana", "mengapa", "bagaimana", "berapa"]
nouns = []
for k, v in f2.items():
    nouns.append(k)

# Define a function to generate a random two-word question


def generate_question():
    # Choose a random question word and noun
    question_word = random.choice(question_words)
    noun = random.choice(nouns)

    # Concatenate the question word and noun
    question = question_word + " " + noun

    # Use the NLP model to check if the question is grammatically valid
    # doc = nlp(question)

    # If the question is not a valid noun phrase or verb phrase, generate a new question
    # if not any([chunk.label_ in ["NP", "VP"] for chunk in doc.noun_chunks]) or not any([chunk.label_ == "VP" for chunk in doc.verb_chunks]):
    #     return generate_question()

    # Add a question mark at the end of the question
    question += "?"

    return question


hasil = {}
for n in nouns:
    sentence = []
    for q in question_words:
        # print(q + " " + n + "?")
        sementara = q + " " + n + "?"
        sentence.append(sementara)
        hasil[n] = sentence
        # question = generate_question()
        # print(question)
with open('pertanyaan baru.json', 'w', encoding='utf-8') as f:
    json.dump(hasil, f, ensure_ascii=False, indent=4)
