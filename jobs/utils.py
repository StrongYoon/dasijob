# jobs/utils.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_job_update(user_id, data):
    """채용 정보 업데이트를 WebSocket을 통해 전송"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}_updates",
        {
            "type": "job_update",
            "data": data
        }
    )

def send_application_update(user_id, data):
    """지원 현황 업데이트를 WebSocket을 통해 전송"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}_updates",
        {
            "type": "application_update",
            "data": data
        }
    )
