import React from 'react';

type PageContainerProps = {
  children: React.ReactNode;
  className?: string;
};

/**
 * Container component for page content with consistent padding and max-width
 */
export default function PageContainer({ children, className = '' }: PageContainerProps) {
  return (
    <main className={`flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 ${className}`}>
      {children}
    </main>
  );
}
