import React from 'react';
import { InfoIcon } from './icons/IconComponents';

interface InfoMessageProps {
  message: string;
}

const InfoMessage: React.FC<InfoMessageProps> = ({ message }) => {
  if (!message) return null;

  return (
    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-500/30 text-blue-700 dark:text-blue-300 px-4 py-3 rounded-lg relative flex items-start space-x-3 animate-fade-in">
      <InfoIcon className="h-5 w-5 mt-0.5 flex-shrink-0" />
      <div>
        <strong className="font-semibold">Information</strong>
        <span className="block sm:inline ml-1">{message}</span>
      </div>
    </div>
  );
};

export default InfoMessage;
