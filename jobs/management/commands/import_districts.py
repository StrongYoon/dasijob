import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from jobs.models import Region


class Command(BaseCommand):
    help = '시군구 데이터를 가져옵니다'

    def handle(self, *args, **options):
        self.stdout.write('시군구 데이터 가져오기 시작...')

        # API 엔드포인트 수정
        url = 'http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList'

        # 시도 목록 가져오기
        regions = Region.objects.filter(level=1)

        for region in regions:
            self.stdout.write(f"{region.name} 시군구 데이터 가져오기 시작...")

            # 파라미터 수정
            params = {
                'serviceKey': settings.ADMINISTRATIVE_DISTRICT_API_KEY,
                'pageNo': '1',
                'numOfRows': '100',
                'type': 'xml',  # json 대신 xml로 변경
                'locatadd_nm': region.code
            }

            try:
                response = requests.get(url, params=params)
                self.stdout.write(f"API 응답 상태 코드: {response.status_code}")
                self.stdout.write(f"API 응답 헤더: {response.headers}")
                self.stdout.write(f"API 응답 내용: {response.text[:500]}")  # 처음 500자만 출력

                # 여기서 잠시 멈추고 응답을 확인해보겠습니다
                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f'API 호출 실패: {response.status_code}'))
                    continue

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'에러 발생 ({region.name}): {str(e)}')
                )
                continue

        self.stdout.write(self.style.SUCCESS('시군구 데이터 가져오기 완료!'))