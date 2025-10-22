"""
LEI Lookup Orchestrator
Main business logic for finding and verifying Legal Entity Identifiers.
"""

import re
from typing import Dict, Optional, List
from .services.gleif_service import GLEIFClient
from .services.gemini_service import GeminiService


class LEILookup:
    """Orchestrates the LEI lookup and verification process."""

    def __init__(self, gemini_api_key: str):
        """
        Initialize the LEI lookup service.

        Args:
            gemini_api_key: Google Generative AI API key
        """
        self.gleif_client = GLEIFClient()
        self.gemini_service = GeminiService(gemini_api_key)

    def find_lei(self, company_name: str, website: str) -> Dict:
        """
        Find and verify LEI for a company using a 4-step process:
        1. Search GLEIF database for company name
        2. Verify legal name from website using Gemini
        3. Match names using flexible algorithm
        4. Return verified LEI information

        Args:
            company_name: The name of the company
            website: The company's website URL

        Returns:
            Dictionary containing:
                - success: Boolean indicating if LEI was found
                - lei: The LEI code (if found)
                - legal_name: The verified legal name
                - address: Full address details
                - sources: Verification sources
                - estimated_cost: API cost
                - message: Info/error message (if applicable)
        """
        try:
            # Step 1: Search GLEIF database
            lei_records = self.gleif_client.get_lei_by_company_name(company_name)

            if not lei_records:
                return {
                    "success": False,
                    "message": f"No LEI records found for '{company_name}'. This company may not have a registered LEI."
                }

            # Step 2: Verify legal name from website
            gemini_result = self.gemini_service.verify_company_name_from_website(website)
            gemini_legal_name = gemini_result.get("legal_name")

            if not gemini_legal_name:
                return {
                    "success": False,
                    "message": "Could not verify company name from the provided website."
                }

            # Step 3: Match names
            matched_record = self._find_matching_record(lei_records, gemini_legal_name)

            if not matched_record:
                return {
                    "success": False,
                    "message": (
                        f"Found LEI records for '{company_name}', but could not verify "
                        f"a match with the legal name from the website. "
                        f"Please ensure the website URL is accurate."
                    )
                }

            # Step 4: Return verified information
            # Note: matched_record is already in the simplified format from GLEIFClient
            return {
                "success": True,
                "lei": matched_record["lei"],
                "legal_name": matched_record["legal_name"],
                "address": matched_record["address"],
                "sources": gemini_result.get("sources", []),
                "estimated_cost": gemini_result.get("estimated_cost", 0.0)
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error during LEI lookup: {str(e)}"
            }

    def _find_matching_record(self, records: List[Dict], gemini_name: str) -> Optional[Dict]:
        """
        Find a matching LEI record using flexible name matching.

        Args:
            records: List of GLEIF LEI records (already in simplified format)
            gemini_name: Legal name verified by Gemini

        Returns:
            Matching LEI record or None
        """
        normalized_gemini = self._normalize_name(gemini_name)

        for record in records:
            if not record.get("legal_name"):
                continue

            normalized_gleif = self._normalize_name(record["legal_name"])

            # Bidirectional matching: check if either name contains the other
            if normalized_gemini in normalized_gleif or normalized_gleif in normalized_gemini:
                return record

        return None

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Normalize company name for flexible matching.

        Removes common suffixes, punctuation, and normalizes whitespace.

        Args:
            name: Company name to normalize

        Returns:
            Normalized name
        """
        # Convert to lowercase
        normalized = name.lower()

        # Remove common company suffixes
        suffixes = [
            r'\binc\.?\b',
            r'\bincorporated\b',
            r'\bllc\.?\b',
            r'\bl\.l\.c\.?\b',
            r'\bltd\.?\b',
            r'\blimited\b',
            r'\bl\.t\.d\.?\b',
            r'\bcorp\.?\b',
            r'\bcorporation\b',
            r'\bgmbh\.?\b',
            r'\bag\.?\b',
            r'\bsa\.?\b',
            r'\bsarl\.?\b',
            r'\bplc\.?\b',
            r'\bco\.?\b',
            r'\bcompany\b'
        ]

        for suffix in suffixes:
            normalized = re.sub(suffix, '', normalized)

        # Remove punctuation
        normalized = re.sub(r'[^\w\s]', '', normalized)

        # Normalize whitespace
        normalized = ' '.join(normalized.split())

        return normalized.strip()
