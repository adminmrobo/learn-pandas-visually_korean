# 캐릭터 · 대표 그림 넣는 곳

파일 이름만 맞춰 이 폴더(`assets/chars/`)에 넣으면 말풍선 · 식구 카드 · 표지에 자동으로 나타난다.
없는 표정은 대체 그림(ALIASES) → 글자 배지 순서로 보여 주므로, 몇 장만 있어도 페이지는 완성된 상태다.

## 지금 들어 있는 그림

| 파일 | 출처 | 상태 |
|---|---|---|
| doc_smile.png | AI_image_classification 의 박사 그림, 64×64 격자로 다시 찍은 512×512 초상 | 사용 중 |
| asst_smile.png | AI_image_classification 의 조수 그림, 같은 64×64 격자 초상 | 사용 중 |
| fly_point.png | AI_image_classification 의 초파리 그림, 같은 64×64 격자 초상 | 사용 중 |
| robo_idle / thinking / wrong / confused / success.png | 명세서 외형대로 코드로 찍은 임시 픽셀 그림, 같은 64×64 격자 초상 | 임시. 정식 그림으로 바꿔 넣으면 된다 |
| ../hero/hero.jpg | 코드로 그린 임시 대표 그림 (1200×800) | 임시. 정식 그림으로 바꿔 넣으면 된다 |

## 더 넣으면 쓰이는 그림 (명세서 §6)

| 캐릭터 | 파일 이름 (투명 배경 PNG, 정사각 512×512 권장) |
|---|---|
| 박사 | doc_smile · doc_explain(손바닥 펴서 설명) · doc_judge(지휘봉 들어 판정) · doc_think(턱 괴기) · doc_spark(손에 보랏빛 불꽃) |
| 세라 | asst_smile · asst_why(고개 갸웃) · asst_ledger(빈 서류철 펼침) · asst_sweat(땀방울) · asst_spark(반짝이) |
| 초파리 | fly_point · fly_doubt(한쪽 눈 가늘게) · fly_magnify(돋보기) · fly_arms(팔짱) · fly_coffee(커피) |
| Money-Robo | robo_idle · robo_thinking · robo_wrong · robo_confused · robo_success |

말풍선에 가장 자주 나오는 것은 `doc_explain`, `asst_why`, `fly_doubt` 다. 이 세 장을 먼저 만들면 효과가 크다.

## 이미지 생성 프롬프트 (이 시리즈: 동네 상가 2층 장부 상담소)

공통 (캐릭터)
```
16-bit RPG style pixel art, cute chibi proportions, bold dark outline, 2-3 tone shading,
transparent background, same character design as the reference image,
cozy evening ledger office above a neighborhood shopping street, warm amber desk-lamp light with deep navy shadows,
centered with small margin, eyes at 25-40% from the top, no text, no letters, no numbers, no logos.
```

| 캐릭터 | 외형 (고정) + 이 시리즈 소품 |
|---|---|
| 박사 | chibi scientist with round glasses, black hair with one white streak, white lab coat over a black vest and tie, big smile, **plain navy waistcoat over the lab coat, holding a blank wooden pointer stick** |
| 세라 | girl researcher with pink hair in two round buns and a navy streak, blue eyes, lavender hoodie under a white lab coat, jeans, **blank ID badge on a lanyard with no text, holding a plain closed ledger folder** |
| 초파리 | anthropomorphic fruit fly, black body, big red compound eyes, blue helmet with gold stripe and pink-blue cables, white lab coat, transparent wings, **holding a magnifying glass and a blank clipboard** |
| Money-Robo | round white robot, short antenna with a small yellow ball, black face screen with yellow eyes, small floating body with an oval shadow, **chest light that glows blue, yellow, red or green** |

표정 시트 (한 장에 5개)
```
[공통] + [외형 + 소품]
Character expression sheet, the same character shown 5 times in a single horizontal row,
same size, plain white background, at least 60px gap between figures:
(1) ... (2) ... (3) ... (4) ... (5) ...   3000 x 800 px.
```
- 박사: (1) big smile (2) open palm explaining (3) raising the pointer to give a verdict (4) hand on chin thinking (5) purple sparks from the hands, excited
- 세라: (1) gentle smile (2) head tilted, puzzled (3) opening the blank ledger folder, reporting (4) sweat drop, tired (5) sparkles, delighted
- 초파리: (1) pointing forward (2) one eye narrowed, doubtful (3) looking through the magnifying glass (4) arms crossed (5) holding a coffee cup, relaxed
- Money-Robo: (1) idle round yellow eyes, blue chest light (2) loading dots on the screen, yellow chest light (3) red X on the screen, red chest light (4) yellow scribble swirl and sweat drop, blinking yellow chest light (5) green check mark, sparkles, arms raised, green chest light

대표 그림 (hero.jpg, 1200×800)
- **쉽게 따라 해 보면서 배우는 파이썬**:
  `16-bit pixel art scene, 1200x800, cozy second-floor ledger office at 7pm, big window showing a neighborhood street with a cafe, a convenience store and a clothing shop glowing (icons only, no text), wooden desk piled with colorful ledgers and an open laptop, the scientist laughing, the pink-haired assistant opening a box of ledgers, the fruit fly researcher pointing at a ledger with a magnifying glass, the round white robot floating with a blue chest light, warm amber lamps, deep navy shadows, no text, no numbers, no logos`
- **보면서 배우는 pandas**:
  `16-bit pixel art scene, 1200x800, same ledger office at night, a large green chalkboard showing one colorful table splitting into three small tables and merging back into one (blocks and arrows only, no text, no numbers), the scientist pointing at the board with a pointer stick, the assistant watching wide-eyed, the fruit fly researcher checking a table with a magnifying glass, the round white robot with loading dots on its face screen, warm amber lamps, deep navy shadows, no text, no numbers, no logos`

네거티브
```
text, letters, numbers, words, signage, watermark, logo, realistic photo, 3D render, blurry,
extra fingers, distorted face, different character design, weapons, cigarettes, alcohol, blood,
real bank logos, real store brand logos, banknotes, ticker symbols, stock charts with numbers
```

## 해상도 · 구도 맞추기 (중요)
원본 그림마다 구도(전신 · 상반신)와 해상도가 달라서, 모든 초상을 **같은 픽셀 격자**로 다시 찍었다.
- 구도: 정사각형, 머리(머리카락 끝~턱)가 한 변의 약 60%, 머리 중심이 위에서 약 42%
- 해상도: **64×64 그림 픽셀**(머리 약 38칸)로 줄인 뒤 8배 키워 512×512. 색은 72색 이하
- 대표 그림: 배경과 같은 300×200 격자에 머리 약 37칸으로 얹은 뒤 4배(1200×800)
새 그림을 넣을 때도 이 규칙으로 맞추면 식구들의 픽셀 크기가 같아 보인다. 변환 스크립트는 `build/pixel_chars.py`, 원본 그림은 `build/chars_src/` 에 있다. 원본을 바꾸고 `python build/pixel_chars.py assets/chars` 를 실행하면 초상이 다시 만들어진다(머리 위치 숫자는 HEAD 에서 맞춘다).

## 구도 확인
- 너비 ≤ 높이 × 1.1, 눈이 위에서 25~40%, 투명 여백 4~8px
- 모든 장의 머리 크기 · 외곽선 · 팔레트가 같다
- 글자 · 숫자 · 로고 없음 (출입증 · 서류철 · 클립보드 · 칠판은 빈칸)
