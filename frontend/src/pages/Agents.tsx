import { useEffect, useState } from 'react'
import { useAgentStore } from '@/store'
import toast from 'react-hot-toast'

export default function Agents() {
  const { agents, fetchAgents, createAgent, deleteAgent } = useAgentStore()
  const [showModal, setShowModal] = useState(false)
  const [form, setForm] = useState({ name: '', role: '', description: '', instructions: '' })
  
  useEffect(() => { fetchAgents() }, [])
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await createAgent(form)
      toast.success('Agent 创建成功')
      setShowModal(false)
      setForm({ name: '', role: '', description: '', instructions: '' })
    } catch { toast.error('创建失败') }
  }
  
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Agent 管理</h2>
        <button onClick={() => setShowModal(true)} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors">+ 创建 Agent</button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map(agent => (
          <div key={agent.id} className="bg-gray-800 rounded-lg border border-gray-700 p-4">
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="font-semibold text-lg">{agent.name}</h3>
                <span className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">{agent.role}</span>
              </div>
              <button onClick={() => deleteAgent(agent.id)} className="text-red-400 hover:text-red-300 text-sm">删除</button>
            </div>
            <p className="text-gray-400 text-sm mb-3 line-clamp-2">{agent.description || '暂无描述'}</p>
            <div className="flex items-center justify-between text-sm">
              <span className={`px-2 py-1 rounded ${agent.status === 'idle' ? 'bg-green-900 text-green-300' : 'bg-blue-900 text-blue-300'}`}>{agent.status}</span>
              <span className="text-gray-500">{new Date(agent.created_at).toLocaleDateString()}</span>
            </div>
          </div>
        ))}
      </div>
      
      {agents.length === 0 && <div className="text-center py-12 text-gray-500">暂无 Agent，点击上方按钮创建一个</div>}
      
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md border border-gray-700">
            <h3 className="text-xl font-bold mb-4">创建 Agent</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              {[['name','名称'],['role','角色'],['description','描述'],['instructions','指令(必填)']].map(([k,label]) => (
                <div key={k}>
                  <label className="block text-sm text-gray-400 mb-1">{label}</label>
                  {k === 'instructions' ? (
                    <textarea value={form.instructions} onChange={e => setForm({...form, instructions: e.target.value})} rows={3} className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 outline-none" required />
                  ) : (
                    <input type="text" value={form[k as keyof typeof form]} onChange={e => setForm({...form, [k]: e.target.value})} className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 outline-none" required={k === 'name' || k === 'role'} />
                  )}
                </div>
              ))}
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="flex-1 px-4 py-2 bg-gray-700 rounded">取消</button>
                <button type="submit" className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded">创建</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
