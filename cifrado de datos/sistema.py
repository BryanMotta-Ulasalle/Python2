# Importamos la librería 'Fernet' para realizar el cifrado y descifrado simétrico
from cryptography.fernet import Fernet

# Definimos la clase Documento
class Documento:
    # El constructor de la clase recibe un id, título, contenido y tipo de documento
    def __init__(self, id, titulo, contenido):
        self.id = id               # Identificador único del documento
        self.titulo = titulo       # Título del documento
        self.contenido = contenido # Contenido del documento (por ejemplo: texto plano)
        self.tipo = None           # Tipo de documento (por ejemplo: contrato, informe)

    # Método para cifrar el contenido del documento
    def cifrarContenido(self, cifrador):
        # Cifra el contenido del documento usando el objeto 'cifrador' (instancia de la clase Cifrador)
        self.contenido = cifrador.cifrar(self.contenido)

    # Método para descifrar el contenido del documento
    def descifrarContenido(self, cifrador):
        # Descifra el contenido del documento usando el objeto 'cifrador'
        self.contenido = cifrador.descifrar(self.contenido)


# Definimos la clase Cifrador
class Cifrador:
    # El constructor de la clase genera una clave aleatoria para cifrado
    def __init__(self):
        # Generamos una clave secreta utilizando Fernet (parte del cifrado simétrico)
        self.clave = Fernet.generate_key()   
        # Creamos un objeto Fernet con la clave generada
        self.fernet = Fernet(self.clave)

    # Método para cifrar un texto
    def cifrar(self, texto):
        # 'texto.encode()' convierte el texto a formato de bytes, necesario para cifrarlo
        # 'fernet.encrypt()' cifra el texto y devuelve el texto cifrado
        # 'decode()' convierte el texto cifrado de vuelta a string para su visualización
        return self.fernet.encrypt(texto.encode()).decode()

    # Método para descifrar un texto cifrado
    def descifrar(self, texto_cifrado):
        # 'texto_cifrado.encode()' convierte el texto cifrado a bytes
        # 'fernet.decrypt()' descifra el texto
        # 'decode()' convierte el texto descifrado a string para su visualización
        return self.fernet.decrypt(texto_cifrado.encode()).decode()


# Definimos la clase GestorDocumentos para gestionar una lista de documentos
class GestorDocumentos:
    # Constructor de la clase, que inicializa una lista vacía de documentos
    def __init__(self):
        self.documentos = []  # Lista para almacenar documentos

    # Método para agregar un documento a la lista
    def agregarDocumento(self, doc):
        self.documentos.append(doc)  # Agrega el documento a la lista

    # Método para buscar un documento por su ID
    def buscarDocumento(self, id):
        # Usa una expresión generadora para buscar el documento con el ID dado
        # Si lo encuentra, lo devuelve; si no, devuelve None
        return next((d for d in self.documentos if d.id == id), None)