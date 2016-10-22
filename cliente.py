###### Esta es la parte del cliente
from xmlrpc.client import ServerProxy
s = ServerProxy("http://127.0.0.1:8000")
# Manda a llamar a la función 'saludame' del servidor
print(s.ping())
print(s.yo_juego())
print(s.estado_del_juego())
#s.camba_direccion(0,2)