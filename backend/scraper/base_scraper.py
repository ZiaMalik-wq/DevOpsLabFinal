"""
Abstract base class for job scrapers.
"""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


@dataclass
class RawJobPosting:
    """Data class for a scraped job posting."""
    title: str
    company: str
    location: str
    source: str
    salary: str = ""
    posted_date: str = ""
    description: str = ""
    url: str = ""


class BaseScraper(ABC):
    """
    Abstract base scraper — all concrete scrapers should inherit from this.
    """

    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    def scrape(self, query: str = "", location: str = "", max_results: int = 50) -> List[RawJobPosting]:
        """
        Scrape job postings from the source.

        Args:
            query: Job title or keyword to search
            location: Location filter
            max_results: Maximum number of results to return

        Returns:
            List of RawJobPosting objects
        """
        pass

    def get_source_name(self) -> str:
        return self.source_name
