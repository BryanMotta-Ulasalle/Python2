import os
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
        self.tipo = None

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

class ClasificadorDocumentos:
    def __init__(self):
        self.documentos_entrenamiento = [
    "Contrato de prestación de servicios entre la empresa XYZ y el proveedor ABC.",
    "Informe de resultados de ventas del año 2024.",
    "Reporte de incidentes técnicos del 15 de marzo de 2025.",
    "Contrato de arrendamiento entre Juan Pérez y la empresa XYZ.",
    "Informe anual de resultados de la empresa ABC.",
    "Reporte de fallas en el sistema de base de datos."
    ]
        self.etiquetas_entrenamiento = [
    "Contrato",
    "Informe",
    "Reporte",
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
# Parte 2: Funciones para cargar varios documentos
# =========================

def cargar_documentos_desde_carpeta(ruta_carpeta):
    """Lee todos los archivos .txt de una carpeta y devuelve una lista de (nombre, contenido)"""
    documentos = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            documentos.append((nombre_archivo, contenido))
    return documentos

# =========================
# Parte 3: Uso del sistema
# =========================

def main():
    # 1. Generar clave secreta
    clave = Fernet.generate_key()

    # 2. Instanciar gestor y clasificador
    gestor = GestorDocumentos(clave)
    clasificador = ClasificadorDocumentos()

    # 3. Ruta de la carpeta donde están los documentos
    ruta_carpeta = "C:\\Users\\Usuario\\Desktop\\python\\cifrado de datos\\documentos"
  # Carpeta donde debes tener tus .txt

    # 4. Cargar todos los documentos de la carpeta
    documentos_importados = cargar_documentos_desde_carpeta(ruta_carpeta)

    if not documentos_importados:
        print("⚠️ No se encontraron documentos en la carpeta.")
        return

    # 5. Procesar cada documento
    for nombre, contenido in documentos_importados:
        doc = Documento(nombre, contenido)

        # Clasificar
        tipo_doc = clasificador.predecir_tipo(doc.contenido)
        doc.set_tipo(tipo_doc)

        # Cifrar
        gestor.cifrar_documento(doc)

        # Agregar al gestor
        gestor.agregar_documento(doc)

        # Mostrar resultados
        print(f"\n📄 Documento: {doc.nombre}")
        print(f"🔖 Clasificado como: {doc.tipo}")
        print(f"🔒 Contenido cifrado: {doc.contenido[:50]}...")  # Mostrar solo un fragmento

    print(f"\n✅ Se procesaron {len(gestor.documentos)} documentos correctamente.")

if __name__ == "__main__":
    main()
