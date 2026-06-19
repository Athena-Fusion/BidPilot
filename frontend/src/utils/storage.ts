import type { AnalysisResult } from '../types';

const STORAGE_KEY = 'bidpilot_result';

export function getStoredAnalysisResult(): AnalysisResult | null {
  try {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    return stored ? (JSON.parse(stored) as AnalysisResult) : null;
  } catch {
    sessionStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export function setStoredAnalysisResult(result: AnalysisResult) {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(result));
}
