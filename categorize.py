import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
dbName = os.getenv('DB_NAME')
collectionName = os.getenv('COLLECTION_NAME')
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client[dbName]
collection = db[collectionName]
scholarships_document = collection.find_one()
scholarships = scholarships_document.get("scholarships", [])

categories = {
    'first_generation_women': ['first generation', 'first-gen', 'first generation student','first gen'],
    'women_of_color': ['latina', 'black', 'african', 'asian', 'women of color', 'person of color', 'native american', 'pacific island', 'native hawaii'],
    'women_with_disabilities': ['disability', 'disabled', 'women with disabilities', 'disable', 'handicap'],
    'lgbtq': ['lgbt', 'lgbtq', 'lesbian', 'gay', 'bisexual', 'transgender', 'lgbtqia', 'queer'],
    'women_in_stem': ['engineering', 'stem', 'science', 'technology', 'management', 'tech','computer science','microsoft','apple','google']
}

for scholarship in scholarships:
    tags = set()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in scholarship['description'].lower() or keyword in scholarship['subject'].lower():
                tags.add(category)
                break
    scholarship['tags'] = list(tags)
    collection.update_one(
        {"_id": scholarships_document["_id"]},
        {"$set": {"scholarships": scholarships}}
    )

    print(f"The tags for {scholarship['name']}: {str(scholarship['tags'])} ")
