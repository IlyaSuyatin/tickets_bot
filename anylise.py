import spacy as sp
import dateparser as dp
from difflib import get_close_matches
from datetime import datetime, timedelta
from enum import Enum

nlp = sp.load("en_core_web_md")
key_words = ["buy tickets", "purchase tickets", "book flights", "get tickets", "buy flight"]

# doc = nlp("I want to fly from Skelleftea to Stockholm on 29th of May")

class DatesStatus(Enum):
    EXPIRED = 0
    FAR = 1
    OK = 2

cities = []
with open("codes.txt")as file:
    rows = file.readlines()
    for row in rows:
        columns = row.split("|")
        city = columns[1].split(",")[0]
        cities.append(city)

def check_city (ent):
    correction = None
    close_matches = get_close_matches(ent.text.title(), cities, n=1)
    if len(close_matches) > 0:
        correction = close_matches[0]
    return correction


def analyse_input(text, nlp):
    doc = nlp(text)
    cities = []
    time = None
    intent = False
    for i, token in enumerate(doc):
        if i < len(doc) - 1:

            if (token.tag_ == "VB" or token.tag_ == "VERB"):
                for j in range(i + 1, len(doc)):
                    if doc[j].tag_ == "NOUN" or doc[j].tag_ == "NNS" or doc[j].tag_ == "NN":
                        break
                else:
                    break
                phrase = nlp(token.text + " " + doc[j].text)
                matches = get_close_matches(phrase.text, key_words, cutoff=0.3)
                print(matches)
                if len(matches) > 0:
                    phrase = nlp(matches[0])
                for key_word in key_words:
                    key_word = nlp(key_word)
                    if phrase.similarity(key_word) > 0.7:
                        intent = True
                        break
                if intent:
                    break
    if intent:
        for ent in doc.ents:
            if ent.label_ in ["DATE", "DATETIME"]:
                time = ent.text
                continue
            parsed_date = dp.parse(ent.text, date_formats=["%d/%m/%y", "%d.%m.%y", "%d/%m/%Y", "%d.%m.%Y"])
            if parsed_date:
                time = ent.text
                continue
            correction = check_city(ent)       
            if ent.label_ == "GPE" or correction:
                cities.append(correction)
                continue
        return(cities, time)

def convert_date(date):
    now = datetime.now()
    if isinstance(date, str):
        close_matches = get_close_matches(date, ['today', 'tomorrow', 'yesterday'])
        if close_matches:
            date = close_matches[0]
        if date == "today":
            return now
        elif date == "tomorrow":
            return now + timedelta(days=1)
        elif date == "yesterday":
            return now + timedelta(days=-1)
    separators = [".", "/"]
    for separator in separators:
        if separator in date:
            break
    parts = date.split(separator)
    if separator != ".":
        separator = "."
    if len(parts) == 2:
        parts.append(str(now.year))
    else:
        if len(parts[-1]) != 4:
            parts[-1] = "20" + parts[-1]
    try:
        return datetime.strptime(separator.join(parts), "%d.%m.%Y")
    except ValueError:
        return None
    # 05.06.2024

def check_date(date):
    date = convert_date(date)
    now = datetime.now()
    print(date-now)
    if (date-now).days < 1:
        return DatesStatus.EXPIRED
    elif (date-now).days > 150:
        return DatesStatus.FAR
    else:
        return DatesStatus.OK

# print(check_date(analyse_input("I want to purchase any the tickets from Skelldheftea to stockolm on yesterday", nlp)[1]))