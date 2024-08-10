import pymysql
import os
import json
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

load_dotenv()

sql_url = os.environ.get("MYSQL_URL")
parsed_url = urlparse(sql_url)


conn = pymysql.connect(
    host=parsed_url.hostname,
    user=unquote(parsed_url.username),
    password=unquote(parsed_url.password),
    port=parsed_url.port,
    database=parsed_url.path[1:]
)
cursor = conn.cursor()

rows = []
with open("../data/content.json", "r") as f:
    data = json.load(f)
    for k,v in data.items():
        rows.append((k,v["description"],v["wiki"]))

for term,definition,wiki_link in rows:
    stmt = "INSERT INTO terms (term,definition,wiki_link) VALUES (%s, %s, %s)"
    cursor.execute(stmt, (term,definition,wiki_link))
    conn.commit()