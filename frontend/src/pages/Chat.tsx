import { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { useChatStore, useAgentStore } from '@/store'
import ReactMarkdown from 'react-markdown'

export default function Chat() {
  const { agentId } = useParams<{ agentId?: string }>()
  const { agents, fetchAgents } = useAgentStore()
  const { messages, isLoading, sendMessage, clearMessages } = useChatStore()
  const [input, setInput] = useState('')
  const [selectedAgent, setSelectedAgent] = useState(agentId || '')
  const bottomRef = useRef<HTMLDivElement>(null)
  
  useEffect(() => { fetchAgents() }, [])
  useEffect(() => { if (agentId) setSelectedAgent(agentId) }, [agentId])
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])
  
  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !selectedAgent || isLoading) return
    const msg = input
    setInput('')
    await sendMessage(selectedAgent, msg)
  }
  
  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">AI 对话</h2>
        <button onClick={clearMessages} className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 rounded">清空对话</button>
      </div>
      
      <div className="mb-4">
        <select value={selectedAgent} onChange={e => setSelectedAgent(e.target.value)} className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg outline-none">
          <option value="">选择 Agent...</option>
          {agents.map(a => <option key={a.id} value={a.id}>{a.name} ({a.role})</option>)}
        </select>
      </div>
      
      <div className="flex-1 bg-gray-800 rounded-lg border border-gray-700 overflow-auto p-4 space-y-4">
        {messages.length === 0 && <div className="h-full flex items-center justify-center text-gray-500">选择 Agent 后开始对话</div>}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] rounded-lg px-4 py-3 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-700'}`}>
              <div className="prose prose-invert prose-sm max-w-none"><ReactMarkdown>{msg.content}</ReactMarkdown></div>
              <div className="text-xs opacity-60 mt-1">{new Date(msg.timestamp).toLocaleTimeString()}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 rounded-lg px-4 py-3">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:'0ms'}} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:'150ms'}} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay:'300ms'}} />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      
      <form onSubmit={handleSend} className="mt-4 flex gap-3">
        <input type="text" value={input} onChange={e => setInput(e.target.value)} disabled={!selectedAgent || isLoading} placeholder={selectedAgent ? '输入消息...' : '请先选择 Agent'} className="flex-1 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg outline-none disabled:opacity-50" />
        <button type="submit" disabled={!selectedAgent || !input.trim() || isLoading} className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg">发送</button>
      </form>
    </div>
  )
}
