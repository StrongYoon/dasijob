import pandas as pd
from django.core.management.base import BaseCommand

from jobs.models import Region


class Command(BaseCommand):
    help = '행정동/법정동 데이터를 가져옵니다'

    def handle(self, *args, **options):
        self.stdout.write('지역 데이터 가져오기 시작...')

        try:
            # CSV 파일 읽기
            df = pd.read_csv('data/administrative_districts.csv', encoding='utf-8')

            processed = {
                'sido': 0,  # 시도 카운트
                'sgg': 0,  # 시군구 카운트
                'dong': 0  # 동리 카운트
            }

            # 시도 처리
            sido_df = df[['행정동코드', '시도명']].drop_duplicates()
            for _, row in sido_df.iterrows():
                code = str(row['행정동코드'])[:2]
                name = row['시도명']
                if name and not name.isspace():  # 빈 값이 아닌 경우만
                    region, created = Region.objects.get_or_create(
                        code=code,
                        defaults={
                            'name': name,
                            'level': 1
                        }
                    )
                    if created:
                        processed['sido'] += 1
                        self.stdout.write(f"시도 추가: {name}")

            # 시군구 처리
            sgg_df = df[['행정동코드', '시도명', '시군구명']].dropna(subset=['시군구명']).drop_duplicates()
            for _, row in sgg_df.iterrows():
                sido_code = str(row['행정동코드'])[:2]
                sgg_code = str(row['행정동코드'])[:5]
                sgg_name = row['시군구명']

                if sgg_name and not sgg_name.isspace():  # 빈 값이 아닌 경우만
                    try:
                        sido = Region.objects.get(code=sido_code)
                        sgg, created = Region.objects.get_or_create(
                            code=sgg_code,
                            defaults={
                                'name': sgg_name,
                                'level': 2,
                                'parent': sido
                            }
                        )
                        if created:
                            processed['sgg'] += 1
                            self.stdout.write(f"시군구 추가: {sido.name} - {sgg_name}")
                    except Region.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"상위 시도를 찾을 수 없음: {row['시도명']}"))

            # 동리 처리
            dong_df = df[['행정동코드', '시도명', '시군구명', '동리명']].dropna(subset=['동리명']).drop_duplicates()
            for _, row in dong_df.iterrows():
                sgg_code = str(row['행정동코드'])[:5]
                dong_code = str(row['행정동코드'])
                dong_name = row['동리명']

                if dong_name and not dong_name.isspace():  # 빈 값이 아닌 경우만
                    try:
                        sgg = Region.objects.get(code=sgg_code)
                        dong, created = Region.objects.get_or_create(
                            code=dong_code,
                            defaults={
                                'name': dong_name,
                                'level': 3,
                                'parent': sgg
                            }
                        )
                        if created:
                            processed['dong'] += 1
                            self.stdout.write(f"동리 추가: {sgg.parent.name} {sgg.name} - {dong_name}")
                    except Region.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"상위 시군구를 찾을 수 없음: {row['시군구명']}"))

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n데이터 가져오기 완료!\n'
                    f'추가된 시도: {processed["sido"]}개\n'
                    f'추가된 시군구: {processed["sgg"]}개\n'
                    f'추가된 동리: {processed["dong"]}개'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'처리 중 에러 발생: {str(e)}'))