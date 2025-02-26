import redis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query


# Conexión a Redis
redis_client = redis.Redis(
    host="redis-19029.c16.us-east-1-3.ec2.redns.redis-cloud.com",
    port=19029,
    password="POC_Telcel",
    decode_responses=True 
)

def crear_indice(client):
    index_name = 'idx:cliente'
    index = client.ft(index_name)
    try:
        index.info()
    except:
        print("Creando índice...")
        schema = (
            TextField("Nombre"),
            TextField("Perfil"),
            TextField("Telefono"),
            NumericField("Saldo_estimado", sortable=True),
            NumericField("Saldo_facturado", sortable=True)
        )
        index.create_index(schema, definition = IndexDefinition(prefix=["cli:"]))
        print("Índice creado exitosamente.")
'''
def buscar(query):
    try:
        result = search_client.search(query)
        return result.docs
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return []
'''

def search(client, query):
    index = client.ft("idx:cliente")
    try:
        results = index.search(query)
        return [doc.__dict__ for doc in results.docs]

    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return []
    
if __name__ == "__main__":
    crear_indice(redis_client)
    print(search(redis_client, "John"))
