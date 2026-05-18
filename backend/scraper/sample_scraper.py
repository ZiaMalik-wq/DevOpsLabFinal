"""
Sample scraper demonstrating how to parse HTML job listings using BeautifulSoup.
This is a demo/template — in production, concrete scrapers for LinkedIn, Rozee.pk, etc. would extend BaseScraper.
"""

from typing import List
from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper, RawJobPosting


# Sample HTML representing a job listing page (for demonstration)
SAMPLE_HTML = """
<html>
<body>
<div class="job-listings">
    <div class="job-card">
        <h2 class="title">Machine Learning Engineer</h2>
        <span class="company">TechCorp Pakistan</span>
        <span class="location">Lahore</span>
        <span class="salary">PKR 200K–300K</span>
        <p class="description">
            We are looking for an ML Engineer with strong Python, TensorFlow,
            and PyTorch skills. Experience with Docker, AWS, and CI/CD pipelines
            is required. Knowledge of NLP and deep learning is a plus.
        </p>
    </div>
    <div class="job-card">
        <h2 class="title">Full Stack Web Developer</h2>
        <span class="company">DevStudio Lahore</span>
        <span class="location">Lahore</span>
        <span class="salary">PKR 120K–180K</span>
        <p class="description">
            Join our team to build modern web applications using React, Node.js,
            and TypeScript. Experience with PostgreSQL, REST APIs, and Docker
            is highly preferred. Knowledge of Next.js is a bonus.
        </p>
    </div>
    <div class="job-card">
        <h2 class="title">Data Analyst</h2>
        <span class="company">Insights Analytics</span>
        <span class="location">Islamabad</span>
        <span class="salary">PKR 100K–150K</span>
        <p class="description">
            Seeking a data analyst proficient in SQL, Python, and Power BI.
            Experience with Pandas, data modeling, and ETL processes is required.
            Tableau experience is a plus.
        </p>
    </div>
    <div class="job-card">
        <h2 class="title">Cloud Infrastructure Engineer</h2>
        <span class="company">CloudBase Solutions</span>
        <span class="location">Karachi</span>
        <span class="salary">PKR 250K–350K</span>
        <p class="description">
            Design and manage cloud infrastructure on AWS. Must have hands-on
            experience with Terraform, Kubernetes, Docker, and CI/CD pipelines.
            Linux administration skills required.
        </p>
    </div>
    <div class="job-card">
        <h2 class="title">Cybersecurity Specialist</h2>
        <span class="company">SecureNet Pakistan</span>
        <span class="location">Islamabad</span>
        <span class="salary">PKR 180K–250K</span>
        <p class="description">
            We need a security specialist experienced in penetration testing,
            SIEM tools, and network security. OWASP knowledge and ethical hacking
            certifications are preferred. Incident response experience is a must.
        </p>
    </div>
</div>
</body>
</html>
"""


class SampleScraper(BaseScraper):
    """
    Demo scraper that parses sample HTML.
    Replace `SAMPLE_HTML` with actual HTTP responses in production.
    """

    def __init__(self):
        super().__init__(source_name="SamplePortal")

    def scrape(self, query: str = "", location: str = "", max_results: int = 50) -> List[RawJobPosting]:
        soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
        cards = soup.select(".job-card")
        results: List[RawJobPosting] = []

        for card in cards[:max_results]:
            title_el = card.select_one(".title")
            company_el = card.select_one(".company")
            location_el = card.select_one(".location")
            salary_el = card.select_one(".salary")
            desc_el = card.select_one(".description")

            job = RawJobPosting(
                title=title_el.get_text(strip=True) if title_el else "",
                company=company_el.get_text(strip=True) if company_el else "",
                location=location_el.get_text(strip=True) if location_el else "",
                source=self.source_name,
                salary=salary_el.get_text(strip=True) if salary_el else "",
                description=desc_el.get_text(strip=True) if desc_el else "",
            )

            # Apply filters if provided
            if query and query.lower() not in job.title.lower():
                continue
            if location and location.lower() not in job.location.lower():
                continue

            results.append(job)

        return results
