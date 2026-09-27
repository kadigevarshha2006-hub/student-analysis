-- ====================================================================
-- AI-Powered Resume Analyzer & Job Matching System (ResumeAI)
-- Database: MySQL 8.0+
-- ====================================================================

CREATE DATABASE IF NOT EXISTS resume_ai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE resume_ai_db;

-- --------------------------------------------------------------------
-- Table: users
-- Stores registered users and authentication credentials
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(191) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_email (email)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: skills_master
-- Canonical taxonomy of technical and soft skills across categories
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS skills_master (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category ENUM(
        'Programming',
        'Web Development',
        'Data & Databases',
        'AI & Machine Learning',
        'Cloud & DevOps',
        'Mobile Development',
        'Testing & QA',
        'Tools & Platforms',
        'Soft Skills'
    ) NOT NULL,
    aliases JSON NULL COMMENT 'JSON array of aliases/synonyms, e.g. ["JS", "ECMAScript"]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_skill_name (name),
    INDEX idx_skill_category (category)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: resumes
-- Uploaded resume documents and parsed raw / structured content
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(20) NOT NULL COMMENT 'pdf or docx',
    file_size_bytes INT NOT NULL,
    raw_text LONGTEXT NOT NULL,
    parsed_json JSON NULL COMMENT 'Structured extracted JSON (contact, education, exp, etc.)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_resumes_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_resumes_user (user_id),
    INDEX idx_resumes_created (created_at)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: resume_skills
-- Skills extracted from specific resumes with confidence and category
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS resume_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    source ENUM('explicit', 'inferred', 'project', 'experience') DEFAULT 'explicit',
    confidence_score DECIMAL(4, 2) DEFAULT 1.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_resume_skills_resume FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    INDEX idx_resume_skills_resume (resume_id),
    INDEX idx_resume_skills_name (skill_name)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: resume_analysis
-- ATS, quality, and generative AI feedback records for resumes
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS resume_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    overall_score DECIMAL(5, 2) NOT NULL,
    ats_score DECIMAL(5, 2) NOT NULL,
    quality_score DECIMAL(5, 2) NOT NULL,
    skills_score DECIMAL(5, 2) NOT NULL,
    readability_score DECIMAL(5, 2) NOT NULL,
    formatting_score DECIMAL(5, 2) NOT NULL,
    section_breakdown JSON NULL COMMENT 'JSON scores per section',
    ats_checks_json JSON NULL COMMENT 'List of pass/warning/fail checks',
    strengths_json JSON NULL COMMENT 'AI & rule-extracted strengths',
    weaknesses_json JSON NULL COMMENT 'AI & rule-extracted weaknesses',
    recommendations_json JSON NULL COMMENT 'Actionable improvement recommendations',
    project_feedback_json JSON NULL COMMENT 'Per-project specific feedback',
    experience_feedback_json JSON NULL COMMENT 'Per-experience specific feedback',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_analysis_resume FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    INDEX idx_analysis_resume (resume_id),
    INDEX idx_analysis_created (created_at)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: job_descriptions
-- Job description input records
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    title VARCHAR(200) NULL,
    company VARCHAR(150) NULL,
    raw_text LONGTEXT NOT NULL,
    required_skills JSON NULL COMMENT 'Extracted mandatory skills',
    preferred_skills JSON NULL COMMENT 'Extracted optional/preferred skills',
    experience_level VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_job_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_job_user (user_id)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: job_matches
-- Semantic similarity, skill match, and gap analysis between resume and JD
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS job_matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    job_description_id INT NOT NULL,
    overall_match_percentage DECIMAL(5, 2) NOT NULL,
    semantic_similarity_score DECIMAL(5, 2) NOT NULL,
    skill_match_score DECIMAL(5, 2) NOT NULL,
    experience_relevance_score DECIMAL(5, 2) NOT NULL,
    matching_skills JSON NOT NULL COMMENT 'Skills present in both',
    missing_skills JSON NOT NULL COMMENT 'Skills required by JD but missing in resume',
    partial_skills JSON NULL COMMENT 'Related/partially matched skills',
    skill_gap_priority JSON NULL COMMENT 'Categorized by High/Medium/Low priority',
    learning_roadmap JSON NULL COMMENT 'AI-generated roadmap for missing skills',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_match_resume FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    CONSTRAINT fk_match_job FOREIGN KEY (job_description_id) REFERENCES job_descriptions(id) ON DELETE CASCADE,
    INDEX idx_match_resume (resume_id),
    INDEX idx_match_job (job_description_id)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Table: bullet_improvements
-- Line-by-line bullet rewrites without hallucination
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bullet_improvements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    analysis_id INT NOT NULL,
    original_text TEXT NOT NULL,
    suggested_text TEXT NOT NULL,
    reasoning TEXT NOT NULL,
    improvement_type VARCHAR(50) DEFAULT 'action_verb',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bullet_analysis FOREIGN KEY (analysis_id) REFERENCES resume_analysis(id) ON DELETE CASCADE,
    INDEX idx_bullet_analysis (analysis_id)
) ENGINE=InnoDB;

-- --------------------------------------------------------------------
-- Initial Seed: Core Skills Master Taxonomy
-- --------------------------------------------------------------------
INSERT IGNORE INTO skills_master (name, category, aliases) VALUES
-- Programming
('Python', 'Programming', '["py", "python3"]'),
('JavaScript', 'Programming', '["js", "es6", "ecmascript"]'),
('TypeScript', 'Programming', '["ts"]'),
('Java', 'Programming', '["core java", "j2ee"]'),
('C', 'Programming', '[]'),
('C++', 'Programming', '["cpp"]'),
('C#', 'Programming', '["csharp", ".net"]'),
('Go', 'Programming', '["golang"]'),
('Rust', 'Programming', '[]'),
('PHP', 'Programming', '[]'),
('Ruby', 'Programming', '[]'),
('Kotlin', 'Programming', '[]'),
('Swift', 'Programming', '[]'),

-- Web Development
('HTML5', 'Web Development', '["html"]'),
('CSS3', 'Web Development', '["css"]'),
('React', 'Web Development', '["react.js", "reactjs"]'),
('Node.js', 'Web Development', '["nodejs", "node"]'),
('Express.js', 'Web Development', '["express", "expressjs"]'),
('FastAPI', 'Web Development', '["fast api"]'),
('Django', 'Web Development', '[]'),
('Flask', 'Web Development', '[]'),
('Spring Boot', 'Web Development', '["springboot"]'),
('Angular', 'Web Development', '["angularjs"]'),
('Vue.js', 'Web Development', '["vue", "vuejs"]'),
('Next.js', 'Web Development', '["nextjs"]'),
('REST APIs', 'Web Development', '["restful", "rest api", "api development"]'),
('GraphQL', 'Web Development', '[]'),
('WebSockets', 'Web Development', '["websocket"]'),

-- Data & Databases
('SQL', 'Data & Databases', '["structured query language"]'),
('MySQL', 'Data & Databases', '[]'),
('PostgreSQL', 'Data & Databases', '["postgres"]'),
('MongoDB', 'Data & Databases', '["mongo"]'),
('Redis', 'Data & Databases', '[]'),
('Pandas', 'Data & Databases', '[]'),
('NumPy', 'Data & Databases', '[]'),
('Apache Spark', 'Data & Databases', '["spark", "pyspark"]'),
('SQLite', 'Data & Databases', '[]'),
('Elasticsearch', 'Data & Databases', '[]'),

-- AI & Machine Learning
('Machine Learning', 'AI & Machine Learning', '["ml"]'),
('Deep Learning', 'AI & Machine Learning', '["dl"]'),
('Natural Language Processing', 'AI & Machine Learning', '["nlp"]'),
('Computer Vision', 'AI & Machine Learning', '["cv"]'),
('TensorFlow', 'AI & Machine Learning', '["tf"]'),
('PyTorch', 'AI & Machine Learning', '[]'),
('Scikit-learn', 'AI & Machine Learning', '["sklearn"]'),
('spaCy', 'AI & Machine Learning', '[]'),
('Sentence Transformers', 'AI & Machine Learning', '["sbert"]'),
('HuggingFace', 'AI & Machine Learning', '["transformers"]'),
('Large Language Models', 'AI & Machine Learning', '["llms", "llm", "generative ai", "genai"]'),
('LangChain', 'AI & Machine Learning', '[]'),
('Gemini API', 'AI & Machine Learning', '["google gemini", "gemini"]'),

-- Cloud & DevOps
('Git', 'Cloud & DevOps', '[]'),
('GitHub', 'Cloud & DevOps', '[]'),
('Docker', 'Cloud & DevOps', '["containerization"]'),
('Kubernetes', 'Cloud & DevOps', '["k8s"]'),
('AWS', 'Cloud & DevOps', '["amazon web services"]'),
('Azure', 'Cloud & DevOps', '["microsoft azure"]'),
('Google Cloud Platform', 'Cloud & DevOps', '["gcp"]'),
('CI/CD', 'Cloud & DevOps', '["continuous integration", "continuous deployment", "github actions", "jenkins"]'),
('Linux', 'Cloud & DevOps', '["ubuntu", "bash", "unix"]'),
('Nginx', 'Cloud & DevOps', '[]'),

-- Soft Skills
('Problem Solving', 'Soft Skills', '["critical thinking", "analytical skills"]'),
('Team Collaboration', 'Soft Skills', '["teamwork", "cross-functional collaboration"]'),
('Communication', 'Soft Skills', '["verbal communication", "written communication"]'),
('Agile Methodologies', 'Soft Skills', '["agile", "scrum", "kanban"]'),
('Leadership', 'Soft Skills', '["team lead", "mentorship"]'),
('Time Management', 'Soft Skills', '["prioritization"]');
