export default function Settings() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">设置</h2>
      <div className="max-w-2xl space-y-6">
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <h3 className="text-lg font-semibold mb-4">LLM 配置</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Provider</label>
              <select className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 outline-none">
                <option value="openai">OpenAI</option>
                <option value="minimax">MiniMax</option>
                <option value="deepseek">DeepSeek</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">API Key</label>
              <input type="password" placeholder="sk-..." className="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 outline-none" />
            </div>
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition-colors">保存配置</button>
          </div>
        </div>
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
          <h3 className="text-lg font-semibold mb-4">关于</h3>
          <div className="text-gray-400 text-sm space-y-2">
            <p>AI Agent 协作平台 v1.0.0</p>
            <p>基于 React + TypeScript + FastAPI 构建</p>
          </div>
        </div>
      </div>
    </div>
  )
}
