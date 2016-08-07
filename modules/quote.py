import random

def getQuote():
    number = random.randint(0,9)
    quotes = [
            "The teacher's become the master. ",
            "That is how I find out raw eggs work as well as any sexual lubricant, men.",
            "On saturday your gonna walk on that field with a dick full of confidence",
            "What if we kill the professor? If your teacher dies, they have to give you all A's. It's the law.",
            "I READ AT A FOURTH GRADE LEVEL!",
            "I can't believe this dick had the balls to show up here." ,
            "What rhymes with best bros? Mojitos! ill go whip us up a batch" ,
            "Does a whale shit in the ocean? Not if it's in sea world",
            "You don't have to tell me about the bro code, I practically invented it.",
            "I wish I could rip my arms off and give them to you so you can call me sometime."
    ]
    return quotes[number]
