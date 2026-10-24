# 보면서 배우는 pandas

**카페·편의점·쇼핑몰 장부로 보는 명령어 72장**

카페 Koi · 동네 편의점 · 의류 쇼핑몰의 장부로 pandas 명령어 72개를 **표가 움직이는 그림**으로 보는 한 페이지 책입니다.
명령어마다 동작 그림, Colab에 그대로 붙여 넣는 코드, 실제 실행 결과가 함께 있습니다.

- 0장 한눈에 보는 groupby · 1장 불러오기와 살펴보기 · 2장 청소하기 · 3장 고르고 거르기 · 4장 새 열 만들기
- 5장 합치고 모양 바꾸기 · 6장 묶어서 집계하기 · 7장 numpy 계산 · 8장 차트 그리기 · 9장 저장하기
- 카드마다 주소가 있습니다: `.../#merge`, `.../#yf_download`

## GitHub Pages 로 열기
1. 이 폴더 내용을 repo 맨 위에 올립니다 (`index.html` 이 루트에 있어야 합니다).
2. Settings → Pages → Source: *Deploy from a branch*, Branch: `main` / `(root)` → Save.
3. 1~2분 뒤 `https://<계정>.github.io/<repo>/` 에서 열립니다.

## 캐릭터 그림
`assets/chars/` 에 PNG 를 넣으면 말풍선 옆에 자동으로 나타납니다. 파일 이름은 그 폴더의 README 를 보세요. 그림이 없어도 글자 배지로 완성된 페이지입니다.

## 고치고 다시 만들기
카드 하나는 `build/cards/NNN_<id>.py` 파일 하나입니다(설명, 코드, 동작 그림 단계, 대사).
```bash
pip install -r build/requirements.txt
python build/build.py            # 모든 카드 실행 → index.html, assets/img/*.png 다시 생성
python build/build.py merge      # 카드 하나만 시험 (build/_preview/merge.json)
```
코드를 실제로 실행해 출력과 그림을 만들기 때문에, 페이지의 숫자는 항상 코드 결과와 같습니다.
pandas 2.2 기준(Colab 과 같은 출력)입니다. 예제 속 가게, 환율, 숫자는 모두 연습용으로 지어낸 값입니다.

---
제작 안상선 (Ahn, Sang-Sun) · sangsun.ahn@gmail.com · © 2026 All rights reserved.
Money-Robo는 저자 서비스의 마스코트이며, 극 중 대사는 비유일 뿐 투자 권유가 아닙니다.
