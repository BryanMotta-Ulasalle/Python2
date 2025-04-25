# test.py
from sistema import Documento, GestorDocumentos, Cifrador

# Crear cifrador
cifrador = Cifrador()

# Crear documento
doc = Documento(1, "Contrato", "Este es un contrato confidencial")

# Cifrar contenido
doc.cifrarContenido(cifrador)
print("Contenido cifrado:", doc.contenido)

# Descifrar contenido
doc.descifrarContenido(cifrador)
print("Contenido descifrado:", doc.contenido)

# Probar gestor
gestor = GestorDocumentos()
gestor.agregarDocumento(doc)

doc_encontrado = gestor.buscarDocumento(1)
print("Documento encontrado:", doc_encontrado.titulo)
