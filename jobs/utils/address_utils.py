import requests
from django.conf import settings

def get_administrative_districts():
    url = "https://api.vworld.kr/req/data"
    params = {
        "service": "data",
        "request": "GetFeature",
        "data": "LT_C_ADSIDO_INFO",
        "key": settings.VWORLD_API_KEY,
        "format": "json"  # 응답 형식을 명시적으로 지정
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        return response.json()
    except requests.RequestException as e:
        print(f"API 요청 중 에러 발생: {e}")
        return None