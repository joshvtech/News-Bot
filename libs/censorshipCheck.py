censorWords = [
    "shit",
    "fuck",
    "piss",
    "dick",
    "cunt",
    "faggot"
]

def check(message):
    message = message.content.lower()
    for i in censorWords:
        if i in message:
            return(True)
    return(False)
