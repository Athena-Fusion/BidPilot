import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileSearch, ShieldAlert, Target, FileText, CheckSquare } from 'lucide-react';

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
    <div className="min-h-screen bg-gray-50 flex">
      {/* 侧边栏 */}
      <aside className="w-56 glass-sidebar text-white flex flex-col flex-shrink-0">
        <div className="p-4 border-b border-slate-700">
          <h1 className="text-lg font-bold tracking-wide">BidPilot</h1>
          <p className="text-xs text-slate-400 mt-1">政企投标智能Agent</p>
        </div>
        <nav className="flex-1 py-2">
          {navItems.map(({ path, label, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) =>
                `flex items-center gap-2 px-4 py-2.5 text-sm transition-colors ${
                  isActive ? 'bg-primary-600 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-slate-700">
          <div className={`text-xs px-2 py-1 rounded ${mockMode ? 'bg-amber-500/20 text-amber-300' : 'bg-green-500/20 text-green-300'}`}>
            {mockMode ? '⚡ Mock 演示模式' : '✓ 真实模型模式'}
          </div>
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="flex-1 overflow-auto">
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
