def send_application_update(user_id, data):
    """
    지원서 상태 업데이트 알림을 보내는 함수

    Args:
        user_id (int): 사용자 ID
        data (dict): 알림에 포함될 데이터
    """
    try:
        from jobs.models import Notification

        Notification.objects.create(
            user_id=user_id,
            notification_type='application',
            title=f'지원 상태 업데이트: {data.get("job_title")}',
            message=f'지원하신 채용공고의 상태가 "{data.get("status")}"로 변경되었습니다.',
            link=f'/applications/{data.get("application_id")}/'
        )
    except Exception as e:
        print(f"알림 전송 중 오류 발생: {str(e)}")