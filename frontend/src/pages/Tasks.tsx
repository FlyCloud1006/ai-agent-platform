import { useEffect } from 'react'
import { useTaskStore } from '@/store'
import { formatDistanceToNow } from 'date-fns'

export default function Tasks() {
  const { tasks, fetchTasks } = useTaskStore()
  
  useEffect(() => {
    fetchTasks()
    const interval = setInterval(fetchTasks, 5000)
    return () => clearInterval(interval)
  }, [])
  
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">任务管理</h2>
        <button onClick={fetchTasks} className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg">刷新</button>
      </div>
      
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700 text-left text-gray-400 text-sm">
                <th className="px-6 py-3">任务ID</th>
                <th className="px-6 py-3">状态</th>
                <th className="px-6 py-3">开始时间</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {tasks.length === 0 ? (
                <tr><td colSpan={3} className="px-6 py-8 text-center text-gray-500">暂无任务</td></tr>
              ) : (
                tasks.map(task => (
                  <tr key={task.id} className="hover:bg-gray-750">
                    <td className="px-6 py-4 font-mono text-sm">{task.id.slice(0, 16)}...</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs ${
                        task.status === 'completed' ? 'bg-green-900 text-green-300' :
                        task.status === 'running' ? 'bg-blue-900 text-blue-300' : 'bg-gray-700'
                      }`}>{task.status}</span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-400">
                      {formatDistanceToNow(new Date(task.started_at), { addSuffix: true })}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
