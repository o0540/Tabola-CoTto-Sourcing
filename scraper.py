import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# ==========================================
# 1. 데이터 수집 단계 (향후 크롤링 라이브러리 추가 적용)
# ==========================================
today_str = datetime.now().strftime("%m/%d")

# 5대 핵심 품목 데이터 (실전 적용 시 크롤링된 변수값으로 치환됩니다)
data = [
  {
    "name": "양파(못난이)",
    "spec": "10kg",
    "price": 9300,
    "source": "못난이마켓",
    "link": "https://m.auction.co.kr/Shop/uglymarket/Products/onion10kg",
    "note": f"TCSE 파이썬 엔진 자동수집 ({today_str})"
  },
  {
    "name": "감자(못난이)",
    "spec": "10kg",
    "price": 10500,
    "source": "오더히어로",
    "link": "https://orderhero.co.kr/market/potato/ugly_10kg",
    "note": "AI 스마트소싱 모니터링"
  },
  {
    "name": "당근(못난이)",
    "spec": "10kg",
    "price": 13500,
    "source": "비굿",
    "link": "https://begood.co.kr/shop/carrot/ugly_10kg",
    "note": "AI 스마트소싱 모니터링"
  },
  {
    "name": "바질",
    "spec": "1kg",
    "price": 22000,
    "source": "프레시웰",
    "link": "https://freshwell.co.kr/goods/basil_1kg",
    "note": "AI 스마트소싱 모니터링"
  },
  {
    "name": "백오이",
    "spec": "50개",
    "price": 18000,
    "source": "예스어스",
    "link": "https://yesus.co.kr/product/cucumber_white_50ea",
    "note": "AI 스마트소싱 모니터링"
  }
]

# JSON 형태로 빳빳하게 변환
json_data = json.dumps(data, ensure_ascii=False, indent=2)

# ==========================================
# 2. 이메일 자동 발송 단계 (구글 앱스 스크립트 트리거용)
# ==========================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# GitHub Secrets 기능을 사용해 아이디와 비밀번호를 안전하게 숨깁니다.
SENDER_EMAIL = os.environ.get("GMAIL_USER") 
SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") 
RECEIVER_EMAIL = SENDER_EMAIL

msg = MIMEMultipart()
msg['Subject'] = '오늘의 식자재 리포트'
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL

# JSON 데이터를 메일 본문에 삽입
msg.attach(MIMEText(json_data, 'plain', 'utf-8'))

# 메일 서버 접속 및 발송
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("✅ [T-Cotto Sourcing Engine] 리포트 발송 완료! 구글 시트 트리거가 곧 작동합니다.")
except Exception as e:
    print(f"❌ 발송 실패: {e}")
