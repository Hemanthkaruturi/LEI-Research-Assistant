"""
GLEIF API Client
A client for interacting with the GLEIF (Global Legal Entity Identifier Foundation) API.

API Documentation: https://documenter.getpostman.com/view/7679680/SVYrrxuU
Rate Limit: 60 requests per minute per user
"""

import requests
from typing import List, Dict, Optional


class GLEIFClient:
    """
    A client for interacting with the GLEIF (Global Legal Entity Identifier Foundation) API.

    This client provides methods to search for Legal Entity Identifiers (LEI) by company name
    and retrieve detailed LEI records.
    """

    BASE_URL = "https://api.gleif.org/api/v1"
    DEFAULT_TIMEOUT = 15
    DEFAULT_PAGE_SIZE = 10

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        """
        Initialize the GLEIF API client.

        Args:
            timeout: Request timeout in seconds (default: 15)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/vnd.api+json'
        })

    def get_lei_by_company_name(
        self,
        company_name: str,
        page_size: int = DEFAULT_PAGE_SIZE,
        filter_by_country: Optional[str] = None,
        filter_by_status: Optional[str] = "ACTIVE"
    ) -> List[Dict]:
        """
        Search for LEI records by company name.

        The GLEIF API supports fuzzy matching, so it will return companies
        that match or are similar to the provided company name.

        Args:
            company_name: The name of the company to search for
            page_size: Number of results to return (default: 10, max: 200)
            filter_by_country: Optional ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB')
            filter_by_status: Filter by entity status (default: 'ACTIVE', or None for all)

        Returns:
            A list of dictionaries containing LEI information for matching companies.
            Each dictionary contains:
                - lei: The LEI code
                - legal_name: The legal name of the entity
                - status: The status of the LEI record
                - country: Country code
                - city: City
                - address: Full legal address
                - registration_date: Initial registration date
                - last_update: Last update date

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        if not company_name or not company_name.strip():
            raise ValueError("Company name cannot be empty")

        # Build query parameters
        params = {
            'filter[entity.legalName]': company_name.strip(),
            'page[size]': min(page_size, 200),  # API max is 200
            'page[number]': 1
        }

        # Add optional filters
        if filter_by_country:
            params['filter[entity.legalAddress.country]'] = filter_by_country.upper()

        if filter_by_status:
            params['filter[entity.status]'] = filter_by_status.upper()

        endpoint = f"{self.BASE_URL}/lei-records"

        try:
            print(f"Searching for company: {company_name}")
            response = self.session.get(
                endpoint,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

            # Parse JSON-API response
            data = response.json()
            results = self._parse_lei_records(data)

            print(f"Found {len(results)} matching record(s)")
            return results

        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to GLEIF API. Check your network connection.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching LEI data: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def get_lei_record(self, lei_code: str) -> Optional[Dict]:
        """
        Retrieve detailed information for a specific LEI code.

        Args:
            lei_code: The 20-character LEI code to look up

        Returns:
            A dictionary containing detailed LEI information, or None if not found.
            Contains the same fields as get_lei_by_company_name().

        Raises:
            ValueError: If LEI code format is invalid
            requests.exceptions.RequestException: If the API request fails
        """
        if not lei_code or len(lei_code) != 20:
            raise ValueError("LEI code must be exactly 20 characters")

        endpoint = f"{self.BASE_URL}/lei-records/{lei_code.strip().upper()}"

        try:
            print(f"Looking up LEI: {lei_code}")
            response = self.session.get(endpoint, timeout=self.timeout)

            if response.status_code == 404:
                print(f"LEI code not found: {lei_code}")
                return None

            response.raise_for_status()

            # Parse JSON-API response
            data = response.json()
            results = self._parse_lei_records(data)

            return results[0] if results else None

        except requests.exceptions.Timeout:
            raise Exception(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise Exception(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to GLEIF API. Check your network connection.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching LEI data: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def _parse_lei_records(self, api_response: Dict) -> List[Dict]:
        """
        Parse the JSON-API response from GLEIF API into a simplified format.

        Args:
            api_response: The raw JSON response from the GLEIF API

        Returns:
            A list of dictionaries with simplified LEI information
        """
        results = []

        # Handle both single record and list responses
        data = api_response.get('data', [])
        if isinstance(data, dict):
            data = [data]

        for record in data:
            try:
                attributes = record.get('attributes', {})
                entity = attributes.get('entity', {})
                legal_name = entity.get('legalName', {})
                legal_address = entity.get('legalAddress', {})
                registration = attributes.get('registration', {})

                parsed_record = {
                    'lei': attributes.get('lei', ''),
                    'legal_name': legal_name.get('name', ''),
                    'status': entity.get('status', ''),
                    'country': legal_address.get('country', ''),
                    'city': legal_address.get('city', ''),
                    'address': self._format_address(legal_address),
                    'postal_code': legal_address.get('postalCode', ''),
                    'registration_date': registration.get('initialRegistrationDate', ''),
                    'last_update': registration.get('lastUpdateDate', ''),
                    'entity_category': entity.get('category', ''),
                    'legal_jurisdiction': entity.get('jurisdiction', '')
                }

                results.append(parsed_record)

            except Exception as e:
                print(f"Warning: Error parsing record: {e}")
                continue

        return results

    def _format_address(self, address: Dict) -> str:
        """
        Format an address dictionary into a single string.

        Args:
            address: Address dictionary from GLEIF API

        Returns:
            Formatted address string
        """
        parts = []

        # Address lines
        for line in address.get('addressLines', []):
            if line:
                parts.append(line)

        # Add additional address components
        for field in ['city', 'region', 'postalCode', 'country']:
            value = address.get(field, '')
            if value:
                parts.append(value)

        return ', '.join(parts) if parts else ''


# Backward compatibility - keep the original class name
GLEIFService = GLEIFClient


# Convenience functions for simple use cases
def get_lei(company_name: str, country: Optional[str] = None) -> Optional[str]:
    """
    Simple function to get the LEI code for a company name.

    Returns the first matching LEI code, or None if no matches found.

    Args:
        company_name: The name of the company
        country: Optional country code to filter results (e.g., 'US', 'GB')

    Returns:
        The LEI code as a string, or None if not found
    """
    try:
        client = GLEIFClient()
        results = client.get_lei_by_company_name(
            company_name,
            page_size=5,
            filter_by_country=country
        )

        if results:
            return results[0]['lei']
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def get_lei_details(company_name: str, country: Optional[str] = None) -> List[Dict]:
    """
    Get detailed LEI information for a company name.

    Returns all matching records with full details.

    Args:
        company_name: The name of the company
        country: Optional country code to filter results (e.g., 'US', 'GB')

    Returns:
        List of dictionaries with LEI details
    """
    try:
        client = GLEIFClient()
        return client.get_lei_by_company_name(
            company_name,
            filter_by_country=country
        )
    except Exception as e:
        print(f"Error: {e}")
        return []
