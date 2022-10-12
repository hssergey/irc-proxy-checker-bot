import random
import requests


def boobs():
    max_tries = 10
    start_id = 2500
    end_id = 7326
    for i in range(0, max_tries):
        id = random.randint(start_id, end_id)
        url = "http://media.oboobs.ru/boobs/0%s.jpg" % id
        response = requests.head(url, timeout = 10)
        if response.status_code == 200:
            return url
    return ""


def fun_handlers(message):
    shit_words = [
        "ауди",
        "бмв",
        "инфинити",
        "опель",
        "крузак",
        "финик",
        "бэха",
        "митсуби",
#        "пикап",
        "бентли",
        "вольво",
        "акцент",
        "гетц",
        "кайен",
        "бугатти",
        "фольксваген",
        "шкода",
        "мазда",
        "тойота",
        "кабриолет",
    ]
    rules_words = [
        "пятерка",
        "семерка",
        "восьмерка",
        "девятка",
    ]
    kokoko_words = [
        "ко ко ко",
        "ко-ко-ко",
    ]
    
    if "_сиськи" in message or "!сиськи" in message:
        return boobs()
    for word in shit_words:
        if word in message.lower():
            test = random.randint(0, 1000)
            if test > 500:
                return "%s говно" % word
    for word in rules_words:
        if word in message:
            test = random.randint(0, 1000)
            if test > 500:
                return "%s рулит" % word
    for word in kokoko_words:
        if word in message:
            test = random.randint(0, 1000)
            if test > 500:
                return "Лососни тунца"
    if "макось" in message:
        test = random.randint(0, 1000)
        if test > 500:
            return "гейось не нужна"
#    if "винда" in message:
#        test = random.randint(0, 1000)
#        if test > 500:
#            return "фи маздай"
    if "макбук" in message:
        test = random.randint(0, 1000)
        if test > 500:
            return "[00:00:51] <@yekm> http://i.imgur.com/fAq3SkA.jpg - самое место для гейбука :)"
    if "запорожец" in message:
        test = random.randint(0, 1000)
        if test > 500:
            return "запорожец наше все!"
    
    return ""
        
