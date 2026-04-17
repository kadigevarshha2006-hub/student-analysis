import React, { useState } from 'react';
import './DashboardComponents.css';

const RoadmapRecommendations = ({ result, onProgressUpdate, onDynamicUpdate }) => {
  const [completedItems, setCompletedItems] = useState(new Set());
  const [deepDives, setDeepDives] = useState({});
  const [loadingDives, setLoadingDives] = useState({});

  const toggleComplete = (title) => {
    const newDocs = new Set(completedItems);
    if (newDocs.has(title)) {
      newDocs.delete(title);
    } else {
      newDocs.add(title);
    }
    setCompletedItems(newDocs);
    
    // Quick math to update progress score visually
    const totalItems = (result.roadmap?.length || 0) + (result.projects?.length || 0);
    if (totalItems > 0 && onProgressUpdate) {
      onProgressUpdate(newDocs.size, totalItems);
    }
  };

  const fetchDeepDive = async (topic) => {
    if (deepDives[topic]) return; // already fetched
    
    setLoadingDives(prev => ({...prev, [topic]: true}));
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_URL}/api/deep-dive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic, targetRole: result.role })
      });
      const data = await response.json();
      setDeepDives(prev => ({...prev, [topic]: data}));
    } catch (err) {
      console.error(err);
      alert('Failed to fetch deep dive for ' + topic);
    } finally {
      setLoadingDives(prev => ({...prev, [topic]: false}));
    }
  };

  return (
    <div className="roadmap-container glass-card">
      <h3 className="text-gradient">Personalized Learning Roadmap</h3>
      <p>Based on your missing skills, here is your dynamic learning path and project suggestions.</p>
      
      <div className="timeline">
        {/* Render Roadmap Tasks */}
        {result.roadmap?.map((task, index) => (
          <div className="timeline-item" key={`task-${index}`}>
            <div className={`timeline-marker ${completedItems.has(task.title) ? 'final' : ''}`}></div>
            <div className="timeline-content">
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <input 
                  type="checkbox" 
                  checked={completedItems.has(task.title)}
                  onChange={() => toggleComplete(task.title)}
                  style={{ marginRight: '10px' }}
                />
                <h4 style={{ textDecoration: completedItems.has(task.title) ? 'line-through' : 'none' }}>
                  Day {task.day}: {task.title}
                </h4>
              </div>
              <p><strong>Explain:</strong> {task.description}</p>
              {task.resources && task.resources.length > 0 && (
                <ul>
                  {task.resources.map((res, i) => (
                    <li key={i}><a href={res} className="resource-link" target="_blank" rel="noreferrer">External Resource</a></li>
                  ))}
                </ul>
              )}
              
              <div style={{ marginTop: '10px' }}>
                <button 
                  className="btn-outline" 
                  style={{ fontSize: '0.8rem', padding: '5px 10px' }}
                  onClick={() => fetchDeepDive(task.title)}
                  disabled={loadingDives[task.title]}
                >
                  {loadingDives[task.title] ? 'Fetching Deep Dive...' : 'Get Dive Deep Info 🔍'}
                </button>
              </div>

              {deepDives[task.title] && (
                <div className="deep-dive-panel" style={{ marginTop: '15px', padding: '15px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                  <h5 style={{ color: '#a855f7', marginBottom: '8px' }}>📚 Curated Courses/Tutorials</h5>
                  <ul style={{ fontSize: '0.85rem', marginBottom: '10px' }}>
                    {deepDives[task.title].courses?.map((c, i) => (
                      <li key={i}><strong>{c.name}</strong> ({c.duration}) - <a href={c.link} target="_blank" rel="noreferrer" style={{color: '#60a5fa'}}>Search/Link</a></li>
                    ))}
                  </ul>
                  
                  <h5 style={{ color: '#4ade80', marginBottom: '8px' }}>📖 Official Documentation</h5>
                  <ul style={{ fontSize: '0.85rem', marginBottom: '10px' }}>
                    {deepDives[task.title].documentations?.map((d, i) => (
                      <li key={i}>{d.name} - <a href={d.link} target="_blank" rel="noreferrer" style={{color: '#60a5fa'}}>Link</a></li>
                    ))}
                  </ul>
                  
                  <h5 style={{ color: '#f472b6', marginBottom: '8px' }}>💻 Actionable Mini-Projects</h5>
                  <ul style={{ fontSize: '0.85rem' }}>
                    {deepDives[task.title].mini_projects?.map((mp, i) => (
                      <li key={i}>{mp}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Render AI Project Suggestions */}
        {result.projects?.map((project, index) => (
          <div className="timeline-item" key={`proj-${index}`}>
            <div className={`timeline-marker ${completedItems.has(project.title) ? 'final' : ''}`}></div>
            <div className="timeline-content" style={{ borderLeft: '3px solid #6366f1' }}>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                 <input 
                  type="checkbox" 
                  checked={completedItems.has(project.title)}
                  onChange={() => toggleComplete(project.title)}
                  style={{ marginRight: '10px' }}
                />
                <h4 style={{ textDecoration: completedItems.has(project.title) ? 'line-through' : 'none' }}>
                  Project: {project.title} <span style={{ fontSize: '0.8rem', color: '#ffb86c' }}>({project.difficulty})</span>
                </h4>
              </div>
              <p className="project-description">
                <strong>Why this project?</strong> {project.description}
              </p>
              <div className="project-steps">
                <span><strong>Skills Honed:</strong> {project.skills_utilized?.join(', ')}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {completedItems.size > 0 && (
        <div style={{ marginTop: '30px', textAlign: 'center' }}>
          <p style={{ marginBottom: '15px', fontSize: '0.9rem', color: '#94a3b8' }}>
            Checked off {completedItems.size} item(s)? Regenerate your roadmap to skip acquired skills!
          </p>
          <button 
            className="btn-primary" 
            style={{ width: '100%' }}
            onClick={() => onDynamicUpdate(Array.from(completedItems))}
          >
            Update Dynamic Recommendations 🔄
          </button>
        </div>
      )}
    </div>
  );
};

export default RoadmapRecommendations;
