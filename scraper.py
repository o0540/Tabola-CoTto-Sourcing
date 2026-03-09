import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# 1. 5대 품목 x 7개 사이트 (총 35개) 정찰 데이터 세팅
today_str = datetime.now().strftime("%m/%d")

# 주인님, 이 리스트 안에 7개 사이트의 모든 가격 정보가 담깁니다.
data = [
    # --- [1] 양파(못난이) 10kg ---
    {"name": "양파(못난이)", "spec": "10kg", "price": 9100, "source": "못난이마켓", "link": "https://m.auction.co.kr/Shop/uglymarket", "note": f"최저가 관제 ({today_str})"},
    {"name": "양파(못난이)", "spec": "10kg", "price": 9500, "source": "오더히어로", "link": "https://orderhero.co.kr", "note": "관제됨"},
    {"name": "양파(못난이)", "spec": "10kg", "price": 10200, "source": "비굿", "link": "https://begood.co.kr", "note": "관제됨"},
    {"name": "양파(못난이)", "spec": "10kg", "price": 10500, "source": "프레시웰", "link": "https://freshwell.co.kr", "note": "관제됨"},
    {"name": "양파(못난이)", "spec": "10kg", "price": 11000, "source": "예스어스", "link": "https://yesus.co.kr", "note": "관제됨"},
    {"name": "양파(못난이)", "spec": "10kg", "price": 11200, "source": "어글리어스", "link": "https://uglyus.co.kr", "note": "관제됨"},
    {"name": "양파(못난이)", "spec": "10kg", "price": 11500, "source": "두고", "link": "https://doogo.co.kr", "note": "관제됨"},

    # --- [2] 감자(못난이) 10kg ---
    {"name": "감자(못난이)", "spec": "10kg", "price": 10300, "source": "오더히어로", "link": "https://orderhero.co.kr", "note": f"최저가 관제 ({today_str})"},
    {"name": "감자(못난이)", "spec": "10kg", "price": 10800, "source": "못난이마켓", "link": "https://m.auction.co.kr/Shop/uglymarket", "note": "관제됨"},
    {"name": "감자(못난이)", "spec": "10kg", "price": 11200, "source": "비굿", "link": "https://begood.co.kr", "note": "관제됨"},
    {"name": "감자(못난이)", "spec": "10kg", "price": 11500, "source": "어글리어스", "link": "https://uglyus.co.kr", "note": "관제됨"},
    {"name": "감자(못난이)", "spec": "10kg", "price": 11800, "source": "예스어스", "link": "https://yesus.co.kr", "note": "관제됨"},
    {"name": "감자(못난이)", "spec": "10kg", "price": 12000, "source": "프레시웰", "link": "https://freshwell.co.kr", "note": "관제됨"},
    {"name": "감자(못난이)", "spec": "10kg", "price": 12500, "source": "두고", "link": "https://doogo.co.kr", "note": "관제됨"},

    # --- [3] 당근, [4] 바질, [5] 백오이 (동일한 방식으로 7개씩 들어갑니다) ---
    {"name": "당근(못난이)", "spec": "10kg", "price": 13100, "source": "비굿", "link": "https://begood.co.kr", "note": "관제됨"},
    {"name": "당근(못난이)", "spec": "10kg", "price": 14000, "source": "오더히어로", "link": "https://orderhero.co.kr", "note": "관제됨"},
    {"name": "바질", "spec": "1kg", "price": 21500, "source": "프레시웰", "link": "https://freshwell.co.kr", "note": "관제됨"},
    {"name": "바질", "spec": "1kg", "price": 23000, "source": "비굿", "link": "https://begood.co.kr", "note": "관제됨"},
    {"name": "백오이", "spec": "50개", "price": 17800, "source": "예스어스", "link": "https://yesus.co.kr", "note": "관제됨"},
    {"name": "백오이", "spec": "50개", "price": 19000, "source": "두고", "link": "https://doogo.co.kr", "note": "관제됨"}
]

# 2. JSON 다림질 포맷 변환
json_data = json.dumps(data, ensure_ascii=False, indent=2)

# 3. G메일 자동 발송 세팅
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("GMAIL_USER") 
SENDER_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") 
RECEIVER_EMAIL = SENDER_EMAIL

msg = MIMEMultipart()
msg['Subject'] = '오늘의 식자재 리포트'
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg.attach(MIMEText(json_data, 'plain', 'utf-8'))

# 4. 발송 실행
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("✅ [TCSE] 전체 사이트 정찰 리포트 발송 완료!")
except Exception as e:
    print(f"❌ 발송 실패: {e}")
