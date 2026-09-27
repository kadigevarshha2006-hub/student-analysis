"""
Comprehensive Canonical Skill Taxonomy Knowledge Base for ResumeAI.
Structured canonical skill definitions with bidirectional aliases across major engineering domains.
"""

SKILL_TAXONOMY = {
    "Programming": [
        {"name": "Python", "aliases": ["python", "py", "python3", "python 3", "cpython"]},
        {"name": "JavaScript", "aliases": ["javascript", "js", "ecmascript", "es6", "es2020", "vanilla js"]},
        {"name": "TypeScript", "aliases": ["typescript", "ts"]},
        {"name": "Java", "aliases": ["java", "core java", "j2ee", "jdk", "java 8", "java 11", "java 17"]},
        {"name": "C", "aliases": ["c language", "ansi c", "c programming"]},
        {"name": "C++", "aliases": ["c++", "cpp", "cplusplus", "c/c++"]},
        {"name": "C#", "aliases": ["c#", "csharp", ".net", "dotnet", "asp.net"]},
        {"name": "Go", "aliases": ["go", "golang", "go language"]},
        {"name": "Rust", "aliases": ["rust", "rustlang"]},
        {"name": "PHP", "aliases": ["php", "php7", "php8"]},
        {"name": "Ruby", "aliases": ["ruby", "ruby on rails", "rails"]},
        {"name": "Kotlin", "aliases": ["kotlin"]},
        {"name": "Swift", "aliases": ["swift", "swiftui"]},
        {"name": "Scala", "aliases": ["scala"]},
        {"name": "R", "aliases": ["r programming", "r language"]},
        {"name": "Dart", "aliases": ["dart", "flutter"]},
        {"name": "Bash", "aliases": ["bash", "shell scripting", "sh", "zsh", "shell script"]},
        {"name": "PowerShell", "aliases": ["powershell", "ps1"]},
        {"name": "SQL", "aliases": ["sql", "structured query language", "pl/sql", "t-sql", "relational database"]}
    ],
    "Web Development": [
        {"name": "HTML", "aliases": ["html", "html5", "semantic html"]},
        {"name": "CSS", "aliases": ["css", "css3", "sass", "scss", "less", "css flexbox", "css grid"]},
        {"name": "React", "aliases": ["react", "react.js", "reactjs", "react js"]},
        {"name": "Node.js", "aliases": ["node.js", "nodejs", "node", "node js"]},
        {"name": "Express.js", "aliases": ["express.js", "expressjs", "express", "express js"]},
        {"name": "FastAPI", "aliases": ["fastapi", "fast api"]},
        {"name": "Django", "aliases": ["django", "django rest framework", "drf"]},
        {"name": "Flask", "aliases": ["flask"]},
        {"name": "Spring Boot", "aliases": ["spring boot", "springboot", "spring framework", "spring"]},
        {"name": "Angular", "aliases": ["angular", "angularjs", "angular 2+", "angular 14", "angular 16"]},
        {"name": "Vue.js", "aliases": ["vue.js", "vuejs", "vue", "vue 3"]},
        {"name": "Next.js", "aliases": ["next.js", "nextjs", "next"]},
        {"name": "NestJS", "aliases": ["nestjs", "nest.js"]},
        {"name": "REST APIs", "aliases": ["rest apis", "rest api", "restful apis", "restful api", "restful", "rest", "api design", "rest endpoints"]},
        {"name": "GraphQL", "aliases": ["graphql", "apollo graphql", "apollo"]},
        {"name": "WebSockets", "aliases": ["websockets", "websocket", "socket.io"]},
        {"name": "Tailwind CSS", "aliases": ["tailwind css", "tailwind", "tailwindcss"]},
        {"name": "Bootstrap", "aliases": ["bootstrap", "bootstrap 5", "bootstrap 4"]},
        {"name": "Redux", "aliases": ["redux", "redux toolkit", "rtk", "redux-thunk"]},
        {"name": "Microservices", "aliases": ["microservices", "microservice architecture", "micro-services"]}
    ],
    "Data & Databases": [
        {"name": "MySQL", "aliases": ["mysql", "my-sql"]},
        {"name": "PostgreSQL", "aliases": ["postgresql", "postgres", "psql"]},
        {"name": "MongoDB", "aliases": ["mongodb", "mongo", "nosql"]},
        {"name": "Redis", "aliases": ["redis", "in-memory cache"]},
        {"name": "SQLite", "aliases": ["sqlite", "sqlite3"]},
        {"name": "Firebase", "aliases": ["firebase", "firestore", "firebase realtime database"]},
        {"name": "Oracle DB", "aliases": ["oracle database", "oracle db", "oracle sql"]},
        {"name": "Microsoft SQL Server", "aliases": ["mssql", "sql server", "ms sql"]},
        {"name": "Cassandra", "aliases": ["cassandra", "apache cassandra"]},
        {"name": "Elasticsearch", "aliases": ["elasticsearch", "elastic search", "elk", "opensearch"]},
        {"name": "Pandas", "aliases": ["pandas"]},
        {"name": "NumPy", "aliases": ["numpy"]},
        {"name": "Apache Spark", "aliases": ["apache spark", "spark", "pyspark"]},
        {"name": "Apache Kafka", "aliases": ["apache kafka", "kafka", "event streaming"]},
        {"name": "Data Warehousing", "aliases": ["data warehousing", "data warehouse", "snowflake", "bigquery", "redshift"]},
        {"name": "ETL Pipelines", "aliases": ["etl", "etl pipelines", "data pipeline", "data pipelines"]}
    ],
    "AI & Machine Learning": [
        {"name": "Machine Learning", "aliases": ["machine learning", "ml", "supervised learning", "unsupervised learning", "statistical modeling"]},
        {"name": "Deep Learning", "aliases": ["deep learning", "dl", "neural networks", "ann", "cnn", "rnn", "transformers"]},
        {"name": "Natural Language Processing", "aliases": ["natural language processing", "nlp", "text processing", "text classification"]},
        {"name": "Computer Vision", "aliases": ["computer vision", "cv", "opencv", "image processing", "yolo"]},
        {"name": "TensorFlow", "aliases": ["tensorflow", "tf", "tf2", "keras"]},
        {"name": "PyTorch", "aliases": ["pytorch", "torch"]},
        {"name": "Scikit-learn", "aliases": ["scikit-learn", "sklearn", "scikit learn"]},
        {"name": "Streamlit", "aliases": ["streamlit"]},
        {"name": "spaCy", "aliases": ["spacy"]},
        {"name": "NLTK", "aliases": ["nltk"]},
        {"name": "Sentence Transformers", "aliases": ["sentence transformers", "sbert", "sentence-transformers"]},
        {"name": "Hugging Face", "aliases": ["hugging face", "huggingface", "transformers"]},
        {"name": "Large Language Models", "aliases": ["large language models", "llms", "llm", "generative ai", "genai", "prompt engineering"]},
        {"name": "LangChain", "aliases": ["langchain"]},
        {"name": "LlamaIndex", "aliases": ["llamaindex", "llama-index"]},
        {"name": "Vector Databases", "aliases": ["vector databases", "vector database", "chromadb", "pinecone", "faiss", "milvus", "qdrant"]},
        {"name": "Gemini API", "aliases": ["gemini api", "google gemini", "gemini", "gemini pro", "gemini flash"]},
        {"name": "OpenAI API", "aliases": ["openai api", "gpt-4", "gpt-3.5", "chatgpt"]},
        {"name": "Data Visualization", "aliases": ["data visualization", "matplotlib", "seaborn", "plotly", "chart.js", "d3.js"]}
    ],
    "Cloud & DevOps": [
        {"name": "Git", "aliases": ["git", "version control", "vcs"]},
        {"name": "GitHub", "aliases": ["github", "gitlab", "bitbucket"]},
        {"name": "Docker", "aliases": ["docker", "containerization", "containers", "dockerfile", "docker compose"]},
        {"name": "Kubernetes", "aliases": ["kubernetes", "k8s"]},
        {"name": "AWS", "aliases": ["aws", "amazon web services", "ec2", "s3", "lambda", "rds", "cloudwatch"]},
        {"name": "Azure", "aliases": ["azure", "microsoft azure"]},
        {"name": "Google Cloud Platform", "aliases": ["google cloud", "google cloud platform", "gcp"]},
        {"name": "CI/CD", "aliases": ["ci/cd", "continuous integration", "continuous deployment", "github actions", "jenkins", "gitlab ci"]},
        {"name": "Linux", "aliases": ["linux", "ubuntu", "debian", "centos", "redhat", "unix"]},
        {"name": "Nginx", "aliases": ["nginx", "reverse proxy"]},
        {"name": "Terraform", "aliases": ["terraform", "iac", "infrastructure as code"]},
        {"name": "Ansible", "aliases": ["ansible"]},
        {"name": "Prometheus", "aliases": ["prometheus", "grafana", "monitoring"]}
    ],
    "Mobile Development": [
        {"name": "Flutter", "aliases": ["flutter"]},
        {"name": "React Native", "aliases": ["react native"]},
        {"name": "Android Development", "aliases": ["android development", "android studio", "android sdk"]},
        {"name": "iOS Development", "aliases": ["ios development", "xcode", "cocoapods"]}
    ],
    "Testing & QA": [
        {"name": "Unit Testing", "aliases": ["unit testing", "unit tests", "pytest", "junit", "jest", "mocha"]},
        {"name": "Selenium", "aliases": ["selenium", "selenium webdriver"]},
        {"name": "Postman", "aliases": ["postman", "api testing", "newman"]},
        {"name": "Cypress", "aliases": ["cypress", "playwright"]}
    ],
    "Soft Skills": [
        {"name": "Problem Solving", "aliases": ["problem solving", "analytical thinking", "critical thinking", "algorithms"]},
        {"name": "Team Collaboration", "aliases": ["team collaboration", "team player", "teamwork", "cross-functional"]},
        {"name": "Communication", "aliases": ["communication", "verbal communication", "written communication", "presentation skills"]},
        {"name": "Agile / Scrum", "aliases": ["agile", "scrum", "kanban", "sprint planning"]},
        {"name": "Leadership", "aliases": ["leadership", "mentorship", "team lead", "project lead"]},
        {"name": "Time Management", "aliases": ["time management", "prioritization", "multitasking"]}
    ]
}

# Bidirectional Canonical Mapping Lookup
CANONICAL_LOOKUP = {}
for category, skills in SKILL_TAXONOMY.items():
    for item in skills:
        canonical = item["name"]
        CANONICAL_LOOKUP[canonical.lower()] = canonical
        for alias in item["aliases"]:
            CANONICAL_LOOKUP[alias.lower()] = canonical

def get_canonical_skill(skill_str: str) -> str:
    """Returns the canonical normalized name for any alias or variant."""
    cleaned = skill_str.strip().lower()
    return CANONICAL_LOOKUP.get(cleaned, skill_str.strip())

def get_all_skills_flat():
    """Returns a flattened list of all skill definitions with their category."""
    flat = []
    for category, skills in SKILL_TAXONOMY.items():
        for item in skills:
            flat.append({
                "name": item["name"],
                "category": category,
                "aliases": item["aliases"]
            })
    return flat
