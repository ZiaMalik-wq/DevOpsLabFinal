"""
NLP-based skill extraction from job descriptions.
Uses a curated dictionary + regex matching (no spaCy dependency).
"""

import re
from typing import List

# ─── Skill Dictionary ────────────────────────────────────
# Canonical skill names with aliases / synonyms
SKILL_DICTIONARY: dict[str, list[str]] = {
    # AI / ML
    "Python":           ["python", "python3"],
    "TensorFlow":       ["tensorflow", "tensor flow"],
    "PyTorch":          ["pytorch", "py torch"],
    "Scikit-Learn":     ["scikit-learn", "sklearn", "scikit learn", "machine learning", "ml"],
    "NLP":              ["nlp", "natural language processing", "text mining", "text classification"],
    "Computer Vision":  ["computer vision", "image recognition", "object detection"],
    "LLMs":             ["llms", "llm", "large language model", "large language models", "gpt", "chatgpt", "generative ai"],
    "Deep Learning":    ["deep learning", "deep-learning", "neural network", "neural networks", "cnn", "rnn", "lstm"],
    "MLOps":            ["mlops", "ml ops", "ml operations", "model deployment"],
    "Hugging Face":     ["hugging face", "huggingface", "transformers"],
    # Web Dev
    "React":            ["react", "reactjs", "react.js"],
    "Node.js":          ["node.js", "nodejs", "node"],
    "TypeScript":       ["typescript", "ts"],
    "Next.js":          ["next.js", "nextjs", "next"],
    "Vue.js":           ["vue.js", "vuejs", "vue"],
    "Angular":          ["angular", "angularjs"],
    "HTML/CSS":         ["html", "css", "html/css", "html5", "css3"],
    "REST APIs":        ["rest api", "rest apis", "restful", "rest"],
    "GraphQL":          ["graphql", "graph ql"],
    "Tailwind CSS":     ["tailwind", "tailwindcss", "tailwind css"],
    "JavaScript":       ["javascript", "js", "ecmascript", "es6"],
    # Data
    "SQL":              ["sql", "mysql", "mssql", "t-sql", "plsql"],
    "Power BI":         ["power bi", "powerbi"],
    "Tableau":          ["tableau"],
    "Pandas":           ["pandas"],
    "Apache Spark":     ["apache spark", "spark", "pyspark"],
    "MongoDB":          ["mongodb", "mongo"],
    "PostgreSQL":       ["postgresql", "postgres", "psql"],
    "ETL":              ["etl", "extract transform load"],
    "Data Modeling":    ["data modeling", "data modelling", "data model"],
    "Snowflake":        ["snowflake"],
    "Redis":            ["redis"],
    "Excel":            ["excel", "ms excel", "microsoft excel"],
    # Cloud / DevOps
    "AWS":              ["aws", "amazon web services", "ec2", "s3"],
    "Docker":           ["docker", "dockerfile", "containerization", "container"],
    "Kubernetes":       ["kubernetes", "k8s", "kube"],
    "CI/CD":            ["ci/cd", "cicd", "ci cd", "continuous integration", "continuous deployment", "pipeline", "pipelines"],
    "Terraform":        ["terraform", "infrastructure as code"],
    "Azure":            ["azure", "microsoft azure"],
    "GCP":              ["gcp", "google cloud", "google cloud platform"],
    "Linux":            ["linux", "ubuntu", "centos", "debian"],
    "Ansible":          ["ansible"],
    "Jenkins":          ["jenkins"],
    "Git":              ["git", "github", "gitlab", "version control"],
    # Cyber Security
    "Penetration Testing": ["penetration testing", "pen testing", "pentest"],
    "SIEM":             ["siem", "security information"],
    "SOC":              ["soc", "security operations"],
    "Network Security": ["network security"],
    "Ethical Hacking":  ["ethical hacking", "white hat"],
    "Cryptography":     ["cryptography", "encryption"],
    "OWASP":            ["owasp"],
    "IAM":              ["iam", "identity and access management"],
    "Zero Trust":       ["zero trust"],
    "Incident Response":["incident response", "ir"],
    # Other
    "Product Management": ["product management", "product manager"],
    "Agile":            ["agile", "scrum", "kanban"],
}

# Pre-compile patterns for efficient matching
_PATTERNS: list[tuple[str, re.Pattern]] = []
for canonical, aliases in SKILL_DICTIONARY.items():
    # Sort by length (longest first) to avoid partial matches
    sorted_aliases = sorted(aliases, key=len, reverse=True)
    pattern = "|".join(re.escape(a) for a in sorted_aliases)
    _PATTERNS.append((canonical, re.compile(rf"\b(?:{pattern})\b", re.IGNORECASE)))


def extract_skills(text: str) -> List[str]:
    """
    Extract canonical skill names from a text (e.g. job description).
    Returns a deduplicated list of matched skills.
    """
    found: list[str] = []
    for canonical, pattern in _PATTERNS:
        if pattern.search(text):
            found.append(canonical)
    return found


def normalize_skill(raw: str) -> str:
    """
    Normalize a raw skill string to its canonical form.
    Returns the original string if no match is found.
    """
    lower = raw.strip().lower()
    for canonical, aliases in SKILL_DICTIONARY.items():
        if lower in aliases or lower == canonical.lower():
            return canonical
    return raw.strip()
