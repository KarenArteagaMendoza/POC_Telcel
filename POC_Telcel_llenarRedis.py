import redis
import csv

try: 
    redis_client = redis.Redis(
        host="redis-19029.c16.us-east-1-3.ec2.redns.redis-cloud.com",
        port=19029,
        password="POC_Telcel",
        decode_responses=True 
    )
    print("Connectado a: ", redis_client.get_connection_kwargs())
except:
    print("Falló la conexión")


def cargar_csv(nombre):
    with open(nombre, 'r', newline='', encoding='utf-8') as archivo_csv:
        archivo = csv.reader(archivo_csv)
        for dato in archivo:
            redis_client.hset(f"cli:{dato[0]}", mapping={"Nombre": dato[1],"Telefono": dato[2], "Perfil": dato[3],"Saldo_estimado": dato[4],"Saldo_facturado": dato[5]})


if __name__ == '__main__':
    print("prueba: ", redis_client.get("prueba"))
    cargar_csv("Cliente.csv")
    print("Datos cargados a Redis")