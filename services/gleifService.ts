import type { GleifApiResponse, GleifRecord } from '../types';

const API_BASE_URL = 'https://api.gleif.org/api/v1';

export const searchCompanyByName = async (companyName: string): Promise<GleifRecord[]> => {
  // Use the documented `filter[fulltext]` parameter to avoid 400 Bad Request errors.
  // This provides a stable full-text search across relevant entity fields.
  const url = `${API_BASE_URL}/lei-records?filter[fulltext]=${encodeURIComponent(companyName)}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Accept': 'application/vnd.api+json',
      },
    });

    if (!response.ok) {
      throw new Error(`GLEIF API request failed with status ${response.status}`);
    }

    const data: GleifApiResponse = await response.json();
    return data.data;
  } catch (error) {
    console.error("Error fetching from GLEIF API:", error);
    throw new Error("Failed to fetch data from the GLEIF directory.");
  }
};
