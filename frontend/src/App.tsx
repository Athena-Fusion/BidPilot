import React, { useState, useEffect } from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import TenderAnalysis from './pages/TenderAnalysis';
import RiskReview from './pages/RiskReview';
import BidStrategy from './pages/BidStrategy';
import DocumentWriter from './pages/DocumentWriter';
import ComplianceReview from './pages/ComplianceReview';
import { api } from './api/client';
import type { AnalysisResult, HealthResult } from './types';
import { getStoredAnalysisResult } from './utils/storage';

function AppContent() {
  const [mockMode, setMockMode] = useState(true);

  useEffect(() => {
    api.health().then((h: HealthResult) => setMockMode(h.mock_mode)).catch(() => {});
  }, []);

  return (
    <Layout mockMode={mockMode}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analysis" element={<TenderAnalysisWrapper />} />
        <Route path="/risk" element={<RiskReview />} />
        <Route path="/strategy" element={<BidStrategy />} />
        <Route path="/document" element={<DocumentWriter />} />
        <Route path="/compliance" element={<ComplianceReview />} />
      </Routes>
    </Layout>
  );
}

// 包装器：分析后自动存储结果到 sessionStorage
function TenderAnalysisWrapper() {
  return <TenderAnalysisWithStorage />;
}

function TenderAnalysisWithStorage() {
  const [, setResult] = useState<AnalysisResult | null>(null);

  // 监听分析结果变化并存储
  useEffect(() => {
    const handler = () => {
      const stored = getStoredAnalysisResult();
      if (stored) setResult(stored);
    };
    window.addEventListener('storage', handler);
    return () => window.removeEventListener('storage', handler);
  }, []);

  return <TenderAnalysis />;
}

export default function App() {
  return (
    <HashRouter>
      <AppContent />
    </HashRouter>
  );
}
