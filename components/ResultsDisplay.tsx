
import React from 'react';
import type { LEIData } from '../types';
import { BuildingIcon, LinkIcon } from './icons/IconComponents';

interface ResultsDisplayProps {
  data: LEIData;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ data }) => {
  return (
    <div className="bg-white dark:bg-slate-800 shadow-lg rounded-xl p-6 border border-slate-200 dark:border-slate-700 w-full animate-fade-in">
      <div className="mb-6">
        <h2 className="text-sm font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider">Legal Entity Identifier (LEI)</h2>
        <p className="font-mono text-xl sm:text-2xl text-slate-800 dark:text-slate-100 bg-slate-100 dark:bg-slate-700 rounded-md p-3 mt-1 text-center select-all">
          {data.lei}
        </p>
      </div>
      
      <div className="space-y-4">
        <div>
          <h3 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Verified Legal Name</h3>
          <p className="text-lg font-medium text-slate-900 dark:text-slate-50">{data.legalName}</p>
        </div>
        <div>
          <h3 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Legal Address</h3>
          <div className="flex items-start mt-1 text-slate-600 dark:text-slate-300">
            <BuildingIcon className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0 text-slate-400 dark:text-slate-500" />
            <p>{data.address}</p>
          </div>
        </div>
      </div>

      {data.sources && data.sources.length > 0 && (
        <div className="mt-6 pt-6 border-t border-slate-200 dark:border-slate-700">
            <h3 className="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">Verification Sources</h3>
            <ul className="space-y-2">
                {data.sources.map((source, index) => (
                    <li key={index}>
                        <a
                            href={source.web.uri}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 group"
                        >
                           <LinkIcon className="h-4 w-4 mr-2 flex-shrink-0 text-slate-400 group-hover:text-blue-500" />
                           <span className="truncate group-hover:underline" title={source.web.title}>{source.web.title}</span>
                        </a>
                    </li>
                ))}
            </ul>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
