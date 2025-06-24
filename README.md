# insightweekly-back

DB (MySQL)
account
- account_id : int
- email : text (로그인에 사용)
- username : text
- password : text (로그인에 사용용)
- interest_category : text

news
- news_id : int
- title : text
- summary : text
- category :text
- publication_date : date
- collact_date : date
- author : text
- news_company : text
- link : text

scrap
- scrap_id : int
- account_id : int
- news_id : int
- active : boolean
- scrap_date : date

view (로그인 하지 않은 사용자는 user_id를 null 값으로 저장)
- view_id : int
- view_time : date
- user_id : int
- news_id : int

+ category = ["IT_과학", "건강", "경제", "교육", "국제", "라이프스타일", "문화", "사건사고", "사회일반", "산업", "스포츠", "여성복지", "여행레저", "연예", "정치", "지역", "취미", "기타"]



API

Account
- POST | /account/login -> token 발행
- POST | /account/logout
- POST | /account/signup

News
- GET | /news?page=<num>

Search
- GET | /search?keyword=<string>&page=<num>

Scrap (로그인 되어있는 상황에만 가능)
- PUT | /scrap?news=<news_id> | token으로 user_id 확인

Analysis (DB 스키마 변경 제안 포함)
- GET | /api/analysis
  - Description: 요약 통계 및 주간 인기 뉴스 데이터를 제공합니다.
  - Response Body:
    ```json
    {
      "summary": {
        "today_collected_news_count": 150,
        "today_views_count": 3450,
        "today_scraps_count": 35
      },
      "weekly_view_trend": [
        { "date": "2023-10-27", "views": 920 },
        { "date": "2023-10-26", "views": 810 },
        { "date": "2023-10-25", "views": 700 }
      ],
      "weekly_scrap_trend": [
        { "date": "2023-10-27", "scraps": 35 },
        { "date": "2023-10-26", "scraps": 40 },
        { "date": "2023-10-25", "scraps": 25 }
      ],
      "weekly_top10_news": [
        { "news_id": 101, "title": "뉴스 제목 1", "category": "IT/과학", "view_count": 1200 },
        { "news_id": 205, "title": "뉴스 제목 2", "category": "경제", "view_count": 1150 }
      ],
      "weekly_top10_news_by_category": {
        "IT/과학": [
          { "news_id": 101, "title": "뉴스 제목 1", "view_count": 1200 }
        ],
        "경제": [
          { "news_id": 205, "title": "뉴스 제목 2", "view_count": 1150 }
        ]
      }
    }
    ```