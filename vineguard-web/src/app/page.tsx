"use client";

import ThemeToggle from "@/components/ThemeToggle";
import ScannerDashboard from "@/components/ScannerDashboard";
import ChatbotWidget from "@/components/ChatbotWidget";
import { ScanLine } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

export default function Home() {
  const { t, language, toggleLanguage } = useLanguage();

  return (
    <main className="max-w-5xl mx-auto px-6 py-12 relative">
      {/* Header */}
      <header className="flex justify-between items-center mb-12 border-b border-[var(--border-color)] pb-6">
        <div>
          <div className="flex items-center gap-3">
            <ScanLine className="text-[var(--accent)] w-8 h-8" />
            <h1 className="text-2xl font-bold tracking-tight">VINEGUARD AI</h1>
          </div>
          <p className="text-sm opacity-60 mt-1 uppercase tracking-widest font-mono">
            {t("header_subtitle")}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={toggleLanguage}
            className="text-xs font-mono border border-[var(--border-color)] px-3 py-1.5 rounded bg-[var(--card-bg)] hover:border-[var(--accent)] transition-colors"
          >
            {language === "es" ? "EN" : "ES"}
          </button>
          <ThemeToggle />
        </div>
      </header>

      {/* Main Content Dashboard */}
      <ScannerDashboard />

      {/* Chatbot Voice & Text Assistant */}
      <ChatbotWidget />
    </main>
  );
}
