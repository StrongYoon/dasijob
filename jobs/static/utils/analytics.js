// 데이터 포맷팅 유틸리티
export const formatNumber = (number) => {
  return new Intl.NumberFormat('ko-KR').format(number);
};

// 날짜 포맷팅 유틸리티
export const formatDate = (date) => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(new Date(date));
};

// 차트 데이터 처리 유틸리티
export const processChartData = (data, type) => {
  switch (type) {
    case 'trend':
      return data.map(item => ({
        date: formatDate(item.date),
        value: item.count
      }));

    case 'category':
      return Object.entries(data).map(([category, count]) => ({
        name: category,
        value: count
      }));

    case 'location':
      return Object.entries(data).map(([location, stats]) => ({
        location,
        jobs: stats.jobs,
        applications: stats.applications
      }));

    default:
      return data;
  }
};

// 분석 데이터 집계 유틸리티
export const aggregateAnalytics = (data) => {
  return {
    totalJobs: data.reduce((sum, item) => sum + item.job_count, 0),
    totalApplications: data.reduce((sum, item) => sum + item.application_count, 0),
    averageApplicationsPerJob: (
      data.reduce((sum, item) => sum + item.average_applications_per_job, 0) / data.length
    ).toFixed(2)
  };
};