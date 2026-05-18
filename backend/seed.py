"""
Seed the database with initial mock data matching the frontend.
"""

import random
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import Skill, SkillDemand, JobPosting, User, UserSkill, Course, RegionalDemand


MONTHS = [
    "Apr 25", "May 25", "Jun 25", "Jul 25", "Aug 25", "Sep 25",
    "Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26",
]


def _trend(base: int, growth: float) -> list[int]:
    return [round(base + growth * i + (random.random() * 8 - 4)) for i in range(12)]


SKILLS_DATA = [
    ("Python",             "AI / ML",         82,  1.2,  "$105K"),
    ("TensorFlow",         "AI / ML",         60,  0.9,  "$115K"),
    ("PyTorch",            "AI / ML",         55,  1.8,  "$118K"),
    ("NLP",                "AI / ML",         45,  2.1,  "$120K"),
    ("LLMs",               "AI / ML",         30,  3.5,  "$135K"),
    ("Deep Learning",      "AI / ML",         50,  1.4,  "$122K"),
    ("Computer Vision",    "AI / ML",         40,  1.0,  "$112K"),
    ("MLOps",              "AI / ML",         25,  2.8,  "$125K"),
    ("Scikit-Learn",       "AI / ML",         48,  0.7,  "$100K"),
    ("Hugging Face",       "AI / ML",         20,  3.0,  "$128K"),
    ("React",              "Web Dev",         90,  0.5,  "$95K"),
    ("Node.js",            "Web Dev",         78,  0.3,  "$92K"),
    ("TypeScript",         "Web Dev",         70,  1.5,  "$98K"),
    ("Next.js",            "Web Dev",         40,  2.2,  "$100K"),
    ("Vue.js",             "Web Dev",         35,  0.2,  "$88K"),
    ("Angular",            "Web Dev",         45,  0.1,  "$90K"),
    ("HTML/CSS",           "Web Dev",         92,  0.1,  "$75K"),
    ("REST APIs",          "Web Dev",         75,  0.4,  "$88K"),
    ("GraphQL",            "Web Dev",         28,  1.1,  "$96K"),
    ("Tailwind CSS",       "Web Dev",         42,  1.9,  "$85K"),
    ("SQL",                "Data",            88,  0.3,  "$85K"),
    ("Power BI",           "Data",            55,  1.1,  "$82K"),
    ("Pandas",             "Data",            62,  0.8,  "$90K"),
    ("Apache Spark",       "Data",            38,  1.3,  "$110K"),
    ("MongoDB",            "Data",            50,  0.6,  "$88K"),
    ("PostgreSQL",         "Data",            56,  0.9,  "$90K"),
    ("Tableau",            "Data",            40,  0.5,  "$80K"),
    ("ETL",                "Data",            35,  0.8,  "$92K"),
    ("Data Modeling",      "Data",            30,  0.6,  "$88K"),
    ("Snowflake",          "Data",            22,  2.0,  "$105K"),
    ("AWS",                "Cloud / DevOps",  85,  0.7,  "$115K"),
    ("Docker",             "Cloud / DevOps",  72,  1.0,  "$105K"),
    ("Kubernetes",         "Cloud / DevOps",  58,  1.6,  "$120K"),
    ("Terraform",          "Cloud / DevOps",  35,  2.0,  "$118K"),
    ("CI/CD",              "Cloud / DevOps",  65,  0.9,  "$100K"),
    ("Azure",              "Cloud / DevOps",  50,  0.8,  "$112K"),
    ("GCP",                "Cloud / DevOps",  40,  1.2,  "$115K"),
    ("Linux",              "Cloud / DevOps",  70,  0.3,  "$95K"),
    ("Ansible",            "Cloud / DevOps",  30,  0.5,  "$98K"),
    ("Jenkins",            "Cloud / DevOps",  38,  0.2,  "$90K"),
    ("Penetration Testing","Cyber Security",  42,  1.4,  "$108K"),
    ("SIEM",               "Cyber Security",  38,  1.2,  "$102K"),
    ("Network Security",   "Cyber Security",  55,  0.5,  "$95K"),
    ("Ethical Hacking",    "Cyber Security",  30,  1.8,  "$100K"),
    ("OWASP",              "Cyber Security",  25,  0.9,  "$96K"),
    ("IAM",                "Cyber Security",  28,  1.0,  "$98K"),
    ("Zero Trust",         "Cyber Security",  18,  2.2,  "$105K"),
    ("Incident Response",  "Cyber Security",  32,  0.8,  "$100K"),
    ("Cryptography",       "Cyber Security",  20,  0.6,  "$102K"),
    ("SOC",                "Cyber Security",  24,  1.0,  "$95K"),
]

JOBS_DATA = [
    (1,  "ML Engineer",            "Systems Limited",     "Lahore",    "LinkedIn", ["Python","TensorFlow","PyTorch","Docker","AWS","MLOps"],                     "PKR 180K–250K", "2026-03-01", "We are looking for a skilled ML Engineer to design, develop and deploy machine learning models at scale. You will work with large datasets and build production-ready pipelines."),
    (2,  "Full Stack Developer",   "Arbisoft",            "Lahore",    "LinkedIn", ["React","Node.js","TypeScript","PostgreSQL","Docker","REST APIs"],           "PKR 150K–220K", "2026-02-28", "Join our team to build full-stack web applications using modern JavaScript frameworks. Experience with cloud deployment is a plus."),
    (3,  "Data Analyst",           "Jazz (VEON)",         "Islamabad", "Rozee.pk", ["SQL","Power BI","Python","Pandas","Excel","Data Modeling"],                "PKR 120K–170K", "2026-03-03", "Seeking a data-driven analyst to extract insights from telecom data and build dashboards for stakeholders."),
    (4,  "Cloud Engineer",         "Contour Software",    "Karachi",   "LinkedIn", ["AWS","Terraform","Docker","Kubernetes","CI/CD","Linux"],                   "PKR 200K–300K", "2026-03-02", "Design and manage cloud infrastructure for SaaS products. Strong AWS knowledge required."),
    (5,  "AI Research Intern",     "LUMS SBASSE",         "Lahore",    "University",["Python","NLP","Deep Learning","PyTorch","Hugging Face","LLMs"],           "PKR 40K–60K",   "2026-02-25", "Research position focused on NLP and large language models. Ideal for final-year CS students."),
    (6,  "Frontend Developer",     "VentureDive",         "Karachi",   "LinkedIn", ["React","TypeScript","Next.js","Tailwind CSS","GraphQL","HTML/CSS"],        "PKR 130K–180K", "2026-03-05", "Build beautiful and performant user interfaces for enterprise clients using React ecosystem."),
    (7,  "Cybersecurity Analyst",  "PTCL",                "Islamabad", "Rozee.pk", ["SIEM","Network Security","Penetration Testing","IAM","Incident Response"],"PKR 140K–200K", "2026-02-20", "Monitor and protect our network infrastructure. Experience with SIEM tools and incident handling required."),
    (8,  "Backend Developer",      "Netsol Technologies", "Lahore",    "LinkedIn", ["Node.js","PostgreSQL","Docker","REST APIs","TypeScript","Redis"],          "PKR 140K–190K", "2026-03-04", "Build scalable backend services for fintech applications."),
    (9,  "Data Scientist",         "Afiniti",             "Lahore",    "LinkedIn", ["Python","Scikit-Learn","NLP","TensorFlow","SQL","Apache Spark"],           "PKR 220K–350K", "2026-03-01", "Apply ML and statistical models to real-world problems in customer engagement optimization."),
    (10, "DevOps Engineer",        "10Pearls",            "Karachi",   "LinkedIn", ["Docker","Kubernetes","AWS","Jenkins","Terraform","CI/CD","Ansible"],       "PKR 180K–260K", "2026-02-27", "Automate and streamline development and deployment pipelines."),
    (11, "NLP Engineer",           "Hazelsoft",           "Lahore",    "Indeed",   ["Python","NLP","LLMs","Hugging Face","Deep Learning","PyTorch"],            "PKR 160K–230K", "2026-03-06", "Develop NLP solutions including chatbots, text classification, and entity extraction systems."),
    (12, "React Native Developer", "Techlogix",           "Lahore",    "LinkedIn", ["React","TypeScript","REST APIs","Node.js","MongoDB","Git"],                "PKR 120K–170K", "2026-03-02", "Build cross-platform mobile applications for enterprise clients."),
    (13, "BI Analyst",             "Teradata Pakistan",   "Islamabad", "Rozee.pk", ["Power BI","SQL","Tableau","ETL","Data Modeling","Python"],                 "PKR 130K–180K", "2026-02-22", "Create reports and dashboards for data-driven decision-making across departments."),
    (14, "Security Engineer",      "ISEC Services",       "Lahore",    "Indeed",   ["Ethical Hacking","OWASP","Penetration Testing","Cryptography","Zero Trust"],"PKR 160K–220K","2026-03-03", "Conduct security assessments and vulnerability testing for client systems."),
    (15, "Platform Engineer",      "Airlift (Tech)",      "Lahore",    "LinkedIn", ["Kubernetes","Docker","Terraform","AWS","GCP","CI/CD","Linux"],             "PKR 250K–350K", "2026-03-07", "Build and maintain internal developer platforms and infrastructure automation."),
    (16, "AI Product Manager",     "Careem",              "Lahore",    "LinkedIn", ["Python","LLMs","NLP","Product Management","SQL","Data Modeling"],          "PKR 300K–450K", "2026-03-08", "Lead AI product strategy, working at the intersection of ML and business impact."),
    (17, "Computer Vision Engineer","RetrocausalAI",      "Islamabad", "LinkedIn", ["Python","Computer Vision","PyTorch","Deep Learning","TensorFlow","Docker"],"PKR 200K–280K", "2026-02-18", "Develop computer vision models for autonomous systems and quality inspection."),
    (18, "Data Engineer",          "Folio3",              "Karachi",   "LinkedIn", ["Python","Apache Spark","AWS","PostgreSQL","ETL","Snowflake","SQL"],        "PKR 170K–240K", "2026-03-04", "Design and build data pipelines and warehouse solutions for analytics teams."),
    (19, "Angular Developer",      "i2c Inc.",            "Lahore",    "Rozee.pk", ["Angular","TypeScript","REST APIs","HTML/CSS","Node.js","SQL"],             "PKR 110K–160K", "2026-02-28", "Develop enterprise payment solutions using Angular framework."),
    (20, "MLOps Engineer",         "Afiniti",             "Lahore",    "LinkedIn", ["MLOps","Docker","Kubernetes","Python","AWS","CI/CD","TensorFlow"],         "PKR 220K–320K", "2026-03-09", "Build and manage ML model deployment pipelines and monitoring systems."),
]

USER_SKILLS = [
    ("Python", 75), ("React", 60), ("SQL", 70), ("HTML/CSS", 85),
    ("Node.js", 50), ("MongoDB", 40), ("Git", 65), ("REST APIs", 55),
]

COURSES_DATA = [
    ("LLMs",               "LangChain & LLM Application Development",     "DeepLearning.AI",  "Coursera",         "6 weeks",  4.8, "Intermediate", "#", "🤖"),
    ("PyTorch",            "Deep Learning with PyTorch",                   "Meta",             "Coursera",         "8 weeks",  4.7, "Intermediate", "#", "🔥"),
    ("NLP",                "Natural Language Processing Specialization",   "DeepLearning.AI",  "Coursera",         "12 weeks", 4.8, "Intermediate", "#", "📝"),
    ("Kubernetes",         "Kubernetes for Developers (LFD259)",           "Linux Foundation", "edX",              "5 weeks",  4.6, "Advanced",     "#", "☸️"),
    ("Terraform",          "HashiCorp Terraform Associate Certification",  "HashiCorp",        "Udemy",            "4 weeks",  4.5, "Intermediate", "#", "🏗️"),
    ("MLOps",              "Machine Learning Engineering for Production",  "DeepLearning.AI",  "Coursera",         "10 weeks", 4.7, "Advanced",     "#", "⚙️"),
    ("TypeScript",         "Understanding TypeScript",                     "Academind",        "Udemy",            "3 weeks",  4.7, "Beginner",     "#", "📘"),
    ("Docker",             "Docker & Kubernetes: The Practical Guide",     "Academind",        "Udemy",            "4 weeks",  4.8, "Beginner",     "#", "🐳"),
    ("Deep Learning",      "Deep Learning Specialization",                 "DeepLearning.AI",  "Coursera",         "16 weeks", 4.9, "Intermediate", "#", "🧠"),
    ("TensorFlow",         "TensorFlow Developer Professional Certificate","Google",           "Coursera",         "10 weeks", 4.7, "Intermediate", "#", "📊"),
    ("AWS",                "AWS Solutions Architect Associate",             "Amazon",           "AWS Training",     "8 weeks",  4.6, "Intermediate", "#", "☁️"),
    ("Penetration Testing","Practical Ethical Hacking",                    "TCM Security",     "Udemy",            "6 weeks",  4.8, "Intermediate", "#", "🔒"),
    ("Next.js",            "Next.js 14 & React — The Complete Guide",      "Academind",        "Udemy",            "5 weeks",  4.8, "Intermediate", "#", "▲"),
    ("Apache Spark",       "Apache Spark with Scala",                      "Databricks",       "Coursera",         "6 weeks",  4.5, "Advanced",     "#", "⚡"),
    ("Power BI",           "Microsoft Power BI Data Analyst (PL-300)",     "Microsoft",        "Microsoft Learn",  "4 weeks",  4.6, "Beginner",     "#", "📈"),
]

REGIONAL_DATA = {
    "Lahore":    [120, 128, 135, 142, 155, 160, 165, 172, 180, 188, 195, 210],
    "Karachi":   [100, 105, 108, 115, 118, 125, 130, 135, 138, 142, 150, 158],
    "Islamabad": [85,  90,  92,  98,  105, 108, 112, 118, 120, 125, 132, 140],
}


def seed_database():
    """Populate the database with initial data."""
    db: Session = SessionLocal()
    try:
        # Check if data already exists
        from models import Skill as SkillModel
        if db.query(SkillModel).count() > 0:
            print("Database already seeded. Skipping.")
            return

        random.seed(42)  # Reproducible trend data

        # 1. Seed skills + demand data
        for name, category, base, growth, salary in SKILLS_DATA:
            skill = Skill(name=name, category=category, avg_salary=salary)
            db.add(skill)
            db.flush()  # Get the ID

            demand_values = _trend(base, growth)
            for i, month in enumerate(MONTHS):
                db.add(SkillDemand(skill_id=skill.id, month=month, demand_count=demand_values[i]))

        # 2. Seed job postings
        for id_, title, company, location, source, skills, salary, posted, desc in JOBS_DATA:
            db.add(JobPosting(
                title=title, company=company, location=location, source=source,
                salary=salary, posted_date=posted, description=desc, raw_skills=skills,
            ))

        # 3. Seed user
        user = User(
            name="Hussnain Raza",
            email="hussnain@example.com",
            university="COMSATS University Islamabad, Lahore",
            degree="BS Computer Science",
            semester=8,
        )
        db.add(user)
        db.flush()

        for skill_name, prof in USER_SKILLS:
            db.add(UserSkill(user_id=user.id, skill_name=skill_name, proficiency=prof))

        # 4. Seed courses
        for skill, title, provider, platform, duration, rating, level, url, icon in COURSES_DATA:
            db.add(Course(
                skill=skill, title=title, provider=provider, platform=platform,
                duration=duration, rating=rating, level=level, url=url, icon=icon,
            ))

        # 5. Seed regional demand
        for region, data in REGIONAL_DATA.items():
            for i, month in enumerate(MONTHS):
                db.add(RegionalDemand(region=region, month=month, job_count=data[i]))

        db.commit()
        print(f"Database seeded: {len(SKILLS_DATA)} skills, {len(JOBS_DATA)} jobs, 1 user, {len(COURSES_DATA)} courses, {len(REGIONAL_DATA)} regions")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_database()
