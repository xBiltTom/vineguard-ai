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
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error en LiteLLM: {e}")
        error_msg = "Lo siento, tuve un problema de conexión con mi red neuronal principal. "
        error_msg += "Por favor, verifica tus API Keys en el archivo .env del servidor FastAPI." if language == "es" else "Please check your API Keys in the FastAPI .env file."
        return error_msg
