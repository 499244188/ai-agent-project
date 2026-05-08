import psycopg2
from config import settings
from pgvector.psycopg2 import register_vector
from openai import OpenAI



conn = None
emb_client=None
cursor = None



def init_database():
    global conn,emb_client,cursor
    # PostgreSQL 链接
    conn = psycopg2.connect(
        host = settings.pg_host,
        port = settings.pg_port,
        user = settings.pg_user,
        password = settings.pg_password,
        dbname = settings.pg_db
    )

    # Embedding 客户端（阿里DashScope)
    emb_client = OpenAI(
        api_key=settings.al_em_key,
        base_url=settings.al_em_url
    )

    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    register_vector(conn)

    # 创建表（先删旧的，因为之前 03_pgvector.py 建的表没有 person 列）
    cursor.execute("DROP TABLE IF EXISTS documents CASCADE")
    cursor.execute("""
            CREATE TABLE documents(
                id SERIAL PRIMARY KEY,
                content TEXT,
                person TEXT,
                embedding vector(1024)
                )
    """)
    conn.commit()

    print("数据库链接成功")

# 获取 Embedding
def get_embedding(text:str)->list:
    response = emb_client.embeddings.create(
        model=settings.al_em_mode,
        input=text
    )
    return response.data[0].embedding

# 存入向量库
def store_document(content:str,person:str=""):
    embedding = get_embedding(content)
    cursor.execute(
        "INSERT INTO documents (content,person,embedding) VALUES (%s, %s, %s)",
        (content,person,embedding)
    )
    conn.commit()



# 工具1 向量搜索
def search_documents(query:str,top_k:int=3)->list:
    query_embedding = get_embedding(query)
    cursor.execute(
        """
        SELECT content,person,embedding<=> %s::vector as distance
        FROM documents
        ORDER BY distance
        LIMIT %s
        """,[str(query_embedding),top_k]
    )
    # return cursor.fetchall()
    # return cursor.fetchone()
    result =  cursor.fetchall()
    return "\n".join(f"[{r[1]}]{r[0]}" for r in result)




