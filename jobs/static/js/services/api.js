class APIService {
  async request(url, options = {}) {
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value,
      },
    };

    try {
      const response = await fetch(url, { ...defaultOptions, ...options });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || '요청 처리 중 오류가 발생했습니다.');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // 이력서 관련 API
  async getResume(id) {
    return this.request(`/api/resumes/${id}/`);
  }

  async saveResume(id, data) {
    return this.request(`/api/resumes/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // 분석 데이터 관련 API
  async getAnalytics() {
    return this.request('/api/analytics/dashboard_stats/');
  }
}

export const apiService = new APIService();