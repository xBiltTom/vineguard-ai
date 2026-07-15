import ThemeToggle from "@/components/ThemeToggle";
import { ScanLine, UploadCloud } from "lucide-react";

export default function Home() {
  return (
    <main className="max-w-5xl mx-auto px-6 py-12">
      {/* Header */}
      <header className="flex justify-between items-center mb-12 border-b border-[var(--border-color)] pb-6">
        <div>
          <div className="flex items-center gap-3">
            <ScanLine className="text-[var(--accent)] w-8 h-8" />
            <h1 className="text-2xl font-bold tracking-tight">VINEGUARD AI</h1>
          </div>
          <p className="text-sm opacity-60 mt-1 uppercase tracking-widest font-mono">
            Precision Foliar Diagnostics v2.0
          </p>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-xs font-mono border border-[var(--border-color)] px-3 py-1.5 rounded bg-[var(--card-bg)] hover:border-[var(--accent)] transition-colors">
            ES / EN
          </button>
          <ThemeToggle />
        </div>
      </header>

      {/* Main Content Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Upload / Scanner Area */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-8 shadow-sm flex flex-col items-center justify-center min-h-[400px] relative overflow-hidden group cursor-pointer hover:border-[var(--accent)] transition-colors">
            
            {/* Ambient Background Glow on hover */}
            <div className="absolute inset-0 bg-gradient-to-b from-transparent to-[var(--accent)] opacity-0 group-hover:opacity-5 transition-opacity duration-500" />
            
            <div className="flex flex-col items-center text-center z-10">
              <UploadCloud className="w-12 h-12 mb-4 opacity-50 group-hover:text-[var(--accent)] group-hover:opacity-100 transition-all duration-300" />
              <h3 className="text-xl font-medium mb-2">Drop leaf sample here</h3>
              <p className="text-sm opacity-60 max-w-sm mb-6">
                Upload a high-resolution image of a grapevine leaf. The AI will scan for Esca, Black Rot, or Leaf Blight.
              </p>
              
              <button className="bg-[var(--foreground)] text-[var(--background)] px-6 py-2.5 rounded font-medium text-sm hover:bg-[var(--accent)] hover:text-[#121513] transition-colors flex items-center gap-2">
                <ScanLine className="w-4 h-4" />
                Initialize Scan
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: AI Metrics / Terminal area */}
        <div className="flex flex-col gap-6">
          <div className="bg-[var(--card-bg)] border border-[var(--border-color)] rounded-xl p-6 shadow-sm h-full flex flex-col">
            <h3 className="text-sm uppercase tracking-widest font-mono opacity-50 mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[var(--accent)] animate-pulse"></span>
              System Status
            </h3>
            
            <div className="flex-1 flex flex-col justify-center items-center text-center border border-dashed border-[var(--border-color)] rounded-lg p-6">
              <p className="font-mono text-xs opacity-40">Awaiting visual input...</p>
            </div>
            
            <div className="mt-6 pt-6 border-t border-[var(--border-color)]">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs opacity-60">Engine</span>
                <span className="text-xs font-mono">MobileNetV2 (Custom)</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs opacity-60">Accuracy</span>
                <span className="text-xs font-mono text-[var(--accent)]">98.4% MCC</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs opacity-60">Latency</span>
                <span className="text-xs font-mono">~45ms</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
