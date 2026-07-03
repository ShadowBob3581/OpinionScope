import random
import time
from sqlalchemy.orm import Session
from app.models.post import Post
from app.services.nlp_processor import NlpProcessorService

# Banco de datos de simulación reactiva sobre el entorno tecnológico/académico
DATA_POOL = [
    {"user": "@ingenieria_tes", "text": "Excelente organización en el Encuentro de Ingeniería Informática de este año. Aprendizaje total. 🚀"},
    {"user": "@cyber_hunter", "text": "¡Alerta! Detectado un fallo masivo en las configuraciones de CORS de múltiples APIs gubernamentales. Cuidado ahí."},
    {"user": "@gerardo_dev", "text": "Diseñando una arquitectura limpia con FastAPI y React. La fluidez de los WebSockets a gran escala es impresionante. 💻"},
    {"user": "@tech_analyst", "text": "Pésimo rendimiento del proveedor de la base de datos hoy, la latencia se elevó en producción y congeló los gráficos. 😡"},
    {"user": "@user_99", "text": "No me convence la nueva actualización de la aplicación, la UI se siente sobrecargada y el tiempo de respuesta es lento. 👎"},
    {"user": "@data_science_mx", "text": "Los modelos de NLP en español han mejorado una barbaridad gracias a las arquitecturas de Transformers de Hugging Face."},
    {"user": "@dev_security", "text": "Implementando simulaciones de ingeniería social para capacitar a estudiantes de preparatoria en privacidad de datos. 🛡️"},
    {"user": "@cloud_master", "text": "La transición de servidores locales hacia contenedores Docker automatizados reduce los errores de despliegue a cero."}
]

class ScraperAgentService:
    @staticmethod
    def ejecutar_ingesta_unitaria(db: Session) -> Post:
        """ Simula la captura en tiempo real de un tweet, lo procesa con la IA 
            y lo guarda inmediatamente en la base de datos.
        """
        # 1. Simular la llegada del post del Stream
        muestra = random.choice(DATA_POOL)
        
        # 2. Consumir el procesador NLP para clasificar las métricas
        analisis = NlpProcessorService.analizar_sentimiento_y_relevancia(muestra["text"])
        
        # 3. Mapear al modelo ORM de SQLAlchemy
        nuevo_post = Post(
            red_social="X (Twitter)",
            usuario=muestra["user"],
            texto=muestra["text"],
            sentimiento=analisis["sentimiento"],
            nlp_confidence=analisis["confidence"],
            relevancia=analisis["relevancia"]
        )
        
        # 4. Guardar permanentemente en la base de datos
        db.add(nuevo_post)
        db.commit()
        db.refresh(nuevo_post)
        
        return nuevo_post