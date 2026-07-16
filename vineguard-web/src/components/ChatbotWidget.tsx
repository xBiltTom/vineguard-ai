"use client";

import { useState, useRef, useEffect } from "react";
import { MessageSquare, X, Send, Mic, MicOff, Bot, User, Loader2 } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useScan } from "@/contexts/ScanContext";

interface ChatMessage {
  role: "user" | "bot" | "assistant";
  content: string;
}

export default function ChatbotWidget() {
  const { t, language } = useLanguage();
  const { lastScan } = useScan();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "bot", content: "¡Hola! Soy VineGuard AI. ¿Tienes alguna pregunta sobre el cuidado de tu viñedo?" }
  ]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Update initial message when language changes
  useEffect(() => {
    setMessages([{ role: "bot", content: t("chat_welcome") }]);
  }, [language]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const toggleListen = async () => {
    if (isListening) {
      // Detener grabación
      mediaRecorderRef.current?.stop();
      setIsListening(false);
      mediaRecorderRef.current?.stream.getTracks().forEach(track => track.stop());
    } else {
      // Iniciar grabación
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        audioChunksRef.current = [];

        mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            audioChunksRef.current.push(e.data);
          }
        };

        mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
          await handleAudioTranscription(audioBlob);
        };

        mediaRecorder.start();
        setIsListening(true);
      } catch (error) {
        console.error("Error accessing microphone:", error);
        setMessages(prev => [...prev, { 
          role: "bot", 
          content: t("error_mic_access")
        }]);
      }
    }
  };

  const handleAudioTranscription = async (audioBlob: Blob) => {
    setIsTranscribing(true);
    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.webm");

    try {
      const response = await fetch("http://localhost:8000/api/transcribe", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Transcription failed");
      
      const data = await response.json();
      if (data.text) {
        setInputText(data.text);
      }
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: "bot", 
        content: t("error_api_conn")
      }]);
    } finally {
      setIsTranscribing(false);
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = inputText.trim();
    setInputText("");
    
    // Snapshot del historial ANTES de agregar el nuevo mensaje del usuario
    const historySnapshot = messages
      .filter(m => m.role !== "bot" || messages.indexOf(m) !== 0) // excluir mensaje de bienvenida estático
      .map(m => ({
        role: m.role === "bot" ? "assistant" : "user",
        content: m.content
      }));
    
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          language: language,
          history: historySnapshot,        // <- Historial con ventana deslizante
          last_scan: lastScan ?? null      // <- Contexto del último diagnóstico
        })
      });

      if (!response.ok) throw new Error("API Error");

      const data = await response.json();
      setMessages(prev => [...prev, { role: "bot", content: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "bot", content: t("error_api_conn") }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-8 right-8 w-14 h-14 bg-[var(--accent)] text-[#121513] rounded-full flex items-center justify-center shadow-lg hover:scale-105 transition-transform z-50 focus:outline-none print:hidden"
        >
          <MessageSquare className="w-6 h-6" />
        </button>
      )}

      {isOpen && (
        <div className="fixed bottom-8 right-8 w-[350px] sm:w-[400px] h-[500px] bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl shadow-2xl flex flex-col z-50 overflow-hidden print:hidden">
          
          <div className="bg-[#121513] px-4 py-3 flex justify-between items-center border-b border-[var(--border-color)]">
            <div className="flex items-center gap-2 text-white">
              <Bot className="w-5 h-5 text-[var(--accent)]" />
              <span className="font-medium text-sm">{t("chat_assistant_title")}</span>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[var(--background)]">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`flex gap-2 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-[#2D3330] text-white' : 'bg-[var(--accent)] text-[#121513]'}`}>
                    {msg.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>
                  
                  <div className={`px-4 py-2 rounded-xl text-sm ${msg.role === 'user' ? 'bg-[#2D3330] text-white rounded-tr-none' : 'bg-[var(--card-bg)] border border-[var(--border-color)] rounded-tl-none text-[var(--foreground)]'}`}>
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="flex gap-2 items-center bg-[var(--card-bg)] border border-[var(--border-color)] px-4 py-2 rounded-xl rounded-tl-none">
                  <div className="flex gap-1">
                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="p-3 border-t border-[var(--border-color)] bg-[var(--card-bg)] flex items-center gap-2">
            
            <button 
              onClick={toggleListen}
              disabled={isTranscribing}
              className={`p-2 rounded-full transition-colors relative ${isListening ? 'bg-red-500/20 text-red-500' : 'bg-[var(--background)] text-gray-400 hover:text-[var(--accent)]'}`}
              title="Voice Dictation"
            >
              {isTranscribing ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : isListening ? (
                <Mic className="w-5 h-5 animate-pulse" />
              ) : (
                <MicOff className="w-5 h-5" />
              )}
            </button>

            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={isTranscribing ? t("chat_transcribing") : t("chat_placeholder")}
              disabled={isTranscribing}
              className="flex-1 max-h-20 min-h-[40px] p-2 text-sm bg-[var(--background)] border border-[var(--border-color)] rounded-lg focus:outline-none focus:border-[var(--accent)] resize-none disabled:opacity-50"
              rows={1}
            />

            <button 
              onClick={sendMessage}
              disabled={!inputText.trim() || isLoading || isTranscribing}
              className="p-2 bg-[var(--accent)] text-[#121513] rounded-full disabled:opacity-50 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
