import React from 'react';
import type { AgentTrace } from '../types';
import { CheckCircle, Clock, Loader2 } from 'lucide-react';

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
    <div className="bg-white rounded-lg border p-4">
      <h3 className="text-sm font-medium text-gray-700 mb-3">Agent 执行流程</h3>
      <div className="flex flex-wrap gap-2">
        {allAgents.map((agent, i) => {
          const trace = traces.find((t) => t.agent === agent);
          const done = !!trace;
          const active = running && !done && (i === traces.length);
          const label = AGENT_LABELS[agent] || agent;

          return (
            <div
              key={agent}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                done
                  ? 'bg-green-50 text-green-700 border border-green-200'
                  : active
                  ? 'bg-blue-50 text-blue-700 border border-blue-200 animate-pulse'
                  : 'bg-gray-50 text-gray-400 border border-gray-200'
              }`}
            >
              {done ? (
                <CheckCircle size={14} />
              ) : active ? (
                <Loader2 size={14} className="animate-spin" />
              ) : (
                <Clock size={14} />
              )}
              {label}
              {done && trace && (
                <span className="text-[10px] opacity-60">{trace.duration_ms}ms</span>
              )}
            </div>
          );
        })}
      </div>
      {traces.length > 0 && (
        <div className="mt-3 space-y-1">
          {traces.map((t) => (
            <div key={t.agent} className="text-xs text-gray-500">
              <span className="font-medium">{AGENT_LABELS[t.agent] || t.agent}</span>：{t.summary}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
