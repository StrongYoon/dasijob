import React, {useState} from 'react';
import {Alert, AlertDescription, AlertTitle} from '@/components/ui/alert';

const ErrorBoundary = ({ children }) => {
  const [error, setError] = useState(null);

  const handleError = (error) => {
    setError(error);
    // 에러 로깅 서비스로 전송
    logErrorToService(error);
  };

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTitle>오류가 발생했습니다</AlertTitle>
        <AlertDescription>
          <p>{error.message}</p>
          <button
            onClick={() => setError(null)}
            className="mt-2 px-4 py-2 bg-red-100 text-red-800 rounded-lg hover:bg-red-200"
          >
            다시 시도
          </button>
        </AlertDescription>
      </Alert>
    );
  }

  return children;
};

// Loading 상태 관리를 위한 컴포넌트
export const LoadingState = ({ isLoading, error, children }) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2">로딩중...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTitle>데이터를 불러오는 중 오류가 발생했습니다</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return children;
};

export default ErrorBoundary;