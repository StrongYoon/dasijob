const ResumeEditor = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const loadResume = async (id) => {
    setIsLoading(true);
    setError(null);
    try {
      const resumeData = await apiService.getResume(id);
      setData(resumeData);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ErrorBoundary>
      <LoadingState isLoading={isLoading} error={error}>
        {data && (
          // 이력서 편집 UI
        )}
      </LoadingState>
    </ErrorBoundary>
  );
};