# 🥗 몸소 Backend

> 몸을 소중히 — 식사 기록과 칼로리 분석 서비스의 백엔드 API 서버입니다.

---

## 🛠 Tech Stack

| 항목         | 기술           |
| ------------ | -------------- |
| Language     | Python         |
| Framework    | FastAPI        |
| ORM          | SQLAlchemy     |
| Auth         | JWT            |
| DB Migration | Alembic (예정) |
| Cache        | Redis (예정)   |

---

## 📁 주요 기능

### ✅ Ver 0 (완료)

**인증 / 사용자**

- 회원가입 API
- 로그인 API (JWT 인증 방식)
- 현재 로그인 사용자 조회 API (`GET /me`)
- 사용자 비밀번호 해싱 적용
- 사용자 모델 / 스키마 정의
- `get_current_user` 의존성 적용
- SQLAlchemy ORM 모델 정의

**식사 기록**

- 이미지 업로드 API
- 식사 기록 생성 API
- 식사 기록 조회 API
- 음식 영양 정보 조회 API

**통계**

- 일일 섭취 칼로리 통계 API
- 일일 탄수화물 / 단백질 / 지방 통계 API

> 🔲 로그아웃 처리 방식 정리 (진행 중)

---

### 🚀 Ver 1 (예정)

- 서비스 출시
- 특정 기간 통계 API
- 특정 기간 목표 설정 API
- 목표와 실제 섭취량 비교 기능
- Alembic을 통한 DB 스키마 변경 이력 및 마이그레이션 관리
- Redis 캐시 활용 검토

---

### 🤖 Ver 2 (예정)

- 비전 AI 학습 (음식 이미지 인식)
- DB 비동기 처리

---

## 📡 API 목록

| Method | Endpoint       | 설명                    | 인증 |
| ------ | -------------- | ----------------------- | ---- |
| POST   | `/auth/signup` | 회원가입                | ❌   |
| POST   | `/auth/login`  | 로그인 (JWT 발급)       | ❌   |
| GET    | `/me`          | 현재 로그인 사용자 조회 | ✅   |
| POST   | `/meals`       | 식사 기록 생성          | ✅   |
| GET    | `/meals`       | 식사 기록 조회          | ✅   |
| POST   | `/upload`      | 이미지 업로드           | ✅   |
| GET    | `/nutrition`   | 음식 영양 정보 조회     | ✅   |

---

## ⚙️ 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

---

## 🔐 인증 방식

JWT Bearer Token 방식을 사용합니다.

```
Authorization: Bearer <access_token>
```

로그인 후 발급된 토큰을 모든 인증 필요 API의 헤더에 포함해 주세요.

---
