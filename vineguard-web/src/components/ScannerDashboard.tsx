"use client";

import { useState, useRef } from "react";
import { ScanLine, UploadCloud, AlertTriangle, CheckCircle, Bug } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";
import { useScan } from "@/contexts/ScanContext";

export default function ScannerDashboard() {
  const { t, language } = useLanguage();
  const { setLastScan } = useScan();
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [scanResult, setScanResult] = useState<any>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        setError(language === "es" ? "Sube un archivo de imagen válido." : "Please upload a valid image file.");
        return;
      }
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
      setScanResult(null);
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith("image/")) {
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
      setScanResult(null);
      setError(null);
    } else {
      setError(language === "es" ? "Por favor suelta un archivo de imagen válido." : "Please drop a valid image file.");
    }
  };

  const startScan = async () => {
    if (!imageFile) return;
    
    setIsScanning(true);
    setError(null);
    setScanResult(null);
    
    const formData = new FormData();
    formData.append("image", imageFile);

    try {
      const minDelay = new Promise(resolve => setTimeout(resolve, 1500));
      
      const apiCall = fetch("http://localhost:8000/api/predict", {
        method: "POST",
        body: formData,
      });

      const [res] = await Promise.all([apiCall, minDelay]);

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || (language === "es" ? "Error del servidor API." : "API Server Error."));
      }

      const data = await res.json();
      setScanResult(data);
      setLastScan(data); // <-- Publica el resultado al contexto global
      
    } catch (err: unknown) {
      if (err instanceof Error) {
        if (err.message.includes("Failed to fetch")) {
          setError(t("error_api_conn"));
        } else {
          setError(err.message);
        }
      } else {
        setError("Ocurrió un error inesperado / Unexpected error");
      }
    } finally {
      setIsScanning(false);
    }
  };

  const getResultUI = () => {
    if (!scanResult) return null;
    
    if (scanResult.predicted_class === "Healthy") {
      return { icon: <CheckCircle className="w-12 h-12 text-[var(--accent)]" />, color: "text-[var(--accent)]" };
    }
    if (scanResult.predicted_class === "Esca") {
      return { icon: <AlertTriangle className="w-12 h-12 text-[var(--danger)]" />, color: "text-[var(--danger)]" };
    }
    return { icon: <Bug className="w-12 h-12 text-yellow-500" />, color: "text-yellow-500" };
  };

  const ui = getResultUI();

  return (
    <div className="flex flex-col gap-8">
      {/* SECCIÓN SUPERIOR: Input y Diagnóstico Principal */}
      <div className={`grid grid-cols-1 ${scanResult ? 'lg:grid-cols-2' : 'lg:grid-cols-3'} gap-8 transition-all duration-700 ease-in-out`}>
        
        {/* Zona Izquierda: Carga de Imagen */}
        <div className={`${scanResult ? 'lg:col-span-1' : 'lg:col-span-2'} flex flex-col gap-6 transition-all duration-700`}>
          <div 
            className={`bg-[var(--card-bg)] border ${error ? 'border-red-500' : 'border-[var(--border-color)]'} rounded-xl p-8 shadow-sm flex flex-col items-center justify-center min-h-[400px] relative overflow-hidden group cursor-pointer hover:border-[var(--accent)] transition-colors`}
            onClick={() => !isScanning && fileInputRef.current?.click()}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleImageUpload} 
              className="hidden" 
              accept="image/jpeg, image/png, image/jpg" 
            />
            
            {!imagePreview && (
              <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[var(--accent)] opacity-0 group-hover:opacity-5 transition-opacity duration-500" />
            )}

            {imagePreview ? (
              <div className="relative w-full h-full flex items-center justify-center">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={imagePreview} alt="Leaf preview" className="max-h-[350px] object-contain rounded-lg z-10 shadow-lg" />
                
                {isScanning && (
                  <>
                    <div className="absolute inset-0 bg-black/50 z-20 rounded-lg"></div>
                    <div className="scanner-laser"></div>
                    <div className="absolute inset-0 z-20 opacity-30" style={{
                      backgroundImage: "linear-gradient(var(--accent) 1px, transparent 1px), linear-gradient(90deg, var(--accent) 1px, transparent 1px)",
                      backgroundSize: "30px 30px"
                    }}></div>
                  </>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center text-center z-10">
                <UploadCloud className="w-16 h-16 mb-6 opacity-40 group-hover:text-[var(--accent)] group-hover:opacity-100 transition-all duration-300" />
                <h3 className="text-2xl font-medium mb-3 tracking-wide">{t("drop_title")}</h3>
                <p className="text-sm opacity-60 max-w-sm mb-6 leading-relaxed">
                  {t("drop_desc")}
                </p>
              </div>
            )}
          </div>

          <div className="flex justify-end items-center gap-4">
            {error && <span className="text-red-500 text-sm font-medium animate-pulse">{error}</span>}
            <button 
              disabled={!imageFile || isScanning}
              onClick={(e) => { e.stopPropagation(); startScan(); }}
              className="bg-[var(--foreground)] text-[var(--background)] px-10 py-4 rounded font-bold tracking-widest text-xs hover:bg-[var(--accent)] hover:text-[#121513] transition-all flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed uppercase shadow-[0_4px_14px_0_rgba(0,0,0,0.1)]"
            >
              <ScanLine className={`w-5 h-5 ${isScanning ? 'animate-spin' : ''}`} />
              {isScanning ? t("btn_scan_loading") : t("btn_scan_init")}
            </button>
          </div>
        </div>

        {/* Zona Derecha: Estado / Tarjeta Principal (Arriba) */}
        <div className={`flex flex-col gap-6 ${!scanResult && !isScanning ? 'lg:col-span-1' : 'lg:col-span-1'} transition-all duration-700`}>
          <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-8 shadow-sm flex flex-col h-full relative overflow-hidden">
            {/* Efecto de fondo */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-[var(--accent)] to-transparent opacity-5 rounded-full blur-3xl"></div>
            
            <h3 className="text-xs uppercase tracking-widest font-mono opacity-50 mb-8 flex items-center gap-3">
              <span className={`w-2.5 h-2.5 rounded-full ${isScanning ? 'bg-yellow-500 animate-pulse shadow-[0_0_8px_#EAB308]' : (scanResult ? 'bg-[var(--accent)] shadow-[0_0_8px_var(--accent)]' : 'bg-gray-500')}`}></span>
              {t("system_status")}
            </h3>
            
            <div className="flex-1 flex flex-col justify-center items-center text-center">
              {!scanResult && !isScanning && (
                <div className="opacity-30 flex flex-col items-center">
                  <div className="w-16 h-16 border border-dashed border-current rounded-full mb-4 flex items-center justify-center">?</div>
                  <p className="font-mono text-xs uppercase tracking-widest">{t("awaiting_input")}</p>
                </div>
              )}
              
              {isScanning && (
                <div className="flex flex-col items-center gap-6 animate-in fade-in zoom-in duration-500">
                  <div className="w-16 h-16 border-4 border-[var(--border-color)] border-t-[var(--accent)] rounded-full animate-spin"></div>
                  <p className="font-mono text-sm text-[var(--accent)] animate-pulse tracking-widest">{t("computing_tensor")}</p>
                </div>
              )}
              
              {scanResult && ui && (
                <div className="flex flex-col items-start text-left w-full animate-in slide-in-from-right-8 fade-in duration-700">
                  <div className="flex items-center gap-4 mb-6">
                    <div className={`p-4 rounded-2xl bg-[var(--background)]/80 border border-[var(--border-color)] shadow-inner`}>
                      {ui.icon}
                    </div>
                    <div>
                      <p className="text-xs font-mono opacity-50 tracking-widest uppercase mb-1">{t("diagnosis_complete")}</p>
                      <h3 className="text-4xl sm:text-5xl font-black mb-4 tracking-tight drop-shadow-md group-hover:text-[var(--accent)] transition-colors">
                        {t("class_" + scanResult.predicted_class)}
                      </h3>
                    </div>
                  </div>
                  <div className="bg-[var(--background)]/40 p-5 rounded-xl border border-[var(--border-color)] w-full">
                    <p className="text-sm opacity-80 leading-relaxed font-medium">
                      {t(`disease_desc_${scanResult.predicted_class}` as any)}
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* SECCIÓN INFERIOR: Panel de Detalles de Inferencia (Solo visible al terminar) */}
      {scanResult && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-12 duration-1000 ease-out pb-10">
          
          {/* Panel 1: Tensor Math (Probabilidades) */}
          <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-6 shadow-sm">
            <h4 className="text-xs uppercase tracking-widest font-bold opacity-50 mb-6 flex items-center gap-2">
              <span className="text-[var(--accent)]">/</span> {t("probability_dist")}
            </h4>
            <div className="flex flex-col gap-5">
              {Object.entries(scanResult.probabilities)
                .sort(([, a], [, b]) => (b as number) - (a as number))
                .map(([className, prob]) => {
                  const percentage = ((prob as number) * 100).toFixed(1);
                  const isWinner = className === scanResult.predicted_class;
                  
                  let barColor = "bg-[var(--accent)]";
                  if (className === "Esca") barColor = "bg-amber-500";
                  if (className === "Black_rot") barColor = "bg-red-500";
                  if (className === "Healthy") barColor = "bg-emerald-500";
                  if (className === "Leaf_blight") barColor = "bg-blue-500";

                  return (
                    <div key={className} className="flex flex-col gap-2">
                      <div className="flex justify-between text-xs font-mono">
                        <span className={isWinner ? "font-bold text-[var(--foreground)] tracking-wide" : "opacity-60"}>{t("class_" + className)}</span>
                        <span className={isWinner ? "font-bold text-[var(--foreground)]" : "opacity-60"}>{percentage}%</span>
                      </div>
                      <div className="h-2 w-full bg-[#090C10] rounded-full overflow-hidden border border-white/5">
                        <div 
                          className={`h-full ${barColor} transition-all duration-1000 ease-out`} 
                          style={{ 
                            width: `${percentage}%`,
                            boxShadow: isWinner ? `0 0 15px ${barColor.replace('bg-', '')}` : 'none'
                          }}
                        />
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>

          {/* Panel 2: Plan de Acción */}
          <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-6 shadow-sm">
            <h4 className="text-xs uppercase tracking-widest font-bold opacity-50 mb-6 flex items-center gap-2">
              <span className="text-[var(--accent)]">/</span> {t("action_plan")}
            </h4>
            <ul className="flex flex-col gap-4">
              {[1, 2, 3].map((num) => (
                <li key={num} className="flex gap-4 items-start bg-[var(--background)]/30 p-4 rounded-lg border border-transparent hover:border-[var(--accent)]/30 transition-all duration-300 group">
                  <span className="flex-shrink-0 w-6 h-6 rounded bg-[var(--border-color)] text-[10px] font-mono flex items-center justify-center opacity-70 group-hover:bg-[var(--accent)] group-hover:text-black group-hover:font-bold transition-colors">
                    0{num}
                  </span>
                  <span className="text-sm opacity-90 leading-snug font-medium pt-0.5">
                    {t(`disease_rec${num}_${scanResult.predicted_class}` as any)}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Panel 3: Análisis Avanzado y Reporte */}
          <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-6 shadow-sm flex flex-col justify-between">
            <div>
              <h4 className="text-xs uppercase tracking-widest font-bold opacity-50 mb-6 flex items-center gap-2">
                <span className="text-[var(--accent)]">/</span> MÉTRICAS DE PRECISIÓN
              </h4>
              
              <div className="flex flex-col gap-6">
                {/* Donut Chart SVG */}
                <div className="flex items-center justify-between bg-[var(--background)]/30 p-4 rounded-lg border border-[var(--border-color)]/50">
                  <div className="flex flex-col">
                    <span className="text-xs opacity-60 tracking-wider mb-1">ÍNDICE DE CONFIANZA</span>
                    <span className="text-2xl font-bold text-[var(--foreground)]">{(scanResult.confidence * 100).toFixed(1)}<span className="text-sm opacity-50">%</span></span>
                    <span className="text-[10px] font-mono text-[var(--accent)] mt-1">LATENCIA: {scanResult.inference_time_ms}ms</span>
                  </div>
                  
                  <div className="relative w-20 h-20">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      {/* Círculo de fondo */}
                      <circle cx="50" cy="50" r="40" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-gray-200 dark:text-gray-800" />
                      {/* Círculo de progreso */}
                      <circle 
                        cx="50" 
                        cy="50" 
                        r="40" 
                        stroke="currentColor" 
                        strokeWidth="8" 
                        fill="transparent" 
                        strokeDasharray="251.2" 
                        strokeDashoffset={251.2 - (scanResult.confidence * 251.2)} 
                        strokeLinecap="round"
                        className={`${
                          scanResult.confidence > 0.85 ? 'text-emerald-500' : 
                          scanResult.confidence > 0.60 ? 'text-yellow-500' : 'text-red-500'
                        } transition-all duration-1500 ease-out`} 
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-[10px] font-bold">IA</span>
                    </div>
                  </div>
                </div>

                {/* Risk Level Indicator */}
                <div className="flex flex-col gap-2">
                  <span className="text-xs opacity-60 tracking-wider">NIVEL DE RIESGO BIOLÓGICO</span>
                  <div className="flex gap-1 h-3 w-full">
                    <div className={`h-full flex-1 rounded-l-full ${['Black_rot', 'Esca', 'Leaf_blight'].includes(scanResult.predicted_class) ? 'bg-yellow-500' : 'bg-emerald-500 shadow-[0_0_8px_#10B981]'}`}></div>
                    <div className={`h-full flex-1 ${['Black_rot', 'Esca'].includes(scanResult.predicted_class) ? 'bg-orange-500' : 'bg-[var(--border-color)] opacity-30'}`}></div>
                    <div className={`h-full flex-1 rounded-r-full ${['Black_rot', 'Esca'].includes(scanResult.predicted_class) ? 'bg-red-500 shadow-[0_0_8px_#EF4444] animate-pulse' : 'bg-[var(--border-color)] opacity-30'}`}></div>
                  </div>
                  <div className="flex justify-between text-[9px] font-mono opacity-50 uppercase px-1 mt-1">
                    <span>Bajo</span>
                    <span>Medio</span>
                    <span>Crítico</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6">
              <button 
                onClick={() => window.print()}
                className="w-full border border-[var(--border-color)] hover:border-[var(--accent)] hover:bg-[var(--accent)] hover:text-black text-[var(--foreground)] p-4 rounded-lg text-xs font-bold tracking-widest uppercase transition-all flex justify-center items-center gap-2 group"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="group-hover:animate-bounce"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
                Exportar Reporte
              </button>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
