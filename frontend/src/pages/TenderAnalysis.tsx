import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { api } from '../api/client';
import type { SampleTender, AnalysisResult } from '../types';
import AgentFlow from '../components/AgentFlow';
import RiskTable from '../components/RiskTable';
import ScoreTable from '../components/ScoreTable';
import FileUploader from '../components/FileUploader';
import { Play, Loader2, AlertCircle } from 'lucide-react';
import { setStoredAnalysisResult } from '../utils/storage';

export default function TenderAnalysis() {
  const location = useLocation();
  const [samples, setSamples] = useState<SampleTender[]>([]);
  const [selectedId, setSelectedId] = useState('');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api.listSampleTenders().then(setSamples).catch(() => {});
    const state = location.state as { tenderId?: string } | null;
    if (state?.tenderId) setSelectedId(state.tenderId);
  }, [location]);

  const handleAnalyze = async () => {
    if (!selectedId) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const r = await api.analyzeTender(selectedId);
      setResult(r);
      setStoredAnalysisResult(r);
    } catch (e: any) {
      setError(e.message || '分析失败');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    try {
      const r = await api.uploadTender(file);
      setSelectedId(r.tender_id);
    } catch (e: any) {
      setError(e.message || '上传失败');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-xl font-bold text-gray-900 mb-4">招标分析</h2>

      {/* 选择与操作 */}
      <div className="bg-white rounded-lg border p-4 mb-4">
        <div className="flex items-end gap-4 mb-4">
          <div className="flex-1">
            <label className="text-xs font-medium text-gray-600 mb-1 block">选择示例招标文件</label>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="w-full border rounded px-3 py-2 text-sm"
            >
              <option value="">-- 请选择 --</option>
              {samples.map((s) => (
                <option key={s.id} value={s.id}>{s.name}（{s.budget}）</option>
              ))}
            </select>
          </div>
          <button
            onClick={handleAnalyze}
            disabled={!selectedId || loading}
            className="flex items-center gap-2 bg-primary-600 text-white px-5 py-2 rounded text-sm hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
            {loading ? '分析中...' : '一键分析'}
          </button>
        </div>
        <FileUploader onFileSelect={handleFileUpload} onValidationError={setError} />
      </div>

      {error && (
        <div className="flex items-center gap-2 text-red-600 text-sm mb-4 bg-red-50 p-3 rounded">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      {/* Agent流程 */}
      <div className="mb-4">
        <AgentFlow traces={result?.agent_trace || []} running={loading} />
      </div>

      {result && (
        <div className="space-y-4">
          {/* 基本信息 */}
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">招标摘要</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
              <div><span className="text-gray-500">项目名称：</span>{result.basic_info.project_name}</div>
              <div><span className="text-gray-500">采购人：</span>{result.basic_info.buyer}</div>
              <div><span className="text-gray-500">预算：</span>{result.basic_info.budget}</div>
              <div><span className="text-gray-500">截止时间：</span>{result.basic_info.deadline}</div>
              <div><span className="text-gray-500">服务周期：</span>{result.basic_info.service_period}</div>
              <div><span className="text-gray-500">保证金：</span>{result.basic_info.bid_bond}</div>
            </div>
          </div>

          {/* 资格要求 */}
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">资格要求（{result.requirements.length}项）</h3>
            <div className="space-y-2">
              {result.requirements.map((r, i) => (
                <div key={i} className="flex items-start gap-2 text-sm">
                  <span className={`px-1.5 py-0.5 rounded text-xs font-medium flex-shrink-0 ${
                    r.risk_level === 'high' ? 'bg-red-100 text-red-700' : r.risk_level === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'
                  }`}>{r.risk_level === 'high' ? '高' : r.risk_level === 'medium' ? '中' : '低'}</span>
                  <span className="text-gray-500 flex-shrink-0">[{r.type}]</span>
                  <span>{r.requirement}</span>
                </div>
              ))}
            </div>
          </div>

          {/* 评分规则 */}
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              评分规则（技术{result.scoring.technical_score}分 + 商务{result.scoring.business_score}分 + 价格{result.scoring.price_score}分）
            </h3>
            <ScoreTable items={result.scoring.items} highValueItems={result.scoring.high_value_items} />
          </div>

          {/* 风险概览 */}
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">风险概览（{result.risks.length}项）</h3>
            <RiskTable risks={result.risks} />
          </div>
        </div>
      )}
    </div>
  );
}
