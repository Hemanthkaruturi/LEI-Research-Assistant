"""
Gemini API Service
Handles interactions with Google's Generative AI (Gemini) API using google.genai client.
"""

import re
import time
from typing import Dict, List, Optional
import google.genai as genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch


class GeminiService:
    """Service for interacting with the Gemini API with Google Search grounding."""

    # Pricing per 1 million tokens (Gemini 2.5 Flash)
    INPUT_COST_PER_MILLION_TOKENS = 0.075  # $0.075 per 1M input tokens
    OUTPUT_COST_PER_MILLION_TOKENS = 0.30   # $0.30 per 1M output tokens

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        Initialize the Gemini service.

        Args:
            api_key: Google Generative AI API key
            model: Model name to use (default: gemini-2.5-flash)
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.google_search_tool = Tool(google_search=GoogleSearch())

    def verify_company_name_from_website(self, website: str) -> Dict:
        """
        Verify the legal company name from a website using Google Search grounding.

        Args:
            website: The website URL to verify

        Returns:
            Dictionary containing:
                - legal_name: The verified legal name
                - sources: List of source URLs used for verification
                - estimated_cost: Estimated API cost in USD

        Raises:
            Exception: If the API request fails after retries
        """
        prompt = (
            f"What is the official legal name for the company that owns "
            f"and operates the website {website}?"
        )

        # Retry logic with exponential backoff
        for attempt in range(4):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=GenerateContentConfig(
                        tools=[self.google_search_tool],
                        response_modalities=["TEXT"],
                    )
                )
                break  # Success, exit retry loop

            except Exception as e:
                if attempt == 3:  # Last attempt
                    raise Exception(f"Error calling Gemini API after 4 attempts: {str(e)}")

                # Extract retry delay from error or use default
                delay = self._extract_retry_delay(str(e)) or 60
                print(f"Gemini Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
                time.sleep(delay)

        # Extract legal name from response
        legal_name = response.text.strip() if response.text else None

        # Extract sources from grounding metadata
        sources = self._extract_sources(response)

        # Calculate estimated cost
        estimated_cost = self._calculate_cost(response)

        return {
            "legal_name": legal_name,
            "sources": sources,
            "estimated_cost": estimated_cost
        }

    def _extract_sources(self, response) -> List[Dict[str, str]]:
        """
        Extract source URLs from grounding metadata.

        Args:
            response: Gemini API response

        Returns:
            List of dictionaries with 'url' and 'title' keys
        """
        sources = []

        # Check if grounding metadata exists
        if not hasattr(response, 'candidates') or not response.candidates:
            return sources

        for candidate in response.candidates:
            if not hasattr(candidate, 'grounding_metadata'):
                continue

            grounding_metadata = candidate.grounding_metadata
            if not hasattr(grounding_metadata, 'grounding_chunks'):
                continue

            # Extract URLs from grounding chunks
            for chunk in grounding_metadata.grounding_chunks:
                if hasattr(chunk, 'web') and chunk.web:
                    sources.append({
                        "url": chunk.web.uri if hasattr(chunk.web, 'uri') else "",
                        "title": chunk.web.title if hasattr(chunk.web, 'title') else ""
                    })

        return sources

    def _calculate_cost(self, response) -> float:
        """
        Calculate the estimated cost of the API call based on token usage.

        Args:
            response: Gemini API response

        Returns:
            Estimated cost in USD
        """
        try:
            if hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                input_tokens = usage.prompt_token_count if hasattr(usage, 'prompt_token_count') else 0
                output_tokens = usage.candidates_token_count if hasattr(usage, 'candidates_token_count') else 0

                input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MILLION_TOKENS
                output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MILLION_TOKENS

                return input_cost + output_cost
        except:
            pass

        return 0.0

    @staticmethod
    def _extract_retry_delay(error_string: str) -> Optional[int]:
        """
        Extract retry delay number from error string.

        Args:
            error_string: Error message string

        Returns:
            Retry delay in seconds, or None if not found
        """
        retry_info_pattern = r"'retryDelay': '(\d+)"
        match = re.search(retry_info_pattern, error_string)
        return int(match.group(1)) if match else None
