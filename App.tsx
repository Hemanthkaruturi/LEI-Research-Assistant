import React, { useState, useCallback } from 'react';
import type { LEIData } from './types';
import SearchForm from './components/SearchForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import InfoMessage from './components/InfoMessage';
import { searchCompanyByName } from './services/gleifService';
import { getLegalNameAndSources } from './services/geminiService';

// Helper to normalize company names for better matching
const normalizeName = (name: string): string => {
  return name
    .toLowerCase()
    // Expanded list of common suffixes
    .replace(/\b(inc|llc|ltd|corp|corporation|gmbh|ag|sarl|l\.l\.c|l\.t\.d)\.?\b/g, '')
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '') // remove punctuation
    .replace(/\s+/g, ' ') // normalize whitespace
    .trim();
};

const App: React.FC = () => {
  const [companyName, setCompanyName] = useState('');
  const [website, setWebsite] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<LEIData | null>(null);
  const [infoMessage, setInfoMessage] = useState<string | null>(null);

  const handleSearch = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);
    setInfoMessage(null);

    try {
      if (!companyName || !website) {
        throw new Error("Company name and website are required.");
      }
      
      // Step 1: Search GLEIF for potential matches
      const gleifRecords = await searchCompanyByName(companyName);
      if (!gleifRecords || gleifRecords.length === 0) {
        // This is not an error, but a valid result: No LEI found.
        setInfoMessage(`No LEI record found for "${companyName}". This often means the entity does not have one.`);
        return; // Gracefully exit the search process
      }

      // Step 2: Use Gemini to find the legal name from the website and get cost
      const { legalName: geminiLegalName, sources, cost } = await getLegalNameAndSources(website);
      const normalizedGeminiName = normalizeName(geminiLegalName);

      // Step 3: Find the best match from GLEIF results using a more flexible check
      const foundRecord = gleifRecords.find(record => {
        const gleifLegalName = record.attributes.entity.legalName.name;
        const normalizedGleifName = normalizeName(gleifLegalName);
        // Use `includes` for a more flexible match instead of strict equality
        return normalizedGleifName.includes(normalizedGeminiName) || normalizedGeminiName.includes(normalizedGleifName);
      });

      if (!foundRecord) {
        throw new Error(`Could not verify the legal entity for ${website}. Gemini suggested "${geminiLegalName}", which did not match any LEI records found for "${companyName}".`);
      }

      // Step 4: Format and set the final result
      const { entity, lei } = foundRecord.attributes;
      const addressParts = [
        ...entity.legalAddress.addressLines,
        entity.legalAddress.city,
        entity.legalAddress.region,
        entity.legalAddress.postalCode,
        entity.legalAddress.country,
      ].filter(Boolean); // Filter out empty parts

      setResult({
        lei,
        legalName: entity.legalName.name,
        address: addressParts.join(', '),
        sources,
        cost,
      });

    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred.");
      }
    } finally {
      setIsLoading(false);
    }
  }, [companyName, website]);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8 font-sans">
      <div className="w-full max-w-2xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-800 dark:text-slate-100">
            LEI Research Assistant
          </h1>
          <p className="mt-2 text-md text-slate-600 dark:text-slate-400">
            Verify a company's Legal Entity Identifier using its name and website.
          </p>
        </header>

        <main className="bg-white dark:bg-slate-800/50 shadow-xl rounded-2xl p-6 sm:p-8 border border-slate-200 dark:border-slate-700">
          <SearchForm
            companyName={companyName}
            setCompanyName={setCompanyName}
            website={website}
            setWebsite={setWebsite}
            onSubmit={handleSearch}
            isLoading={isLoading}
          />
        </main>

        <div className="mt-8 w-full">
            {isLoading && <LoadingSpinner />}
            {error && <ErrorMessage message={error} />}
            {infoMessage && <InfoMessage message={infoMessage} />}
            {result && <ResultsDisplay data={result} />}
        </div>
      </div>
    </div>
  );
};

export default App;