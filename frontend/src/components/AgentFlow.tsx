import React from 'react';
import type { AgentTrace } from '../types';
import { ArrowRight, CheckCircle2, Clock3, Loader2 } from 'lucide-react';

interface AgentFlowProps {
  traces: AgentTrace[];
  running?: boolean;
}

const AGENT_LABELS: Record<string, string> = {
  TenderParserAgent: '招标解析',
  RequirementAgent: '资格提取',
  ScoringAgent: '评分分析',
  RiskAgent: '风险识别',
  StrategyAgent: '策略生成',
  SolutionAgent: '方案生成',
  BusinessAgent: '商务响应',
  ResponseTableAgent: '响应表生成',
  ComplianceAgent: '合规审查',
  ReportAgent: '报告生成',
};

export default function AgentFlow({ traces, running = false }: AgentFlowProps) {
  const allAgents = Object.keys(AGENT_LABELS);

  return (
    <div className="glass-card rounded-2xl border border-slate-200/80 p-5 sm:p-6">
      <div className="flex items-center justify-between gap-4 mb-5">
        <div>
          <p className="page-eyebrow">分析管线</p>
          <h3 className="mt-1 text-base font-bold text-slate-800">Agent 执行流程</h3>
        </div>
        <div className={`rounded-full px-3 py-1.5 text-xs font-semibold ${running ? 'bg-primary-50 text-primary-700' : traces.length ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'}`}>
          {running ? '正在分析' : traces.length ? `已完成 ${traces.length}/${allAgents.length}` : `等待开始 · ${allAgents.length} 步`}
        </div>
      </div>
      <div className="flex flex-wrap gap-y-3">
        {allAgents.map((agent, i) => {
          const trace = traces.find((t) => t.agent === agent);
          const done = !!trace;
          const active = running && !done && (i === traces.length);
          const label = AGENT_LABELS[agent] || agent;

          return (
            <React.Fragment key={agent}>
            <div
              className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                done
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-100'
                  : active
                  ? 'bg-primary-50 text-primary-700 border border-primary-200 shadow-sm animate-pulse'
                  : 'bg-slate-50 text-slate-400 border border-slate-200'
              }`}
            >
              {done ? (
                <CheckCircle2 size={14} />
              ) : active ? (
                <Loader2 size={14} className="animate-spin" />
              ) : (
                <Clock3 size={14} />
              )}
              {label}
              {done && trace && (
                <span className="text-[10px] opacity-60">{trace.duration_ms}ms</span>
              )}
            </div>
            {i < allAgents.length - 1 && <ArrowRight size={14} className="hidden xl:block mx-1 self-center text-slate-300" />}
            </React.Fragment>
          );
        })}
      </div>
      {traces.length > 0 && (
        <div className="mt-5 pt-4 border-t border-slate-100 grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
          {traces.map((t) => (
            <div key={t.agent} className="text-xs text-slate-500">
              <span className="font-semibold text-slate-700">{AGENT_LABELS[t.agent] || t.agent}</span> · {t.summary}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
