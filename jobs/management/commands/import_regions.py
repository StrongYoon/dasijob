import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from jobs.models import Region


class Command(BaseCommand):
    help = '행정구역 데이터를 가져옵니다'

    def handle(self, *args, **options):
        base_url = 'https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList'
        params = {
            'serviceKey': settings.ADMINISTRATIVE_DISTRICT_API_KEY,
            'pageNo': '1',
            'numOfRows': '100',
            'type': 'json,
        }

        try:
            # 시도 데이터 가져오기
            params['locatadd_nm'] = ''  # 빈 값으로 시도 데이터 조회
            response = requests.get(base_url, params=params)
            data = response.json()

            if 'StanReginCd' in data:
                items = data['StanReginCd'][1]['row']

                for item in items:
                    # 시도 레벨 데이터 생성
                    region, created = Region.objects.get_or_create(
                        code=item['region_cd'],
                        defaults={
                            'name': item['region_nm'],
                            'level': 1
                        }
                    )

                    if created:
                        self.stdout.write(f"시도 추가: {region.name}")

                    # 해당 시도의 시군구 데이터 가져오기
                    params['locatadd_nm'] = item['region_cd']
                    sub_response = requests.get(base_url, params=params)
                    sub_data = sub_response.json()

                    if 'StanReginCd' in sub_data:
                        sub_items = sub_data['StanReginCd'][1]['row']

                        for sub_item in sub_items:
                            # 시군구 레벨 데이터 생성
                            sub_region, sub_created = Region.objects.get_or_create(
                                code=sub_item['region_cd'],
                                defaults={
                                    'name': sub_item['region_nm'],
                                    'level': 2,
                                    'parent': region
                                }
                            )

                            if sub_created:
                                self.stdout.write(f"시군구 추가: {sub_region.name}")

            self.stdout.write(self.style.SUCCESS('행정구역 데이터 가져오기 완료!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'에러 발생: {str(e)}'))