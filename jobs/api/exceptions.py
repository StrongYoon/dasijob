class ResumeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이력서 처리 중 오류가 발생했습니다.'
    default_code = 'resume_error'

class AnalyticsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '데이터 분석 중 오류가 발생했습니다.'
    default_code = 'analytics_error'