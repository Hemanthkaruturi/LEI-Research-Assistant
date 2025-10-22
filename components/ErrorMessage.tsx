
import React from 'react';
import { WarningIcon } from './icons/IconComponents';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  if (!message) return null;

  return (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-500/30 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg relative flex items-start space-x-3">
      <WarningIcon className="h-5 w-5 mt-0.5 flex-shrink-0" />
      <div>
        <strong className="font-semibold">Error</strong>
        <span className="block sm:inline ml-1">{message}</span>
      </div>
    </div>
  );
};

export default ErrorMessage;
