import { create } from 'zustand'
import axios from 'axios'

const API = '/api/v1'
const api = axios.create({ baseURL: API })

export interface Agent {
  id: string; name: string; role: string; description: string; instructions: string;
  status: string; config: Record<string,any>; created_at: string; updated_at: string;
}

export interface Message { role: 'user'|'assistant'; content: string; timestamp: string; }

interface AgentStore { agents: Agent[]; loading: boolean; fetchAgents: () => Promise<void>; createAgent: (d: Partial<Agent>) => Promise<Agent>; deleteAgent: (id: string) => Promise<void>; }
interface ChatStore { messages: Message[]; isLoading: boolean; sendMessage: (aid: string, msg: string) => Promise<void>; clearMessages: () => void; }
interface TaskStore { tasks: any[]; fetchTasks: () => Promise<void>; }

export const useAgentStore = create<AgentStore>((set, get) => ({
  agents: [], loading: false,
  fetchAgents: async () => { set({loading:true}); try { const r = await api.get('/agents'); set({agents:r.data,loading:false}); } catch { set({loading:false}); } },
  createAgent: async (d) => { const r = await api.post('/agents', d); set({agents:[...get().agents, r.data]}); return r.data; },
  deleteAgent: async (id) => { await api.delete(`/agents/${id}`); set({agents: get().agents.filter(a => a.id !== id)}); },
}))

export const useChatStore = create<ChatStore>((set, get) => ({
  messages: [], isLoading: false,
  sendMessage: async (agentId, message) => {
    set({isLoading: true});
    set({messages: [...get().messages, {role:'user', content:message, timestamp:new Date().toISOString()}]});
    try {
      const r = await api.post('/chat', {agent_id: agentId, message});
      set({messages: [...get().messages, {role:'assistant', content:r.data.response, timestamp:new Date().toISOString()}]});
    } catch(e: any) {
      set({messages: [...get().messages, {role:'assistant', content:`错误: ${e.message}`, timestamp:new Date().toISOString()}]});
    } finally { set({isLoading: false}); }
  },
  clearMessages: () => set({messages: []}),
}))

export const useTaskStore = create<TaskStore>((set) => ({
  tasks: [],
  fetchTasks: async () => { try { const r = await api.get('/tasks'); set({tasks: r.data}); } catch {} },
}))
