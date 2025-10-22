# LEI Research Assistant

A Python-based web application to find and verify Legal Entity Identifiers (LEI) for companies using GLEIF data and AI-powered verification.

## Features

- **LEI Lookup**: Search for Legal Entity Identifiers by company name
- **AI Verification**: Uses Google Gemini to verify legal names from company websites
- **Flexible Matching**: Advanced name normalization and matching algorithm
- **Source Attribution**: Displays verification sources with citations
- **Cost Tracking**: Shows estimated API costs for transparency

## Architecture

This application uses a clean separation between backend logic and frontend presentation:

### Backend (`/backend`)
- **`services/gleif_service.py`**: GLEIF API integration for LEI data retrieval
- **`services/gemini_service.py`**: Google Gemini API integration for name verification
- **`lei_lookup.py`**: Main orchestrator with business logic for the 4-step verification process

### Frontend
- **`app.py`**: Streamlit web application providing the user interface

## How It Works

The application uses a 4-step verification process:

1. **GLEIF Search**: Searches the Global Legal Entity Identifier Foundation database for company name matches
2. **Website Verification**: Uses Google Gemini with Google Search grounding to verify the legal name from the company's website
3. **Name Matching**: Applies flexible name normalization and matching to find the correct LEI record
4. **Result Formatting**: Returns verified LEI information with full address and source citations

## Prerequisites

- **Python**: 3.8 or higher
- **Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/apikey)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd LEI-Research-Assistant
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Run Locally

1. **Activate your virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to `http://localhost:8501`

4. **Search for a company**:
   - Enter the company name (e.g., "Google")
   - Enter the company's website (e.g., "google.com")
   - Click "Search LEI"

### Example Searches

- **Company**: Google | **Website**: google.com
- **Company**: Apple Inc | **Website**: apple.com
- **Company**: Microsoft | **Website**: microsoft.com

## API Integrations

### GLEIF API
- **URL**: https://api.gleif.org/api/v1/lei-records
- **Purpose**: Retrieve LEI records for companies
- **Authentication**: None required (public API)

### Google Generative AI (Gemini)
- **Model**: gemini-2.5-flash
- **Purpose**: Verify legal company names from websites
- **Authentication**: API key required
- **Features**: Google Search grounding for accurate verification

## Cost Estimates

The application displays estimated API costs based on Gemini 2.5 Flash pricing:
- Input: $0.35 per 1M characters
- Output: $1.05 per 1M characters

Typical cost per lookup: $0.000001 - $0.00001 USD

## Development

### Project Structure

```
LEI-Research-Assistant/
├── app.py                          # Streamlit frontend
├── backend/
│   ├── __init__.py
│   ├── lei_lookup.py               # Main orchestrator
│   └── services/
│       ├── __init__.py
│       ├── gleif_service.py        # GLEIF API client
│       └── gemini_service.py       # Gemini API client
├── requirements.txt                # Python dependencies
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=backend
```

## Troubleshooting

### API Key Issues
- Ensure your `.env` file exists and contains `GEMINI_API_KEY=your_key`
- Restart the Streamlit app after setting the API key
- Verify your API key is valid at [Google AI Studio](https://aistudio.google.com/apikey)

### No LEI Found
- Some companies may not have registered LEIs
- Try variations of the company name
- Ensure the website URL is accurate

### Name Mismatch
- The legal name from the website must match the GLEIF record
- Try using the exact legal name (e.g., "Google LLC" instead of "Google")
- Verify the website belongs to the correct entity

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data from [GLEIF](https://www.gleif.org/) (Global Legal Entity Identifier Foundation)
- Powered by [Google Gemini](https://ai.google.dev/)
- Built with [Streamlit](https://streamlit.io/)
