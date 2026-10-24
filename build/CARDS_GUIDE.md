# 카드 작성 규칙 (보면서 배우는 pandas)

- 파일: build/cards/NNN_<id>.py  (NNN = 장번호*100 + 순서). 형식은 000_type01.py, 101_read_csv.py, 402_map_dict.py 를 따른다.
- 실행: `python build/build.py <id> <id> ...` → build/_preview/<id>.json (카드별), site/assets/img/<id>.png
- 원본 카드 내용: (원본 카드는 이전 판 HTML 참고). 명령어(cmd)·엑셀 대응·설명의 뼈대는 원본을 살리고, 예시를 가게 데이터로 바꾼다.
- 데이터: build/snippets.py 의 KOI / KOI_KIND / CVS / SHOP / FX 문자열을 그대로 코드에 붙인다(카드마다 스스로 실행 가능). 카드에 맞게 더 작은 표를 새로 만들어도 되지만 가게 세계관(카페 Koi · 동네 편의점 · 의류 쇼핑몰 · 환율)을 지킨다. 회계 용어(차변, 대변, 계정, 전표, 거래처 미수금, 공시, DART, 급여, 이사회, 세율, PPE, 감가상각, 차입금)는 쓰지 않는다.
- 차트 라벨·범례·열 이름·값은 영어(Colab 한글 깨짐 방지). 설명(desc)·caption·talk 는 한국어. 문체는 원본처럼 "~다." 평서문.
- 코드는 Colab 새 셀에 붙여 넣으면 파일 없이 돌아가야 한다. 주석은 한국어로 짧게.
- stages(ns, out): 원본처럼 2~4단계. 표 값은 ns 의 실제 DataFrame 에서 T() 로 만들고 숫자를 손으로 적지 않는다. 차트 단계는 CH(type=...) 스펙(원본 spec 필드 참고) 또는 IMG(id).
- caption 의 숫자도 실제 실행 결과와 같아야 한다(f-string 으로 ns 에서 꺼내 쓴다).
- tip: 내 파일로 할 때의 한 줄(선택). "수업 파일", "키트", "주차", "슬라이드", "P-xx" 같은 다른 자료 언급 금지.
- talk(선택, 최대 2줄, 한 줄 60자 이하): 장의 첫 카드 = 세라 질문 + 박사 답. 함정 카드(공백, NaN, 평균 vs 합계, 빈 표 등) = 한 줄. 다른 카드는 비운다.
  who: doc(박사, 해요체 설명) · asst(세라, "왜요?", 판정 안 함) · fly(초파리, 반말 짧은 의심 질문) · robo(Money-Robo, 반말 "삐빅", state= idle|thinking|wrong|confused|success, 투자 이야기 금지)
  talk 속 숫자는 실행 결과 숫자만.
