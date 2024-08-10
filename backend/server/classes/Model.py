import tiktoken
import os
import json
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote
import pymysql

# Proper error handling weather its a 503 error from OAI or out of tokens or input is too many tokens

class Model:
    def __init__(self, max_retries=50):
        load_dotenv()
        self.sql_url = os.environ.get("MYSQL_URL")
        self.parsed_url = urlparse(self.sql_url)
        self.conn = pymysql.connect(
            host=self.parsed_url.hostname,
            user=unquote(self.parsed_url.username),
            password=unquote(self.parsed_url.password),
            port=self.parsed_url.port,
            database=self.parsed_url.path[1:]
        )
        self.cursor = self.conn.cursor()
        self.oai = OpenAI()
        self.MAX_RETRIES = max_retries
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.pc = Pinecone(api_key=os.environ.get("PINECONE_KEY"))
        self.pc_index = self.pc.Index("dune-gpt")

    def generate_embedding(self, query, model="text-embedding-3-large"):
        retries = 0
        embedding = []
        while not embedding and retries < self.MAX_RETRIES:
            try:
                if len(self.encoder.encode(query)) <= 8191:
                    embedding = self.oai.embeddings.create(input = [query], model=model).data[0].embedding
                else:
                    return []
            except Exception as e:
                retries += 1
                if retries == self.MAX_RETRIES: return []
        
        return embedding

    def get_definitions_from_top_k(self,top_k_matches):
        term_map = {}

        print("Top 10 Similar Phrases")
        print([x["id"] for x in top_k_matches["matches"]])
        print("-------")

        placeholders = ', '.join(["%s"] * len(top_k_matches["matches"]))
        formatted_term_ids = [x["id"] for x in top_k_matches["matches"]]
        stmt = f'SELECT * FROM terms WHERE term in ({placeholders})'
        self.cursor.execute(stmt,formatted_term_ids)

        rows = self.cursor.fetchall()
        for r in rows:
            term_map[r[1]] = r[2]

        return term_map

    def get_chat_response(self,user_input):
        
        user_input_vector = self.generate_embedding(user_input)
        term_map = self.get_definitions_from_top_k(self.pc_index.query(vector=user_input_vector, top_k=10, include_values=False))

        chat_prompt = ""

        for k,v in term_map.items():
            chat_prompt += f'{k} : {v} \n'

        chat_prompt += "Question: \n"
        chat_prompt += user_input

        print("Full Prompt")
        print(chat_prompt)
        print("-----")

        completion = self.oai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert on the Dune universe. Your soul purpose is to provide answers to any Dune related question. When asked a specific question, you will be provided supplementary contextual information to help you answer the question better. If you are asked about anything outside the scope of the Dune universe, politely mention your only purpose."},
                {"role": "user", "content": chat_prompt }
            ]
        )

        return completion.choices[0].message.content