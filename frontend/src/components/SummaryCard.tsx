import React from 'react';

interface SummaryCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  color?: string;
  icon?: React.ReactNode;
}

export default function SummaryCard({ title, value, subtitle, color = 'blue', icon }: SummaryCardProps) {
  const colorMap: Record<string, { text: string, border: string, gradient: string }> = {
    blue: { text: 'text-blue-600', border: 'border-blue-200/40', gradient: 'premium-gradient-primary' },
    green: { text: 'text-emerald-600', border: 'border-emerald-200/40', gradient: 'premium-gradient-emerald' },
    red: { text: 'text-rose-600', border: 'border-rose-200/40', gradient: 'premium-gradient-rose' },
    amber: { text: 'text-amber-600', border: 'border-amber-200/40', gradient: 'premium-gradient-amber' },
    purple: { text: 'text-purple-600', border: 'border-purple-200/40', gradient: 'premium-gradient-purple' },
  };

  const style = colorMap[color] || colorMap.blue;

  return (
    <div className={`glass-card rounded-xl border p-5 ${style.border} hover:shadow-lg transition-all duration-300 transform hover:-translate-y-0.5`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">{title}</span>
        <div className={`p-2 rounded-lg text-white ${style.gradient} shadow-md`}>
          {icon}
        </div>
      </div>
      <div className={`text-3xl font-extrabold mt-2 ${style.text}`}>{value}</div>
      {subtitle && <div className="text-xs text-slate-500 mt-1.5 font-medium">{subtitle}</div>}
    </div>
  );
}
