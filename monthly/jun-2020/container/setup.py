import pymongo

f = open("flag.txt")
flag = f.read()
f.close()

client = pymongo.MongoClient()

db = client["ss"]
collection = db["books"]

collection.insert_one(
    {
        "id": 0,
        "name": "SQLI för nybörjare",
        "author": "sven svenson",
        "description": "En bok om hur man gör sql injections, för nybörjare",
        "borrowed": False,
    }
)
collection.insert_one(
    {
        "id": 1,
        "name": "pwnhub",
        "author": "sten stenson",
        "description": "Boken som förklarar allt om hur man pwnar alla möjliga binärer!",
        "borrowed": False,
    }
)
collection.insert_one(
    {
        "id": 2,
        "name": "Hur man blir en hacker",
        "author": "hacker hackerson",
        "description": 'Har du någonsin tänkt dig "hmm, jag undrar hur man hackar"? ja? Då är den här boken perfekt för dig!',
        "borrowed": False,
    }
)

collection.insert_one(
    {
        "id": 39800907872953481,
        "name": "Flagboken",
        "author": "???",
        "description": flag,
        "borrowed": True,
    }
)
