"""
Gemini API Service
Handles interactions with Google's Generative AI (Gemini) API.
"""

import google.generativeai as genai
from typing import Dict, List, Optional


class GeminiService:
    """Service for interacting with the Gemini API."""

    # Pricing per 1 million characters (Gemini 2.5 Flash)
    INPUT_COST_PER_MILLION = 0.35
    OUTPUT_COST_PER_MILLION = 1.05

    def __init__(self, api_key: str):
        """
        Initialize the Gemini service.

        Args:
            api_key: Google Generative AI API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

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
            Exception: If the API request fails
        """
        try:
            prompt = (
                f"What is the official legal name for the company that owns "
                f"and operates the website {website}?"
            )

            # Configure tool for Google Search grounding
            tool = genai.Tool(google_search=genai.GoogleSearch())

            # Generate content with grounding
            response = self.model.generate_content(
                prompt,
                tools=[tool]
            )

            # Extract legal name from response
            legal_name = response.text.strip() if response.text else None

            # Extract sources from grounding metadata
            sources = []
            if hasattr(response, 'grounding_metadata') and response.grounding_metadata:
                if hasattr(response.grounding_metadata, 'grounding_chunks'):
                    for chunk in response.grounding_metadata.grounding_chunks:
                        if hasattr(chunk, 'web') and chunk.web:
                            sources.append({
                                "url": chunk.web.uri,
                                "title": chunk.web.title if hasattr(chunk.web, 'title') else ""
                            })

            # Calculate estimated cost
            estimated_cost = self._calculate_cost(prompt, response.text or "")

            return {
                "legal_name": legal_name,
                "sources": sources,
                "estimated_cost": estimated_cost
            }

        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")

    def _calculate_cost(self, input_text: str, output_text: str) -> float:
        """
        Calculate the estimated cost of the API call.

        Args:
            input_text: The input prompt text
            output_text: The output response text

        Returns:
            Estimated cost in USD
        """
        input_chars = len(input_text)
        output_chars = len(output_text)

        input_cost = (input_chars / 1_000_000) * self.INPUT_COST_PER_MILLION
        output_cost = (output_chars / 1_000_000) * self.OUTPUT_COST_PER_MILLION

        return input_cost + output_cost
