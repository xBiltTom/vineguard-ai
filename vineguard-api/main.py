from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Importaciones locales
from src.inference import predict_from_bytes, load_production_model
from src.chatbot_logic import generate_chatbot_response

app = FastAPI(
    title="VineGuard API",
    description="Backend API para el sistema de diagnóstico de viñedos",
    version="1.0.0"
)

# Configurar CORS (Para que el Frontend Next.js pueda comunicarse sin errores)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción deberías poner ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== MODELOS DE DATOS ====
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    language: str = "es"
    # Historial de conversación (ventana deslizante gestionada en el backend)
    history: list[ChatMessage] = []
    # Contexto del último escaneo (opcional, inyectado silenciosamente al system prompt)
    last_scan: dict | None = None

# ==== EVENTOS DE INICIO ====
@app.on_event("startup")
async def startup_event():
    # Intentar cargar el modelo al iniciar el servidor
    # Esto evitará que la primera petición demore mucho tiempo
    load_production_model()

# ==== ENDPOINTS ====

@app.get("/")
def root():
    return {"message": "Bienvenido a VineGuard API. Usa /docs para ver la documentación."}

@app.get("/health")
def health_check():
    """Verifica el estado del servidor y del modelo."""
    import os
    from src.inference import MODEL_CACHE, get_model_path
    
    is_model_loaded = MODEL_CACHE is not None
    model_exists = os.path.exists(get_model_path())
    
    return {
        "status": "online",
        "model_loaded": is_model_loaded,
        "model_file_exists": model_exists,
        "model_path": get_model_path()
    }

@app.post("/api/predict")
async def predict_disease(image: UploadFile = File(...)):
    """
    Recibe una imagen (JPG/PNG), la preprocesa y la evalúa usando el mejor modelo (.h5) de producción.
    Devuelve la clase detectada, la confianza y el tiempo de inferencia.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen válida.")
        
    try:
        contents = await image.read()
        resultado = predict_from_bytes(contents)
        return resultado
    except RuntimeError as re:
        raise HTTPException(status_code=503, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_bot(request: ChatRequest):
    """
    Recibe un mensaje del agricultor con su historial y devuelve una respuesta agronómica.
    Soporta contexto del último escaneo para respuestas personalizadas.
    """
    try:
        # Convertir los objetos ChatMessage a dicts para LiteLLM
        history_dicts = [{"role": m.role, "content": m.content} for m in request.history]
        response = generate_chatbot_response(
            message=request.message,
            language=request.language,
            history=history_dicts,
            last_scan=request.last_scan
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe_voice(audio: UploadFile = File(...)):
    """
    Recibe un archivo de audio del frontend y lo transcribe usando Groq Whisper.
    Esta es la alternativa profesional a la Web Speech API que falla en Linux.
    """
    from src.chatbot_logic import transcribe_audio
    try:
        contents = await audio.read()
        texto = transcribe_audio(contents)
        return {"text": texto}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
