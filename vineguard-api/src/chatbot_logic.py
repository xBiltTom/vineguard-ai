import os
from litellm import completion
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el modelo configurado (por defecto usa gemini/gemini-1.5-flash si no se especifica)
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini/gemini-1.5-flash")

def generate_chatbot_response(message: str, language: str = "es") -> str:
    """
    Se comunica con el proveedor de IA (OpenAI, Google, Anthropic, etc.) usando LiteLLM.
    El proveedor dependerá del API Key configurado en el archivo .env.
    """
    
    # Prompt del Sistema: Le da personalidad agronómica a la IA
    system_prompt = f"""
    Eres el Asistente Inteligente de VineGuard, un experto agrónomo especializado en viñedos.
    Tu trabajo es ayudar a los agricultores a diagnosticar y tratar enfermedades de la hoja de vid,
    específicamente: Podredumbre Negra (Black Rot), Esca (Sarampión Negro) y Tizón de la Hoja (Leaf Blight).
    
    Debes responder siempre en idioma: {'Español' if language == 'es' else 'Inglés'}.
    Mantén tus respuestas breves, profesionales, prácticas y directas al grano (máximo 3-4 oraciones).
    No uses formatos Markdown complejos, solo texto limpio con emojis ocasionales si lo ves conveniente.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    
    try:
        # LiteLLM unifica todos los proveedores bajo la sintaxis de OpenAI
        response = completion(
            model=LITELLM_MODEL,
            messages=messages,
            temperature=0.3, # Baja temperatura para respuestas más técnicas y precisas
            max_tokens=200,
            api_key=os.getenv("LLM_API_KEY")
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error en LiteLLM: {e}")
        error_msg = "Lo siento, tuve un problema de conexión con mi red neuronal principal. "
        error_msg += "Por favor, verifica tus API Keys en el archivo .env del servidor FastAPI." if language == "es" else "Please check your API Keys in the FastAPI .env file."
        return error_msg

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
