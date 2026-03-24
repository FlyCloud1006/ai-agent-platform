import { Outlet, NavLink } from 'react-router-dom'
import clsx from 'clsx'

const navItems = [
  { path: '/dashboard', label: '控制台', icon: '📊' },
  { path: '/agents', label: 'Agent管理', icon: '🤖' },
  { path: '/chat', label: 'AI对话', icon: '💬' },
  { path: '/tasks', label: '任务管理', icon: '📋' },
  { path: '/settings', label: '设置', icon: '⚙️' },
]

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex">
      <aside className="w-64 bg-gray-800 border-r border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-700">
          <h1 className="text-xl font-bold text-blue-400">🤖 AI Agent 平台</h1>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(item => (
            <NavLink key={item.path} to={item.path} className={({isActive}) => clsx('flex items-center gap-3 px-4 py-3 rounded-lg transition-colors', isActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700')}>
              <span>{item.icon}</span><span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-700 text-sm text-gray-500">v1.0.0</div>
      </aside>
      <main className="flex-1 overflow-auto"><div className="p-6"><Outlet /></div></main>
    </div>
  )
}
