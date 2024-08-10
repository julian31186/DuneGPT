from pinecone import Pinecone
from dotenv import load_dotenv
import os
import math
import json

load_dotenv()
pc = Pinecone(api_key=os.environ.get("PINECONE_KEY"))
index = pc.Index("dune-gpt")
embeds = "../data/embeds.json"

def load_pinecone():
    batch_num = 1
    with open(embeds,'r') as f:
        data = json.load(f)
        print(type(data))
        for i in range(0,len(data),10):
            if i + 10 < len(data):
                index.upsert(data[i:i + 10])
            else:
                index.upsert(data[i: i + len(data) - i])

            print(f'Uploaded batch number -> {batch_num}/{math.ceil(len(data) / 10)}')
            batch_num += 1

load_pinecone()