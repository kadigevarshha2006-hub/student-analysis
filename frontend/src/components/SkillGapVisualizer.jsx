import React from 'react';
import './DashboardComponents.css';

const SkillGapVisualizer = ({ result }) => {
  return (
    <div className="skill-gap-visualizer glass-card">
      <h3>Skill Gap Analysis</h3>
      
      <div className="skill-section">
        <h4 className="acquired-skills-title">Acquired Skills</h4>
        <div className="chips-container">
          {result.currentSkills.map(skill => (
            <span key={skill} className="skill-chip current">{skill}</span>
          ))}
        </div>
      </div>

      <div className="divider"></div>

      <div className="skill-section">
        <h4 className="missing-skills-title">Missing Skills to Acquire</h4>
        <p className="hint">These are required for your target role</p>
        <div className="chips-container">
          {result.missingSkills.map(skill => (
            <span key={skill} className="skill-chip missing">{skill}</span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SkillGapVisualizer;
