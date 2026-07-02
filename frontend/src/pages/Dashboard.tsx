import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SummaryCard from '../components/SummaryCard';
import { api } from '../api/client';
import type { AnalysisResult, SampleTender, HealthResult } from '../types';
import { FileSearch, ShieldAlert, FileText, CheckSquare, Zap } from 'lucide-react';
import { getStoredAnalysisResult } from '../utils/storage';

export default function Dashboard() {
  const navigate = useNavigate();
  const [health, setHealth] = useState<HealthResult | null>(null);
  const [samples, setSamples] = useState<SampleTender[]>([]);
  const [lastResult, setLastResult] = useState<AnalysisResult | null>(null);

  useEffect(() => {
    api.health().then(setHealth).catch(() => {});
    api.listSampleTenders().then(setSamples).catch(() => {});
    setLastResult(getStoredAnalysisResult());
  }, []);

  const highRiskCount = lastResult?.risks.filter((risk) => risk.severity === 'high').length ?? '-';
  const draftCount = lastResult ? lastResult.solution.sections.length : '-';
  const passRate = lastResult?.compliance.pass_rate || '-';

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-900">BidPilot 工作台</h2>
        <p className="text-sm text-gray-500 mt-1">政企软件信息化投标智能Agent系统</p>
      </div>

      {/* 指标卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <SummaryCard title="示例项目" value={samples.length} subtitle="可一键分析" color="blue" icon={<FileSearch size={18} />} />
        <SummaryCard title="高风险项" value={highRiskCount} subtitle={lastResult ? "最近分析" : "分析后展示"} color="red" icon={<ShieldAlert size={18} />} />
        <SummaryCard title="标书初稿" value={draftCount} subtitle={lastResult ? "章节数" : "分析后生成"} color="green" icon={<FileText size={18} />} />
        <SummaryCard title="合规通过率" value={passRate} subtitle={lastResult ? "最近分析" : "分析后展示"} color="amber" icon={<CheckSquare size={18} />} />
      </div>

      {/* 量化价值 */}
      <div className="glass-card rounded-xl border border-slate-200/55 p-6 mb-6 shadow-sm">
        <h3 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
          <Zap size={16} className="text-amber-500 fill-amber-500/30" /> 量化价值（基于模拟案例估算）
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-slate-600">
          <div className="flex items-start gap-2">
            <span className="text-emerald-500 font-bold">↓</span>
            <div>初步读标：<span className="font-medium text-slate-800">2-4小时 → 10-20分钟</span></div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-500 font-bold">↓</span>
            <div>资格整理：<span className="font-medium text-slate-800">1小时 → 5分钟</span></div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-500 font-bold">↓</span>
            <div>评分分析：<span className="font-medium text-slate-800">1-2小时 → 10分钟</span></div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-500 font-bold">↓</span>
            <div>响应表初稿：<span className="font-medium text-slate-800">半天 → 10-15分钟</span></div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-500 font-bold">✓</span>
            <div>废标风险覆盖：<span className="font-medium text-slate-800">报价/资质/签章/保证金/★号参数</span></div>
          </div>
          <div className="flex items-start gap-2">
            <span className="text-emerald-500 font-bold">✓</span>
            <div>新人辅助：<span className="font-medium text-slate-800">降低对老员工经验依赖</span></div>
          </div>
        </div>
      </div>

      {/* 示例项目 */}
      <div className="glass-card rounded-xl border border-slate-200/55 p-6 mb-6 shadow-sm">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">示例招标项目</h3>
        <div className="space-y-3">
          {samples.map((s) => (
            <div key={s.id} className="flex items-center justify-between p-3.5 rounded-lg border border-slate-100 hover:bg-white/50 transition-colors">
              <div>
                <div className="text-sm font-semibold text-slate-800">{s.name}</div>
                <div className="text-xs text-slate-500 mt-1">
                  <span className="inline-block bg-slate-100 text-slate-600 px-2 py-0.5 rounded mr-2 font-medium">{s.industry}</span>
                  预算：<span className="font-semibold text-slate-700">{s.budget}</span> · {s.description}
                </div>
              </div>
              <button
                onClick={() => navigate('/analysis', { state: { tenderId: s.id } })}
                className="text-xs premium-gradient-primary text-white px-4 py-2 rounded-lg hover:shadow-md transition-all font-medium flex-shrink-0"
              >
                一键分析
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* 系统状态 */}
      <div className="text-xs text-gray-400">
        后端状态：{health?.status === 'ok' ? '✓ 正常' : '✗ 异常'} ·
        版本：{health?.version || '-'} ·
        模式：{health?.mock_mode ? 'Mock演示' : '真实模型'}
      </div>
    </div>
  );
}
