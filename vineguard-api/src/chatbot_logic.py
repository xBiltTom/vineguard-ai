"""
Lógica simple de Chatbot Agronómico.
En una versión de producción avanzada, esto se conectaría a la API de OpenAI o Gemini.
Para este proyecto universitario, implementamos un sistema basado en heurísticas (keywords) 
o respuestas pre-programadas para asistir al agricultor.
"""

def generate_chatbot_response(message: str, language: str = "es") -> str:
    message = message.lower().strip()
    
    # === RESPUESTAS EN ESPAÑOL ===
    if language == "es":
        if "hola" in message or "saludo" in message:
            return "¡Hola! Soy el Asistente Inteligente de VineGuard. ¿En qué te puedo ayudar hoy con tu viñedo?"
        
        elif "esca" in message or "sarampion" in message:
            return "El Esca (o Sarampión Negro) es una enfermedad compleja del tronco muy grave. Te recomiendo no aplicar químicos agresivos ya que están prohibidos. Lo mejor es realizar una 'Cirugía del Tronco' o poda tardía usando pastas cicatrizantes biológicas (Trichoderma)."
            
        elif "podredumbre" in message or "black rot" in message or "negra" in message:
            return "La Podredumbre Negra es causada por el hongo Guignardia bidwellii. Si tu modelo lo detectó, retira urgentemente las 'bayas momificadas' y aplica fungicidas sistémicos como Miclobutanil. ¡No uses riego por aspersión!"
            
        elif "tizon" in message or "blight" in message or "hoja" in message and "amarilla" in message:
            return "El Tizón de la Hoja es tratable con Caldo Bordelés o fungicidas sistémicos. Asegúrate de mejorar el drenaje del suelo y no excederte con el nitrógeno."
            
        elif "gracias" in message:
            return "¡De nada! Recuerda que un viñedo bien monitoreado es un viñedo productivo. ¡Mucho éxito en la cosecha!"
            
        elif "ayuda" in message or "que puedes hacer" in message:
            return "Puedo explicarte cómo tratar las enfermedades que detecte la IA (Esca, Podredumbre Negra, Tizón). Solo pregúntame sobre alguna enfermedad."
            
        else:
            return "Interesante pregunta agronómica. Como asistente base, mi especialidad actual es el tratamiento de enfermedades foliares (Esca, Tizón, Podredumbre). ¿Quieres saber sobre alguna de ellas?"
            
    # === RESPUESTAS EN INGLÉS ===
    else:
        if "hello" in message or "hi" in message:
            return "Hello! I'm the VineGuard Intelligent Assistant. How can I help you with your vineyard today?"
            
        elif "esca" in message or "measles" in message:
            return "Esca is a complex and severe trunk disease. Chemical eradication is largely banned. I recommend Trunk Surgery and using biological wound protectants (like Trichoderma) during late pruning."
            
        elif "rot" in message or "black" in message:
            return "Black Rot is caused by Guignardia bidwellii. Urgently remove mummified berries and apply systemic fungicides like Myclobutanil. Avoid sprinkler irrigation!"
            
        elif "blight" in message:
            return "Leaf Blight is treatable with copper-based fungicides. Ensure good soil drainage and avoid excess nitrogen fertilization."
            
        elif "thanks" in message or "thank" in message:
            return "You're welcome! Remember, a well-monitored vineyard is a productive one. Good luck with the harvest!"
            
        elif "help" in message:
            return "I can explain how to treat the diseases detected by the AI (Esca, Black Rot, Blight). Just ask me about any of them."
            
        else:
            return "Interesting question. As a baseline assistant, my specialty is foliar disease treatment (Esca, Blight, Black Rot). Would you like to know about any of them?"
