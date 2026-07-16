"use client";

import { createContext, useContext, useState, ReactNode } from "react";

// Estructura del resultado del último escaneo
export interface ScanResult {
  predicted_class: string;
  confidence: number;
  inference_time_ms: number;
  probabilities: Record<string, number>;
}

interface ScanContextType {
  lastScan: ScanResult | null;
  setLastScan: (result: ScanResult | null) => void;
}

const ScanContext = createContext<ScanContextType>({
  lastScan: null,
  setLastScan: () => {},
});

export function ScanProvider({ children }: { children: ReactNode }) {
  const [lastScan, setLastScan] = useState<ScanResult | null>(null);
  return (
    <ScanContext.Provider value={{ lastScan, setLastScan }}>
      {children}
    </ScanContext.Provider>
  );
}

export function useScan() {
  return useContext(ScanContext);
}
