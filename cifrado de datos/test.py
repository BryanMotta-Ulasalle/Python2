# test.py
from sistema import Documento, GestorDocumentos, Cifrador

# Ejemplo de cómo utilizar las clases:

# 1. Crear un objeto Cifrador para manejar el cifrado
cifrador = Cifrador()

# 2. Crear un documento con un ID, título y contenido
doc = Documento(1, "Contrato", "Este es un contrato confidencial")

# 3. Cifrar el contenido del documento usando el cifrador
doc.cifrarContenido(cifrador)
print("Contenido cifrado:", doc.contenido)  # Mostrar el contenido cifrado

# 4. Descifrar el contenido del documento usando el cifrador
doc.descifrarContenido(cifrador)
print("Contenido descifrado:", doc.contenido)  # Mostrar el contenido original

# 5. Crear un gestor de documentos para manejar múltiples documentos
gestor = GestorDocumentos()

# 6. Agregar el documento creado al gestor
gestor.agregarDocumento(doc)

# 7. Buscar el documento por su ID (1) y mostrar su título
doc_encontrado = gestor.buscarDocumento(1)
print("Documento encontrado:", doc_encontrado.titulo)
print("Documento encontrado:", doc_encontrado.titulo)
