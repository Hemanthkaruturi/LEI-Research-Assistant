
import React from 'react';
import { SearchIcon } from './icons/IconComponents';

interface SearchFormProps {
  companyName: string;
  setCompanyName: (name: string) => void;
  website: string;
  setWebsite: (website: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

const SearchForm: React.FC<SearchFormProps> = ({
  companyName,
  setCompanyName,
  website,
  setWebsite,
  onSubmit,
  isLoading,
}) => {
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <div>
        <label htmlFor="companyName" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
          Company Name
        </label>
        <div className="mt-1">
          <input
            type="text"
            name="companyName"
            id="companyName"
            className="block w-full rounded-md border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            placeholder="e.g., Google"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            required
          />
        </div>
      </div>

      <div>
        <label htmlFor="website" className="block text-sm font-medium text-slate-700 dark:text-slate-300">
          Company Website or Domain
        </label>
        <div className="mt-1">
          <input
            type="text"
            name="website"
            id="website"
            className="block w-full rounded-md border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            placeholder="e.g., google.com or alphabet.com"
            value={website}
            onChange={(e) => setWebsite(e.target.value)}
            required
          />
        </div>
        <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
          Providing an accurate website is crucial for verifying the correct legal entity.
        </p>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="inline-flex w-full items-center justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-slate-400 disabled:cursor-not-allowed dark:focus:ring-offset-slate-900"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Researching...
          </>
        ) : (
          <>
            <SearchIcon className="-ml-1 mr-2 h-5 w-5" />
            Research
          </>
        )}
      </button>
    </form>
  );
};

export default SearchForm;
