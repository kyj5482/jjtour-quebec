# JJ Tour · 2026 퀘벡 · 몬트리올 가족여행

우리 가족 4명이 추수감사절 연휴(2026년 11월 25일 – 29일)에 다녀오는 퀘벡시티 2박 · 몬트리올 1박 일정표입니다. UI/UX는 `../jjtour`(2027 미국 서부 가족여행)와 같습니다.

- 11/25 수 저녁 SNA 출발(밤 비행기) → 11/26 목 아침 퀘벡 도착 → 11/27 금 몽모랑시 폭포 · 오를레앙섬 · 시타델 → 11/28 토 12:32 VIA 레일로 몬트리올, AURA → 11/29 일 13:10 몬트리올 출발, SNA 도착
- 탭: 가족 일정, Jia · Jaei 모험(아이용 미션 · 프랑스어 배지), 여행 경비 시뮬레이션(USD, CAD 환율), 준비물 · 연락처, 현지인 꿀팁, 여행 프랑스어 롤플레이(fr-CA 음성)
- 오른쪽 위 **한국어 / English** 버튼으로 페이지 전체(일정·지도·경비·준비물·꿀팁·롤플레이·인트로 영상)를 바꿉니다. `?lang=en`으로 영어 화면을 바로 열 수 있고, 고른 언어는 기기에 기억됩니다.
- 프랑스어 문장마다 발음을 달았습니다: 한국어 화면은 한글 발음, 영어 화면은 영어식 발음(bohn-ZHOOR). ▶ 버튼은 브라우저의 퀘벡 프랑스어(fr-CA) 음성으로 읽어 줍니다.
- 페이지: https://kyj5482.github.io/jjtour-quebec/ (`index.html`, GitHub Pages)

## 다시 빌드하기

```bash
python3 src/build.py
```

`src/template.html`에 `src/geo.js`와 데이터 파일(`days.js`·`days_en.js`, `meals.js`, `tips.js`·`tips_en.js`, `french.js`)을 합쳐 `index.html`을 만듭니다. 화면 글자는 `L(한국어, English)`로 두 언어를 함께 적습니다.
인트로 영상은 `src/intro_music.py`·`src/intro_film.py`(어른용), `src/intro_music_kids.py`·`src/intro_film_kids.py`(아이용, 글꼴 `src/Jua-Regular.ttf`)로 만들었습니다 (numpy, Pillow, imageio-ffmpeg 필요).

```bash
python3 src/intro_music.py music.wav 69 && python3 src/intro_film.py img intro.mp4 music.wav
python3 src/intro_music_kids.py music_kids.wav 62 && python3 src/intro_film_kids.py img intro_kids.mp4 music_kids.wav src/Jua-Regular.ttf
python3 src/intro_film_en.py img intro_en.mp4 music.wav && python3 src/intro_film_kids_en.py img intro_kids_en.mp4 music_kids.wav src/Jua-Regular.ttf
```

## 자료 출처 (2026-10-18 확인)

- 항공: Google 항공권 (아메리칸 19:39 SNA → PHX → PHL → YQB 10:24, 에어캐나다·유나이티드 13:10 YUL → ORD → SNA 19:01)
- 기차: VIA 레일 예약 화면 (11/28 37번 열차 퀘벡 12:32 → 몬트리올 15:54, 이코노미 CAD $54부터)
- 호텔: Booking.com (해당 날짜, 4인 1실) · 렌터카: KAYAK
- 입장료·운영 시간: 시타델, 몽모랑시 폭포(Sépaq), 노트르담 대성당(AURA), 문명 박물관 공식 페이지 · 크리스마스 마켓: 퀘벡시 관광청
- 지도: Natural Earth, OpenStreetMap 기여자(ODbL) — `geo.js`는 두 자료를 투영·단순화한 결과
- 사진: Wikimedia Commons, 저작자와 라이선스는 `credits.json`과 페이지 하단에 있습니다.
