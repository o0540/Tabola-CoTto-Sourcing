import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup

today_str = datetime.now().strftime("%m/%d")

# 1. 로그인 필요 없는 '오픈마켓(지마켓)' 실시간 크롤링 엔진
def get_real_item(keyword, item_name, spec):
    url = f"https://browse.gmarket.co.kr/search?keyword={keyword}"
    # 파이썬이 아니라 '진짜 사람'이 접속하는 것처럼 위장하는 신분증
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 검색 결과 중 첫 번째(가장 상단) 상품 찾기
        item = soup.select_one('.box__item-container')
        if not item:
            return None
            
        # 진짜 링크와 가격 추출
        link = item.select_one('.box__item-title a')['href']
        price_text = item.select_one('.box__price-seller strong').text.replace(',', '')
        price = int(price_text)
        
        return {
            "name": item_name,
            "spec": spec,
            "price": price,
            "source": "오픈마켓(실시간)",
            "link": link,  # <--- 진짜 클릭 되는 구매 페이지 주소!
            "note": f"★실시간 실측 성공 ({today_str})★"
        }
    except Exception as e:
        print(f"크롤링 에러: {e}")
        return None

# 2. 5대 품목 실제 데이터 수집 명령
data = []

# 주인님의 핵심 품목들을 차례대로 검색해서 살아있는 링크를 가져옵니다
items_to_search = [
    ("못난이 감자 10kg", "감자(못난이)", "10kg"),
    ("못난이 양파 10kg", "양파(못난이)", "10kg"),
    ("못난이 당근 10kg", "당근(못난이)", "10kg"),
    ("생바질 1kg", "바질", "1kg"),
    ("백오이 50개", "백오이", "50개")
]

for search_keyword, name, spec in items_to_search:
    result = get_real_item(search_keyword, name, spec)
    if result:
        data.append(result)

# 3. JSON 변환 및 G메일 발송 (이전과 동일)
json_data = json.dumps(data, ensure_ascii=False, indent=2)

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

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print("✅ [실전 크롤링] 접속 가능한 진짜 링크 발송 완료!")
except Exception as e:
    print(f"❌ 메일 발송 실패: {e}")
