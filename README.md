# QR Converter

> 엑셀의 URL 목록을 한 번에 QR 코드 이미지로 변환하는 Windows 유틸리티

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-tkinter-green)
![Build](https://img.shields.io/badge/Build-PyInstaller-orange)

엑셀 파일 하나만 선택하면 수십·수백 개의 URL을 QR 코드 이미지(PNG/JPG)로 일괄 변환합니다.
설치 없이 실행되는 **단일 exe 파일**로 배포됩니다.

## 📦 다운로드

**[⬇️ 최신 버전 다운로드 (QR_Code_Converter.exe)](../../releases/latest)**

> 첫 실행 시 Windows SmartScreen 경고가 뜨면 **추가 정보 → 실행**을 눌러 주세요. (서명되지 않은 실행 파일의 일반적인 안내입니다)

---

## ✨ 주요 기능

- 📋 **엑셀 기반 일괄 변환** — `Source URL` / `QR Code Name` 두 컬럼만 채우면 끝
- 📥 **엑셀 템플릿 다운로드** — 프로그램에서 바로 양식 생성
- 📁 **저장 폴더 · 확장자 선택** — PNG(기본) / JPG
- 🎛️ **QR 속성 조절** — 크기(box_size 1\~50), 테두리(border 0\~20)
- 📊 **실시간 진행 표시** — Progress bar + `n / m` 카운터 + 상세 로그
- 📝 **로그 자동 저장** — exe 옆 `log/` 폴더에 timestamp 파일로 기록
- 🔒 **안전한 취소** — 작업 중 닫기 시 확인 팝업(팝업 중 작업 일시정지)
- 🔄 **파일명 중복 자동 처리** — `이름.png` → `이름(2).png` → `이름(3).png`

## 🚀 사용 방법

1. `QR__Code_Converter.exe` 실행
2. **엑셀 템플릿 다운로드**로 양식을 받아 URL과 이미지 이름 작성

   | Source URL | QR Code Name |
   |---|---|
   | https://example.com/event/1 | event_qr_01 |
   | https://example.com/event/2 | event_qr_02 |

3. 엑셀 파일 선택 → 저장 폴더 지정 → 확장자·QR 속성 확인 → **실행**
4. 변환 완료 후 요약(성공 건수, 로그 위치) 확인 → **완료**

> ⚠️ **QR Code Name이 중복되지 않도록 주의하세요.** 중복 시 `이름(2)`, `이름(3)` 형태로 자동 저장됩니다.

## 🛠️ 개발 및 빌드

```bash
# 의존성 설치
pip install -r requirements.txt

# 개발 실행
python src/main.py

# exe 빌드 (산출물: dist/QR__Code_Converter.exe)
build.bat
```

## 📂 프로젝트 구조

```
├── src/
│   ├── main.py              # 엔트리포인트, 화면 전환
│   ├── ui_setup_frame.py    # 설정 화면 (파일/폴더/확장자/QR 속성)
│   ├── ui_progress_frame.py # 진행 화면 (Progress bar/로그/요약)
│   ├── converter.py         # 엑셀 파싱 + QR 생성 워커 스레드
│   ├── excel_template.py    # 엑셀 템플릿 생성
│   ├── logger.py            # 로그 파일 관리
│   └── paths.py             # 실행 경로 판별
├── build.bat                # exe 빌드 스크립트
├── PLAN.md                  # 설계 문서
└── SUMMARY.md               # 구현 결과 요약
```

## 📄 로그 예시

```
[1] Start convert URL to QR Code - https://example.com/event/1 to event_qr_01
[1] Convert Success : event_qr_01.png
[2] Start convert URL to QR Code - https://example.com/event/2 to event_qr_02
[2] Convert Success : event_qr_02.png

총 2건 중 2건 성공, 0건 실패
```

## 🧰 기술 스택

| 역할 | 사용 기술 |
|---|---|
| 언어 / GUI | Python 3.11+ / tkinter |
| QR 생성 | [qrcode](https://pypi.org/project/qrcode/) + Pillow |
| 엑셀 처리 | openpyxl |
| exe 빌드 | PyInstaller (`--onefile --windowed`) |
