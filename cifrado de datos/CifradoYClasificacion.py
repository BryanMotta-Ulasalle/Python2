# Importar librerías necesarias
from cryptography.fernet import Fernet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# =========================
# Parte 1: Clases para manejo de documentos
# =========================

class Documento:
    def __init__(self, nombre, contenido):
        self.nombre = nombre
        self.contenido = contenido
        self.tipo = None  # Tipo del documento: se llenará con la clasificación

    def set_tipo(self, tipo):
        self.tipo = tipo

class GestorDocumentos:
    def __init__(self, clave_secreta):
        self.documentos = []
        self.clave_secreta = clave_secreta
        self.cipher_suite = Fernet(clave_secreta)

    def agregar_documento(self, documento):
        self.documentos.append(documento)

    def cifrar_documento(self, documento):
        contenido_bytes = documento.contenido.encode('utf-8')
        contenido_cifrado = self.cipher_suite.encrypt(contenido_bytes)
        documento.contenido = contenido_cifrado

    def descifrar_documento(self, documento):
        contenido_descifrado = self.cipher_suite.decrypt(documento.contenido).decode('utf-8')
        return contenido_descifrado

# =========================
# Parte 2: Modelo de IA para Clasificación
# =========================

class ClasificadorDocumentos:
    def __init__(self):
        # Datos de entrenamiento simples
        self.documentos_entrenamiento = [
            "Contrato de prestación de servicios",
            "Informe de resultados anuales",
            "Reporte de incidentes técnicos"
        ]
        self.etiquetas_entrenamiento = [
            "Contrato",
            "Informe",
            "Reporte"
        ]
        self.vectorizador = TfidfVectorizer(stop_words='english')
        X = self.vectorizador.fit_transform(self.documentos_entrenamiento)
        
        self.modelo = MultinomialNB()
        self.modelo.fit(X, self.etiquetas_entrenamiento)

    def predecir_tipo(self, contenido_descifrado):
        X_new = self.vectorizador.transform([contenido_descifrado])
        prediccion = self.modelo.predict(X_new)[0]
        return prediccion

# =========================
# Parte 3: Función para cargar un documento desde archivo
# =========================

def cargar_documento_desde_archivo(ruta_archivo):
    """Lee el contenido de un archivo de texto y devuelve su contenido"""
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    return contenido

# =========================
# Parte 4: Uso del sistema
# =========================

def main():
    # 1. Generar clave secreta para cifrado
    clave = Fernet.generate_key()

    # 2. Instanciar gestor y clasificador
    gestor = GestorDocumentos(clave)
    clasificador = ClasificadorDocumentos()

    # 3. Ruta del archivo a importar
    ruta = "c:\\Users\\Usuario\\Desktop\\python\\cifrado de datos\\documento_ejemplo.txt"  # Cambia el nombre si tu archivo tiene otro nombre

    # 4. Cargar el contenido desde el archivo
    contenido_importado = cargar_documento_desde_archivo(ruta)

    # 5. Crear el documento en base al archivo
    doc_nuevo = Documento(ruta, contenido_importado)

    # 6. Clasificar el documento
    tipo_doc = clasificador.predecir_tipo(doc_nuevo.contenido)
    doc_nuevo.set_tipo(tipo_doc)

    # 7. Cifrar el contenido del documento
    gestor.cifrar_documento(doc_nuevo)

    # 8. Agregar el documento al gestor
    gestor.agregar_documento(doc_nuevo)

    # 9. Mostrar resultados
    print(f"\n📄 Documento: {doc_nuevo.nombre}")
    print(f"🔖 Clasificado como: {doc_nuevo.tipo}")
    print(f"🔒 Contenido cifrado: {doc_nuevo.contenido}")

    # 10. (Opcional) Descifrar y mostrar el contenido original
    contenido_original = gestor.descifrar_documento(doc_nuevo)
    print(f"\n🔓 Contenido descifrado:")
    print(contenido_original)

if __name__ == "__main__":
    main()
