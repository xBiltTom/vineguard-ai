"use client";

import { useState, useRef } from "react";
import { ScanLine, UploadCloud, AlertTriangle, CheckCircle, Bug } from "lucide-react";

export default function ScannerDashboard() {
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
        setError("Please upload a valid image file.");
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
      setError("Please drop a valid image file.");
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
      // Forzamos un mínimo de 1.5 segundos para apreciar la animación láser
      const minDelay = new Promise(resolve => setTimeout(resolve, 1500));
      
      const apiCall = fetch("http://localhost:8000/api/predict", {
        method: "POST",
        body: formData,
      });

      // Ejecutamos ambas promesas a la vez
      const [res] = await Promise.all([apiCall, minDelay]);

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Error del servidor API. ¿Está prendido FastAPI?");
      }

      const data = await res.json();
      setScanResult(data);
      
    } catch (err: unknown) {
      if (err instanceof Error) {
        // Si dice "Failed to fetch", es que el servidor está apagado
        if (err.message.includes("Failed to fetch")) {
          setError("Error: No se pudo conectar a FastAPI (Puerto 8000).");
        } else {
          setError(err.message);
        }
      } else {
        setError("Ocurrió un error inesperado");
      }
    } finally {
      setIsScanning(false);
    }
  };

  // Determinar icono y color según el resultado
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
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Left Column: Upload / Scanner Area */}
      <div className="lg:col-span-2 flex flex-col gap-6">
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
          
          {/* Ambient Glow */}
          {!imagePreview && (
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[var(--accent)] opacity-0 group-hover:opacity-5 transition-opacity duration-500" />
          )}

          {imagePreview ? (
            <div className="relative w-full h-full flex items-center justify-center">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={imagePreview} alt="Leaf preview" className="max-h-[350px] object-contain rounded-lg z-10" />
              
              {isScanning && (
                <>
                  <div className="absolute inset-0 bg-black/40 z-20 rounded-lg"></div>
                  {/* Láser de la firma visual */}
                  <div className="scanner-laser"></div>
                  {/* Cuadrícula técnica sobre la foto */}
                  <div className="absolute inset-0 z-20 opacity-30" style={{
                    backgroundImage: "linear-gradient(var(--accent) 1px, transparent 1px), linear-gradient(90deg, var(--accent) 1px, transparent 1px)",
                    backgroundSize: "20px 20px"
                  }}></div>
                </>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center text-center z-10">
              <UploadCloud className="w-12 h-12 mb-4 opacity-50 group-hover:text-[var(--accent)] group-hover:opacity-100 transition-all duration-300" />
              <h3 className="text-xl font-medium mb-2">Drop leaf sample here</h3>
              <p className="text-sm opacity-60 max-w-sm mb-6">
                Upload a high-resolution image of a grapevine leaf. The AI will scan for Esca, Black Rot, or Leaf Blight.
              </p>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div className="flex justify-end items-center gap-4">
          {error && <span className="text-red-500 text-sm font-medium">{error}</span>}
          <button 
            disabled={!imageFile || isScanning}
            onClick={(e) => { e.stopPropagation(); startScan(); }}
            className="bg-[var(--foreground)] text-[var(--background)] px-8 py-3 rounded font-medium text-sm hover:bg-[var(--accent)] hover:text-[#121513] transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ScanLine className={`w-4 h-4 ${isScanning ? 'animate-spin' : ''}`} />
            {isScanning ? 'ANALYZING TISSUE...' : 'INITIALIZE SCAN'}
          </button>
        </div>
      </div>

      {/* Right Column: AI Metrics / Terminal area */}
      <div className="flex flex-col gap-6">
        <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-6 shadow-sm h-full flex flex-col">
          <h3 className="text-sm uppercase tracking-widest font-mono opacity-50 mb-6 flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isScanning ? 'bg-yellow-500 animate-pulse' : (scanResult ? 'bg-[var(--accent)]' : 'bg-gray-500')}`}></span>
            System Status
          </h3>
          
          <div className="flex-1 flex flex-col justify-center items-center text-center border border-dashed border-[var(--border-color)] rounded-lg p-6 bg-[var(--background)]/50">
            {!scanResult && !isScanning && (
              <p className="font-mono text-xs opacity-40">Awaiting visual input...</p>
            )}
            
            {isScanning && (
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-2 border-t-[var(--accent)] border-r-transparent border-b-transparent border-l-transparent rounded-full animate-spin"></div>
                <p className="font-mono text-xs text-[var(--accent)] animate-pulse">Computing tensor...</p>
              </div>
            )}
            
            {scanResult && ui && (
              <div className="flex flex-col items-center gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                {ui.icon}
                <div>
                  <h2 className={`text-2xl font-bold ${ui.color}`}>{scanResult.predicted_class}</h2>
                  <p className="text-sm opacity-60 font-mono mt-1">Diagnosis Complete</p>
                </div>
              </div>
            )}
          </div>
          
          <div className="mt-6 pt-6 border-t border-[var(--border-color)]">
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs opacity-60">Engine</span>
              <span className="text-xs font-mono">VineGuard CNN v2</span>
            </div>
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs opacity-60">Confidence</span>
              <span className={`text-xs font-mono ${scanResult ? 'text-[var(--accent)]' : ''}`}>
                {scanResult ? `${(scanResult.confidence * 100).toFixed(2)}%` : '--'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-xs opacity-60">Latency</span>
              <span className="text-xs font-mono">
                {scanResult ? `${scanResult.inference_time_ms}ms` : '--'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
