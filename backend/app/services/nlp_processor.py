import re
from textblob import TextBlob

class NlpProcessorService:
    @staticmethod
    def limpiar_texto(texto: str) -> str:
        """Remueve enlaces, menciones y ruido del texto de las redes sociales."""
        # Eliminar URLs
        texto = re.sub(r"http\s+", "", texto)
        texto = re.sub(r"https\s+", "", texto)
        # Eliminar menciones (@usuario)
        texto = re.sub(r"@\w+", "", texto)
        # Eliminar espacios en blanco duplicados y limpiar extremos
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto

    @staticmethod
    def analizar_sentimiento_y_relevancia(texto_original: str) -> dict:
        """Procesa el texto y calcula las variables analíticas de la IA."""
        texto_limpio = NlpProcessorService.limpiar_texto(texto_original)
        
        # Análisis probabilístico de polaridad emocional (-1.0 a 1.0)
        analysis = TextBlob(texto_limpio)
        polaridad = analysis.sentiment.polarity

        # Clasificación estricta del sentimiento y confianza simulada
        if polaridad > 0.15:
            sentimiento = "Positivo"
            confidence = min(0.5 + (polaridad * 0.5), 0.98)
        elif polaridad < -0.15:
            sentimiento = "Negativo"
            confidence = min(0.5 + (abs(polaridad) * 0.5), 0.99)
        else:
            sentimiento = "Neutral"
            confidence = min(0.6 + (abs(polaridad)), 0.85)

        # Algoritmo de Relevancia (Impacto Estratégico de 0 a 10)
        # Se calcula basándose en la densidad del mensaje y la intensidad de la emoción
        longitud_score = min(len(texto_limpio) / 40, 4.0)
        intensidad_emocional = abs(polaridad) * 6.0
        relevancia = round(min(longitud_score + intensidad_emocional, 10.0), 1)
        
        # Asegurar un piso mínimo de relevancia para evitar valores nulos
        if relevancia < 1.0:
            relevancia = round(1.0 + longitud_score, 1)

        return {
            "texto_limpio": texto_limpio,
            "sentimiento": sentimiento,
            "confidence": round(confidence, 2),
            "relevancia": relevancia
        }