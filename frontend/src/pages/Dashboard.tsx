import { useEffect } from 'react'
import { useAgentStore, useTaskStore } from '@/store'
import { formatDistanceToNow } from 'date-fns'

export default function Dashboard() {
  const { agents, fetchAgents } = useAgentStore()
  const { tasks, fetchTasks } = useTaskStore()
  
  useEffect(() => {
    fetchAgents()
    fetchTasks()
  }, [])
  
  const activeTasks = tasks.filter(t => t.status === 'running')
  
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">控制台</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="text-gray-400 text-sm mb-2">Agent 总数</div>
          <div className="text-3xl font-bold text-blue-400">{agents.length}</div>
        </div>
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="text-gray-400 text-sm mb-2">活跃任务</div>
          <div className="text-3xl font-bold text-green-400">{activeTasks.length}</div>
        </div>
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <div className="text-gray-400 text-sm mb-2">系统状态</div>
          <div className="text-3xl font-bold text-emerald-400">正常</div>
        </div>
      </div>
      
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="px-6 py-4 border-b border-gray-700">
          <h3 className="text-lg font-semibold">最近任务</h3>
        </div>
        <div className="divide-y divide-gray-700">
          {tasks.length === 0 ? (
            <div className="p-6 text-gray-500 text-center">暂无任务</div>
          ) : (
            tasks.slice(0, 10).map(task => (
              <div key={task.id} className="px-6 py-4 flex items-center justify-between">
                <div>
                  <div className="font-medium">任务 {task.id.slice(0, 8)}...</div>
                  <div className="text-sm text-gray-400">Agent: {task.agent_id.slice(0, 8)}...</div>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`px-2 py-1 rounded text-xs ${
                    task.status === 'completed' ? 'bg-green-900 text-green-300' :
                    task.status === 'running' ? 'bg-blue-900 text-blue-300' : 'bg-gray-700'
                  }`}>{task.status}</span>
                  <span className="text-sm text-gray-500">
                    {formatDistanceToNow(new Date(task.started_at), { addSuffix: true })}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
