"""
GLEIF API Service
Handles interactions with the Global Legal Entity Identifier Foundation API.
"""

import requests
from typing import List, Dict, Optional


class GLEIFService:
    """Service for interacting with the GLEIF API."""

    BASE_URL = "https://api.gleif.org/api/v1/lei-records"

    def search_lei(self, company_name: str) -> List[Dict]:
        """
        Search for LEI records by company name.

        Args:
            company_name: The name of the company to search for

        Returns:
            List of LEI records matching the company name

        Raises:
            requests.RequestException: If the API request fails
        """
        try:
            params = {
                "filter[fulltext]": company_name
            }

            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            return data.get("data", [])

        except requests.RequestException as e:
            raise Exception(f"Error searching GLEIF API: {str(e)}")

    @staticmethod
    def extract_lei_info(record: Dict) -> Optional[Dict]:
        """
        Extract relevant LEI information from a GLEIF record.

        Args:
            record: A single LEI record from the GLEIF API

        Returns:
            Dictionary containing extracted LEI information
        """
        if not record or "attributes" not in record:
            return None

        attributes = record["attributes"]
        entity = attributes.get("entity", {})
        legal_name = entity.get("legalName", {})
        legal_address = entity.get("legalAddress", {})

        return {
            "lei": attributes.get("lei"),
            "legal_name": legal_name.get("name"),
            "address_lines": legal_address.get("addressLines", []),
            "city": legal_address.get("city"),
            "region": legal_address.get("region"),
            "country": legal_address.get("country"),
            "postal_code": legal_address.get("postalCode")
        }
