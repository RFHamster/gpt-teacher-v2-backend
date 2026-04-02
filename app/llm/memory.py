import psycopg
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from app.core.config import settings

DB_URI = str(settings.SQLALCHEMY_DATABASE_URI).replace("+psycopg", "")

_conn = None
_checkpointer = None
_store = None

def get_db_resources():
    global _conn, _checkpointer, _store
    
    if _conn is None or _conn.closed:
        _conn = psycopg.connect(DB_URI)
        _conn.autocommit = True
        _checkpointer = PostgresSaver(_conn)
        _checkpointer.setup()
        _store = PostgresStore(_conn)
        _store.setup()
    return _checkpointer, _store