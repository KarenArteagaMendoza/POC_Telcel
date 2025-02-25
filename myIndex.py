
import redis
import time
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.aggregation import AggregateRequest, Asc, Desc


def connect_to_redis():
    try:
        redis_client = redis.Redis( host="localhost", port=12000, password="test", decode_responses=True)
        print("Conexión exitosa con Redis")
        crear_indice(redis_client) 
        search(redis_client, "net")
        return redis_client
    except redis.ConnectionError as e:
        print(f"Error: No se pudo establecer la conexión con Redis - {e}")
        return None

def crear_indice(client):
    index_name = 'idx:cliente'
    index = client.ft(index_name)
    try:
        index.info()
    except:
        print("Creando índice...")
        schema = (NumericField('id', sortable=True), 
                  TextField('Nombre', weight=1), 
                  TextField('Perfil', weight=1),
                  NumericField('Saldo_estimado', sortable=True),
                  NumericField('Saldo_facturado', sortable=True) )
        client.ft(index_name).create_index(schema, definition=IndexDefinition(prefix=['cliente:']))
        print("Índice creado exitosamente.")
        time.sleep(1)

def search(client, query):
    index = client.ft("idx:cache")
    results = index.search(Query("@data:"+ query).paging(offset=0)).docs
    return results

def tryIndex():    
    # Connect to Redis
    redis_client = connect_to_redis() #Conexión con Redis (Función)

    # Perform operations with the connections, if successful
    if redis_client:
        time.sleep(1)
        print("Cerrando conexión con Redis ...")
        redis_client.close()

if __name__ == "__main__":
    tryIndex()