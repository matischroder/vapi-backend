import uvicorn
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el puerto desde la variable de entorno
port = int(os.getenv("PORT", 5050))

if __name__ == "__main__":
    # Exclude virtual environment from watch files
    import sys
    from pathlib import Path

    venv_path = Path(sys.executable).parent.parent
    watch_dirs = [d for d in [str(venv_path), "."] if d != str(venv_path)]

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=watch_dirs,
    )
