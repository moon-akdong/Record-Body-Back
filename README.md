# Backend (FastAPI)

- Ver 0.
  - 로그인 (인증 API)
  - 이미지 업로드 API
  - 음식 이름&무게 업로드 API
  - 음식 영양 정보 조회 API
  - 일일 통계 API

- Ver 1.
  - 특정 기간 통계 API
  - 특정 기간 목표 설정 API
  - 목표와 비교 기능

- Ver 2.
  - DB : Alembic → 스키마 변경 이력/마이그레이션 관리 적용
  - DB : Await 비동기 처리
  -

## Ver 0.

- [x] 회원가입 API
- [x] 로그인 API
- [x] JWT 로그인 인증 방식
- [x] 현재 로그인 사용자 조회 API (`/me`)
- [x] SQLAlchemy ORM 모델 정의
- [ ] 로그아웃 처리 방식 정리
- [x] 사용자 비밀번호 해싱 적용
- [x] 사용자 모델 / 스키마 정의
- [x] 인증용 `get_current_user` 의존성 적용
- [x] 이미지 업로드 API
- [ ] 식사 기록 생성 API
- [ ] 식사 기록 조회 API
- [x] 음식 영양 정보 조회 API
- [ ] 일일 섭취 칼로리 통계 API
- [ ] 일일 탄수화물/단백질/지방 통계 API
