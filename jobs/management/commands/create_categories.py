from django.core.management.base import BaseCommand

from jobs.models import JobCategory, SubCategory


class Command(BaseCommand):
    help = '시니어 친화 직군 카테고리 생성'

    def handle(self, *args, **kwargs):
        if JobCategory.objects.exists():
            if input('기존 카테고리가 존재합니다. 모두 삭제하고 새로 생성하시겠습니까? (y/n): ').lower() != 'y':
                self.stdout.write(self.style.WARNING('작업이 취소되었습니다.'))
                return
            JobCategory.objects.all().delete()

        # 1. 사무/관리
        office = JobCategory.objects.create(
            name="사무/관리",
            description="오랜 경험을 활용할 수 있는 사무/관리직",
            icon="briefcase"
        )
        SubCategory.objects.create(category=office, name="일반 사무", description="문서 작성, 데이터 관리 등의 일반 사무직")
        SubCategory.objects.create(category=office, name="행정 보조", description="행정 업무 보조 및 사무 지원")
        SubCategory.objects.create(category=office, name="문서 관리", description="서류 정리 및 문서 관리")
        SubCategory.objects.create(category=office, name="데이터 입력", description="전산 데이터 입력 및 관리")

        # 2. 서비스/돌봄
        service = JobCategory.objects.create(
            name="서비스/돌봄",
            description="따뜻한 마음으로 함께하는 서비스 직군",
            icon="heart"
        )
        SubCategory.objects.create(category=service, name="요양보호", description="요양원, 재가요양 등 요양보호 서비스")
        SubCategory.objects.create(category=service, name="아동 돌봄", description="어린이집, 유치원 도우미")
        SubCategory.objects.create(category=service, name="생활 도우미", description="가사 도우미, 주거 관리 서비스")
        SubCategory.objects.create(category=service, name="반려동물 케어", description="반려동물 돌봄 서비스")

        # 3. 교육/강사
        education = JobCategory.objects.create(
            name="교육/강사",
            description="풍부한 경험을 나누는 교육 직군",
            icon="book"
        )
        SubCategory.objects.create(category=education, name="방과후 교사", description="초/중/고 방과후 교실 지도")
        SubCategory.objects.create(category=education, name="특기적성 강사", description="예체능, 취미 관련 교육")
        SubCategory.objects.create(category=education, name="전통문화 교육", description="전통예절, 문화 교육")
        SubCategory.objects.create(category=education, name="생활체육 강사", description="요가, 게이트볼 등 생활체육 지도")

        # 4. 시설/경비
        facility = JobCategory.objects.create(
            name="시설/경비",
            description="안전하고 믿음직한 시설 관리 직군",
            icon="shield"
        )
        SubCategory.objects.create(category=facility, name="아파트 경비", description="주거단지 경비 및 관리")
        SubCategory.objects.create(category=facility, name="주차 관리", description="주차장 관리 및 정리")
        SubCategory.objects.create(category=facility, name="시설 관리", description="건물 관리 및 유지보수")
        SubCategory.objects.create(category=facility, name="안전 관리", description="시설물 안전 관리 및 점검")

        # 5. 판매/영업
        sales = JobCategory.objects.create(
            name="판매/영업",
            description="풍부한 대화와 경험을 살리는 판매 직군",
            icon="shop"
        )
        SubCategory.objects.create(category=sales, name="매장 관리", description="상품 진열 및 매장 관리")
        SubCategory.objects.create(category=sales, name="판매 도우미", description="상품 안내 및 판매")
        SubCategory.objects.create(category=sales, name="전화 상담", description="고객 상담 및 텔레마케팅")
        SubCategory.objects.create(category=sales, name="중개 도우미", description="부동산, 중고차 등 중개 보조")

        # 6. 제조/생산
        manufacturing = JobCategory.objects.create(
            name="제조/생산",
            description="꼼꼼함과 정확성을 살리는 제조 직군",
            icon="tool"
        )
        SubCategory.objects.create(category=manufacturing, name="품질 검수", description="제품 품질 관리 및 검사")
        SubCategory.objects.create(category=manufacturing, name="포장·조립", description="상품 포장 및 간단한 조립")
        SubCategory.objects.create(category=manufacturing, name="식품 가공", description="식품 제조 및 가공")
        SubCategory.objects.create(category=manufacturing, name="수공예", description="전통 공예 및 수작업")

        # 7. 운송/배달
        delivery = JobCategory.objects.create(
            name="운송/배달",
            description="안전하고 정확한 운송 직군",
            icon="truck"
        )
        SubCategory.objects.create(category=delivery, name="납품 기사", description="상품 운송 및 납품")
        SubCategory.objects.create(category=delivery, name="퀵서비스", description="서류 및 소화물 배달")
        SubCategory.objects.create(category=delivery, name="배달 도우미", description="음식 및 물품 배달")
        SubCategory.objects.create(category=delivery, name="운전 기사", description="승합차량 및 통근 운전")

        # 8. 전문직
        professional = JobCategory.objects.create(
            name="전문직",
            description="전문성과 경험을 활용하는 직군",
            icon="star"
        )
        SubCategory.objects.create(category=professional, name="상담사", description="심리, 진로, 취업 상담")
        SubCategory.objects.create(category=professional, name="번역·통역", description="외국어 번역 및 통역")
        SubCategory.objects.create(category=professional, name="자문위원", description="경영, 기술 자문")
        SubCategory.objects.create(category=professional, name="기술 지도사", description="기술 및 기능 지도")

        self.stdout.write(self.style.SUCCESS('카테고리 생성이 완료되었습니다!'))