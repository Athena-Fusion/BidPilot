import React from 'react';

interface SummaryCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  color?: string;
  icon?: React.ReactNode;
}

export default function SummaryCard({ title, value, subtitle, color = 'blue', icon }: SummaryCardProps) {
  const colorMap: Record<string, { text: string, border: string, gradient: string, surface: string }> = {
    blue: { text: 'text-blue-700', border: 'border-blue-100', gradient: 'premium-gradient-primary', surface: 'bg-blue-50/70' },
    green: { text: 'text-emerald-700', border: 'border-emerald-100', gradient: 'premium-gradient-emerald', surface: 'bg-emerald-50/70' },
    red: { text: 'text-rose-700', border: 'border-rose-100', gradient: 'premium-gradient-rose', surface: 'bg-rose-50/70' },
    amber: { text: 'text-amber-700', border: 'border-amber-100', gradient: 'premium-gradient-amber', surface: 'bg-amber-50/70' },
    purple: { text: 'text-purple-700', border: 'border-purple-100', gradient: 'premium-gradient-purple', surface: 'bg-purple-50/70' },
  };

  const style = colorMap[color] || colorMap.blue;

  return (
    <div className={`glass-card rounded-2xl border p-5 ${style.border} hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5`}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-600">{title}</span>
        <div className={`p-2.5 rounded-xl text-white ${style.gradient} shadow-md`}>
          {icon}
        </div>
      </div>
      <div className={`text-3xl font-extrabold tracking-tight mt-5 ${style.text}`}>{value}</div>
      {subtitle && <div className={`mt-3 inline-flex rounded-md px-2 py-1 text-xs font-medium text-slate-500 ${style.surface}`}>{subtitle}</div>}
    </div>
  );
}
