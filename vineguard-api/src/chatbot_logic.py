import os
from litellm import completion
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el modelo configurado (por defecto usa gemini/gemini-1.5-flash si no se especifica)
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini/gemini-1.5-flash")

# Ventana de contexto: número máximo de TURNOS (user+bot) a conservar.
# Con 8 turnos (~2k tokens) + system prompt (~300) + respuesta (200) = ~2.5k tokens.
# Muy seguro para modelos de 8k tokens. Escalable: aumenta MAX_HISTORY_TURNS para LLMs mayores.
MAX_HISTORY_TURNS = 8

def build_system_prompt(language: str, last_scan: Optional[dict] = None) -> str:
    """Construye el system prompt inyectando el contexto del último diagnóstico si existe."""
    lang_label = "Español" if language == "es" else "Inglés"
    
    base_prompt = f"""Eres el Asistente Inteligente de VineGuard, un experto agrónomo especializado en viñedos.
Tu trabajo es ayudar a los agricultores a diagnosticar y tratar enfermedades de la hoja de vid,
específicamente: Podredumbre Negra (Black Rot), Esca (Sarampión Negro) y Tizón de la Hoja (Leaf Blight).

Debes responder siempre en idioma: {lang_label}.
Mantén tus respuestas breves, profesionales, prácticas y directas al grano (máximo 3-4 oraciones).
No uses formatos Markdown complejos, solo texto limpio con emojis ocasionales si lo ves conveniente."""

    if last_scan:
        disease = last_scan.get("predicted_class", "Desconocida")
        confidence = last_scan.get("confidence", 0) * 100
        scan_context = f"""

CONTEXTO DEL ÚLTIMO ANÁLISIS REALIZADO:
El sistema acaba de analizar una hoja de vid del agricultor y detectó: {disease} con una confianza del {confidence:.1f}%.
Si el agricultor te hace preguntas relacionadas con su cultivo o su situación actual, ten en cuenta este diagnóstico reciente.
No menciones este contexto a menos que sea relevante para la pregunta del usuario."""
        base_prompt += scan_context

    return base_prompt

def generate_chatbot_response(
    message: str,
    language: str = "es",
    history: Optional[list] = None,
    last_scan: Optional[dict] = None
) -> str:
    """
    Se comunica con el proveedor de IA usando LiteLLM.
    Maneja un historial de conversación con ventana deslizante para no superar el límite de tokens.
    
    Args:
        message: El mensaje actual del usuario.
        language: Idioma de respuesta ('es' o 'en').
        history: Lista de turnos anteriores [{"role": "user"|"assistant", "content": "..."}].
        last_scan: Resultado del último diagnóstico del escáner para inyectar como contexto.
    """
    system_prompt = build_system_prompt(language, last_scan)
    
    # Aplicar ventana deslizante: conservar solo los últimos N turnos del historial.
    # Esto garantiza que nunca superemos el límite de tokens del modelo, sin importar
    # cuántos mensajes acumule el usuario. Escalable: solo cambiar MAX_HISTORY_TURNS.
    safe_history = (history or [])[-MAX_HISTORY_TURNS * 2:]  # *2 porque cada turno = 2 mensajes
    
    messages = [
        {"role": "system", "content": system_prompt},
        *safe_history,
        {"role": "user", "content": message}
    ]
    
    try:
        response = completion(
            model=LITELLM_MODEL,
            messages=messages,
            temperature=0.3,
            max_tokens=250,
            api_key=os.getenv("LLM_API_KEY")
        )
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error en LiteLLM: {e}")
        if language == "es":
            return "Lo siento, tuve un problema de conexión con mi red neuronal principal. Por favor, verifica tus API Keys en el archivo .env del servidor FastAPI."
        return "Sorry, I had a connection issue with my main neural network. Please check your API Keys in the FastAPI .env file."


import requests

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Toma un archivo de audio (webm/mp3/wav) y usa la API de Groq (Whisper)
    para convertirlo a texto, saltándose las limitaciones del navegador en Linux.
    """
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("API Key no configurada. Imposible transcribir.")
        
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Preparamos el archivo como multipart/form-data
    files = {
        "file": ("audio.webm", audio_bytes, "audio/webm")
    }
    data = {
        "model": "whisper-large-v3-turbo",
        "language": "es"
    }
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        raise RuntimeError(f"Error de Whisper: {response.text}")
