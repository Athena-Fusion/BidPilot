import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { api } from '../api/client';
import type { SampleTender, AnalysisResult } from '../types';
import AgentFlow from '../components/AgentFlow';
import RiskTable from '../components/RiskTable';
import ScoreTable from '../components/ScoreTable';
import FileUploader from '../components/FileUploader';
import { ArrowRight, CheckCircle2, Play, Loader2, AlertCircle } from 'lucide-react';
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
    <div className="max-w-7xl mx-auto">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          <p className="page-eyebrow">第一步 · 输入文件</p>
          <h2 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">招标分析</h2>
          <p className="mt-2 text-sm text-slate-500">选择示例项目，或上传真实招标文件，系统将生成完整的投标准备底稿。</p>
        </div>
        {selectedId && <div className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700"><CheckCircle2 size={14} /> 已选择分析对象</div>}
      </div>

      {/* 选择与操作 */}
      <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6 mb-5">
        <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_minmax(280px,0.72fr)] gap-7 lg:gap-10">
          <div>
            <div className="flex items-center gap-2 mb-4"><span className="h-7 w-7 rounded-lg bg-primary-50 text-primary-700 grid place-items-center text-xs font-bold">1</span><h3 className="text-sm font-bold text-slate-800">从示例项目开始</h3></div>
          <div className="flex-1">
            <label className="text-xs font-semibold text-slate-600 mb-2 block">选择招标文件</label>
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="focus-ring w-full border border-slate-200 bg-white rounded-xl px-3.5 py-3 text-sm text-slate-700 shadow-sm"
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
            className="focus-ring mt-3 w-full sm:w-auto inline-flex justify-center items-center gap-2 premium-gradient-primary text-white px-5 py-3 rounded-xl text-sm font-bold hover:shadow-lg hover:shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {loading ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
            {loading ? '分析中...' : '开始分析'} {!loading && <ArrowRight size={15} />}
          </button>
          <p className="mt-3 text-xs text-slate-400">适合快速体验完整分析流程</p>
          </div>
          <div className="lg:border-l lg:border-slate-100 lg:pl-8">
            <div className="flex items-center gap-2 mb-4"><span className="h-7 w-7 rounded-lg bg-violet-50 text-violet-700 grid place-items-center text-xs font-bold">2</span><h3 className="text-sm font-bold text-slate-800">上传真实文件</h3></div>
            <FileUploader onFileSelect={handleFileUpload} onValidationError={setError} />
          </div>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 text-red-700 text-sm mb-5 bg-red-50 border border-red-100 p-3.5 rounded-xl">
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
          <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6">
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
          <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6">
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
          <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">
              评分规则（技术{result.scoring.technical_score}分 + 商务{result.scoring.business_score}分 + 价格{result.scoring.price_score}分）
            </h3>
            <ScoreTable items={result.scoring.items} highValueItems={result.scoring.high_value_items} />
          </div>

          {/* 风险概览 */}
          <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">风险概览（{result.risks.length}项）</h3>
            <RiskTable risks={result.risks} />
          </div>
        </div>
      )}
    </div>
  );
}
