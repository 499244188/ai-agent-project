from agent import run_agent
from tools.search import store_document,init_database


init_database()
# 测试
print("\n===先存如几条数据====")
store_document("Python 大蟒蛇，很让人害怕的蛇类，火影忍者中有这个", "wiki")
store_document("PostgreSQL是最流行的开源关系型数据库", "wiki")
store_document("pgvector让PostgreSQL支持向量搜索", "wiki")

run_agent()