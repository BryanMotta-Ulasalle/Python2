# sistema.py
from cryptography.fernet import Fernet

class Documento:
    def __init__(self, id, titulo, contenido):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.tipo = None

    def cifrarContenido(self, cifrador):
        self.contenido = cifrador.cifrar(self.contenido)

    def descifrarContenido(self, cifrador):
        self.contenido = cifrador.descifrar(self.contenido)

class Cifrador:
    def __init__(self):
        self.clave = Fernet.generate_key()
        self.fernet = Fernet(self.clave)

    def cifrar(self, texto):
        return self.fernet.encrypt(texto.encode()).decode()

    def descifrar(self, texto_cifrado):
        return self.fernet.decrypt(texto_cifrado.encode()).decode()

class GestorDocumentos:
    def __init__(self):
        self.documentos = []

    def agregarDocumento(self, doc):
        self.documentos.append(doc)

    def buscarDocumento(self, id):
        return next((d for d in self.documentos if d.id == id), None)
