import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileSearch, ShieldAlert, Target, FileText, CheckSquare, Sparkles } from 'lucide-react';

const navItems = [
  { path: '/', label: '工作台', icon: LayoutDashboard },
  { path: '/analysis', label: '招标分析', icon: FileSearch },
  { path: '/risk', label: '风险审查', icon: ShieldAlert },
  { path: '/strategy', label: '投标策略', icon: Target },
  { path: '/document', label: '标书生成', icon: FileText },
  { path: '/compliance', label: '合规审查', icon: CheckSquare },
];

interface LayoutProps {
  children: React.ReactNode;
  mockMode?: boolean;
}

export default function Layout({ children, mockMode = true }: LayoutProps) {
  return (
    <div className="min-h-screen flex">
      {/* 侧边栏 */}
      <aside className="hidden lg:flex w-64 glass-sidebar text-white flex-col flex-shrink-0 sticky top-0 h-screen">
        <div className="px-5 pt-6 pb-5 border-b border-slate-700/70">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-400 to-primary-700 shadow-lg shadow-blue-950/30 grid place-items-center">
              <Sparkles size={19} strokeWidth={2.5} />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">BidPilot</h1>
              <p className="text-[11px] text-slate-400 mt-0.5">智能投标工作台</p>
            </div>
          </div>
        </div>
        <nav className="flex-1 px-3 py-5 space-y-1">
          <p className="px-3 mb-3 text-[10px] font-bold tracking-[0.18em] text-slate-500">工作流</p>
          {navItems.map(({ path, label, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive ? 'bg-primary-600 text-white shadow-lg shadow-blue-950/20' : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-slate-700/70">
          <div className={`flex items-center gap-2 text-xs px-3 py-2 rounded-lg ${mockMode ? 'bg-amber-400/10 text-amber-200' : 'bg-emerald-400/10 text-emerald-200'}`}>
            <span className={`h-1.5 w-1.5 rounded-full ${mockMode ? 'bg-amber-300' : 'bg-emerald-300'}`} />
            {mockMode ? '演示分析模式' : '真实模型模式'}
          </div>
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 min-w-0 overflow-auto">
        <div className="lg:hidden sticky top-0 z-10 bg-slate-950/95 backdrop-blur border-b border-slate-800 px-4 py-3">
          <div className="flex items-center gap-2 text-white mb-3"><Sparkles size={16} className="text-blue-300" /><span className="font-semibold">BidPilot</span></div>
          <nav className="flex gap-2 overflow-x-auto pb-0.5">
            {navItems.map(({ path, label }) => (
              <NavLink key={path} to={path} className={({ isActive }) => `whitespace-nowrap rounded-full px-3 py-1.5 text-xs font-medium ${isActive ? 'bg-primary-600 text-white' : 'bg-slate-800 text-slate-300'}`}>
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="p-4 sm:p-6 lg:p-8">{children}</div>
      </main>
    </div>
  );
}
