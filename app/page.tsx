export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 to-black p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">Peach Agents</h1>
        <p className="text-xl text-gray-400 mb-8">Trading Platform with AI-Powered Market Intelligence</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-white mb-2">📊 Dashboard</h2>
            <p className="text-gray-400">Real-time trading metrics and performance tracking</p>
          </div>
          
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-white mb-2">🚀 Deployment</h2>
            <p className="text-gray-400">Automated batch deployments with intelligent scaling</p>
          </div>
          
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-white mb-2">🧠 Learning</h2>
            <p className="text-gray-400">YouTube + RSS sentiment analysis for market insights</p>
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">System Status</h3>
          <p className="text-gray-400">✅ Deployment active</p>
          <p className="text-gray-400">✅ Database connected</p>
          <p className="text-gray-400">✅ Market monitoring live</p>
        </div>
      </div>
    </main>
  )
}
