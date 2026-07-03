# Importamos la clase Base común para que esté disponible de manera unificada
from app.database.session import Base

from app.models.post import Post  # noqa
from app.models.trend import TrendAggregated  # noqa
# NOTA PARA EL FUTURO:
# Cuando creemos las tablas en la carpeta 'models/', las importaremos aquí 
# para que SQLAlchemy/Alembic las reconozca al arrancar.
# Ejemplo: from app.models.post import Post  # noqa