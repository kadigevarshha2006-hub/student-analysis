
import './index.css'
import Dashboard from './components/Dashboard'

function App() {
  return (
    <div className="app-container">
      <header className="glass-panel main-header">
        <div className="header-content">
          <h1 className="text-gradient logo">SkillBridge AI</h1>
          <nav>
            <button className="btn-outline">Dashboard</button>
          </nav>
        </div>
      </header>
      
      <main className="main-content">
        <Dashboard />
      </main>

      <footer className="main-footer">
        <p>Empowering students to bridge the gap to industry standards.</p>
      </footer>
    </div>
  )
}

export default App
