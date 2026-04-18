import { useState, useRef, useEffect } from 'react';
import './Dashboard.css';
import SkillGapVisualizer from './SkillGapVisualizer';
import RoadmapRecommendations from './RoadmapRecommendations';

const Dashboard = () => {
  const [githubUrl, setGithubUrl] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fastMode, setFastMode] = useState(false);

  const fileInputRef = useRef(null);

  const [progressBoost, setProgressBoost] = useState(0);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const sharedData = params.get('share');
    if (sharedData) {
      try {
        const decoded = JSON.parse(decodeURIComponent(escape(atob(sharedData))));
        setAnalysisResult(decoded);
      } catch (e) {
        console.error("Failed to load shared roadmap", e);
        alert("Invalid or corrupted share link.");
      }
    }
  }, []);

  const handleShare = () => {
    try {
      const jsonStr = JSON.stringify(analysisResult);
      const base64Str = btoa(unescape(encodeURIComponent(jsonStr)));
      const shareUrl = `${window.location.origin}${window.location.pathname}?share=${base64Str}`;
      navigator.clipboard.writeText(shareUrl);
      alert('Share link copied to clipboard!');
    } catch (e) {
      console.error(e);
      alert('Failed to generate share link. Data might be too large.');
    }
  };

  const handleAnalyze = async (completedItems = []) => {
    if ((!githubUrl && !selectedFile) || !targetRole) return;
    setAnalyzing(true);
    setProgressBoost(0);

    try {
      const formData = new FormData();
      formData.append('targetRole', targetRole);
      formData.append('githubUrl', githubUrl);
      formData.append('completedItems', JSON.stringify(completedItems));
      formData.append('fastMode', fastMode);
      if (selectedFile) {
        formData.append('file', selectedFile);
      }

      const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        let errorMsg = 'Analysis failed check backend logs';
        try {
          const errorData = await response.json();
          errorMsg = errorData.detail || errorMsg;
        } catch (e) {
          // ignore parsing error
        }
        throw new Error(errorMsg);
      }

      const data = await response.json();
      if (data.error) {
        alert("Invalid Input: " + data.error);
        return;
      }
      setAnalysisResult(data);
    } catch (error) {
      console.error(error);
      alert(`Error: ${error.message}\n\n(If it fails intermittently, you might be hitting Gemini API limits or a timeout)`);
    } finally {
      setAnalyzing(false);
    }
  };

  const currentMatchPercentage = analysisResult ? Math.min(100, analysisResult.matchPercentage + progressBoost) : 0;

  return (
    <div className="dashboard-container animate-fade-in">
      {!analysisResult ? (
        <div className="upload-section glass-card">
          <h2 className="text-gradient">Analyze Your Skill Gap</h2>
          <p>Link your GitHub or upload your Resume to compare your current profile against live job market demands.</p>
          
          <div className="input-group">
            <div className="github-bar-container" style={{ display: 'flex', alignItems: 'center', backgroundColor: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.1)', paddingRight: '10px' }}>
              <input 
                type="text" 
                className="input-field" 
                placeholder="https://github.com/username or Paste Resume Text"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                style={{ border: 'none', backgroundColor: 'transparent', flexGrow: 1, marginBottom: 0, boxShadow: 'none' }}
              />
              <button 
                type="button" 
                className="attach-btn" 
                onClick={() => fileInputRef.current?.click()}
                title="Attach PDF or Document"
                style={{ background: 'none', border: 'none', color: '#8b5cf6', cursor: 'pointer', fontSize: '1.2rem', padding: '5px' }}
              >
                📎
              </button>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={(e) => setSelectedFile(e.target.files[0])} 
                style={{ display: 'none' }}
                accept=".pdf,.docx,.txt"
              />
            </div>
            {selectedFile && <div style={{ fontSize: '0.8rem', color: '#a78bfa', marginTop: '5px', textAlign: 'left', paddingLeft: '5px' }}>Attached: {selectedFile.name}</div>}
            <input 
              type="text" 
              className="input-field" 
              placeholder="Your Target Role (e.g. Data Scientist, Backend Engineer)"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              style={{ marginTop: '15px' }}
            />
            
            <label style={{ display: 'flex', alignItems: 'center', marginTop: '15px', color: '#a78bfa', fontSize: '0.9rem', cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={fastMode} 
                onChange={(e) => setFastMode(e.target.checked)} 
                style={{ marginRight: '8px', cursor: 'pointer' }}
              />
              Fast Mode (Quick & Concise Descriptions)
            </label>
          </div>
          
          <button 
            className="btn-primary analyze-btn" 
            onClick={() => handleAnalyze()}
            disabled={analyzing || (!githubUrl && !selectedFile) || !targetRole}
          >
            {analyzing ? 'Analyzing Profile with AI...' : 'Generate Roadmap'}
          </button>
        </div>
      ) : (
        <div className="results-section">
          <div className="overview-header glass-card">
            <h2>Target Role: <span className="text-gradient">{analysisResult.role}</span></h2>
            <div className="match-score">
              <span className="score-label">Market Readiness</span>
              <div className="progress-bar-container">
                <div 
                  className="progress-bar-fill" 
                  style={{ width: `${currentMatchPercentage}%` }}
                ></div>
              </div>
              <span className="score-value">{currentMatchPercentage}%</span>
            </div>
          </div>
          
          <div className="analysis-grid">
            <SkillGapVisualizer result={analysisResult} />
            <RoadmapRecommendations 
              result={analysisResult} 
              onProgressUpdate={(completed, total) => {
                 // Each completed item gives a max of remaining percentage to 100
                const remaining = 100 - analysisResult.matchPercentage;
                const boost = Math.round((completed / total) * remaining);
                setProgressBoost(boost);
              }}
              onDynamicUpdate={(completedItems) => handleAnalyze(completedItems)}
            />
          </div>
          
          <div className="actions" style={{ display: 'flex', gap: '15px', justifyContent: 'center' }}>
            <button className="btn-outline" onClick={() => {
              setAnalysisResult(null);
              window.history.pushState({}, '', window.location.pathname);
            }}>Analyze New Profile</button>
            <button className="btn-primary" onClick={handleShare}>🔗 Share Roadmap</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
