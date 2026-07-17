import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SummaryCard from '../components/SummaryCard';
import { api } from '../api/client';
import type { AnalysisResult, SampleTender, HealthResult } from '../types';
import { ArrowRight, CheckCircle2, FileSearch, ShieldAlert, FileText, CheckSquare, Sparkles, Zap } from 'lucide-react';
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
    <div className="max-w-7xl mx-auto">
      <section className="relative overflow-hidden rounded-3xl bg-slate-950 px-6 py-7 sm:px-8 sm:py-9 mb-6 shadow-xl shadow-slate-900/10">
        <div className="absolute inset-y-0 right-0 w-2/3 bg-[radial-gradient(circle_at_70%_35%,rgba(59,130,246,0.46),transparent_44%)]" />
        <div className="relative max-w-2xl">
          <div className="inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1.5 text-xs font-semibold text-blue-100 ring-1 ring-white/10">
            <Sparkles size={14} className="text-blue-300" /> 政企投标智能工作台
          </div>
          <h2 className="mt-4 text-2xl sm:text-3xl font-bold tracking-tight text-white">把读标、校验与成稿，收敛到一次清晰的决策流程。</h2>
          <p className="mt-3 text-sm leading-6 text-slate-300">从一份招标文件开始，快速识别高风险条款、评分重点与待准备材料。</p>
          <button onClick={() => navigate('/analysis')} className="focus-ring mt-6 inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-slate-900 shadow-lg shadow-black/10 hover:bg-blue-50 transition-colors">
            开始新的投标分析 <ArrowRight size={16} />
          </button>
        </div>
      </section>

      <div className="flex items-end justify-between gap-4 mb-4">
        <div>
          <p className="page-eyebrow">工作概览</p>
          <h3 className="mt-1 text-xl font-bold text-slate-900">当前投标准备进度</h3>
        </div>
        <div className={`hidden sm:flex items-center gap-2 text-xs font-medium ${health?.status === 'ok' ? 'text-emerald-700' : 'text-slate-400'}`}>
          <span className={`h-2 w-2 rounded-full ${health?.status === 'ok' ? 'bg-emerald-500' : 'bg-slate-300'}`} />
          {health?.status === 'ok' ? `分析服务在线 · ${health.version}` : '正在连接分析服务'}
        </div>
      </div>

      {/* 指标卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <SummaryCard title="示例项目" value={samples.length} subtitle="可一键分析" color="blue" icon={<FileSearch size={18} />} />
        <SummaryCard title="高风险项" value={highRiskCount} subtitle={lastResult ? "最近分析" : "分析后展示"} color="red" icon={<ShieldAlert size={18} />} />
        <SummaryCard title="标书初稿" value={draftCount} subtitle={lastResult ? "章节数" : "分析后生成"} color="green" icon={<FileText size={18} />} />
        <SummaryCard title="合规通过率" value={passRate} subtitle={lastResult ? "最近分析" : "分析后展示"} color="amber" icon={<CheckSquare size={18} />} />
      </div>

      {/* 量化价值 */}
      <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6 mb-6">
        <div className="flex items-center gap-3 mb-5">
          <div className="h-9 w-9 rounded-xl bg-amber-50 text-amber-600 grid place-items-center"><Zap size={17} /></div>
          <div><p className="text-sm font-bold text-slate-800">量化价值</p><p className="text-xs text-slate-500 mt-0.5">基于模拟案例估算</p></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-x-6 gap-y-4 text-sm text-slate-600">
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
      <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6 mb-6">
        <div className="flex items-center justify-between gap-4 mb-4">
          <div><p className="page-eyebrow">快速开始</p><h3 className="mt-1 text-base font-bold text-slate-800">示例招标项目</h3></div>
          <span className="hidden sm:inline-flex items-center gap-1.5 text-xs text-slate-500"><CheckCircle2 size={14} className="text-emerald-500" /> 选择后可直接分析</span>
        </div>
        <div className="space-y-3">
          {samples.map((s) => (
            <div key={s.id} className="group flex items-center justify-between gap-4 p-4 rounded-xl border border-slate-100 bg-white/45 hover:border-primary-200 hover:bg-white transition-all">
              <div className="min-w-0">
                <div className="text-sm font-semibold text-slate-800">{s.name}</div>
                <div className="text-xs text-slate-500 mt-2 leading-5">
                  <span className="inline-block bg-primary-50 text-primary-700 px-2 py-0.5 rounded-md mr-2 font-semibold">{s.industry}</span>
                  预算：<span className="font-semibold text-slate-700">{s.budget}</span><span className="hidden md:inline"> · {s.description}</span>
                </div>
              </div>
              <button
                onClick={() => navigate('/analysis', { state: { tenderId: s.id } })}
                className="focus-ring inline-flex items-center gap-1.5 text-xs premium-gradient-primary text-white px-3.5 py-2 rounded-lg hover:shadow-md transition-all font-semibold flex-shrink-0"
              >
                分析 <ArrowRight size={13} className="group-hover:translate-x-0.5 transition-transform" />
              </button>
            </div>
          ))}
          {!samples.length && <div className="rounded-xl border border-dashed border-slate-200 py-8 text-center text-sm text-slate-500">正在加载可分析的示例项目…</div>}
        </div>
      </div>

      {/* 系统状态 */}
      <div className="text-xs text-slate-400 px-1">
        服务状态：{health?.status === 'ok' ? '正常' : '连接中'} · 版本：{health?.version || '-'} · 模式：{health?.mock_mode ? '演示分析' : '真实模型'}
      </div>
    </div>
  );
}
