from openai import OpenAI
from dotenv import load_dotenv
import tiktoken
import json

load_dotenv()
client = OpenAI()

MAX_RETRIES = 50

content = "../data/content.json"
embed_output = "../data/embeds.json"

encoder = tiktoken.get_encoding("cl100k_base")

def get_embedding(text, model="text-embedding-3-large"):
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def load_embed():
    vectors = []
    cnt = 1
    skp = 0
    with open(content,"r") as f:
        d = json.load(f)
        for term,value in d.items():
            embed,retry_attempts = [],0
            while not embed and retry_attempts < MAX_RETRIES:
                try:
                    definition = value["description"]
                    if len(encoder.encode(definition)) <= 8191:
                        embed = get_embedding(definition)
                        vectors.append({ "id" : term, "values" : embed })
                        print(f'Embedded term {cnt}/{len(d)}')
                        cnt += 1
                    else:
                        print(f'Skipped {term} due to large token length')
                        skp += 1
                        break
                except Exception as e:
                    retry_attempts += 1
                    print(f'Exception raised -> {e}, retrying for the {retry_attempts}th time')
                    

    print("Skipped {skp} total terms")
        
    with open(embed_output, 'w') as f:
        json.dump(vectors, f,indent=4)

load_embed()