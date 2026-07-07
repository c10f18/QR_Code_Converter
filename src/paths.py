"""실행 환경(exe / 스크립트)에 따른 기준 경로 판별."""
import sys
from pathlib import Path


def app_base_dir() -> Path:
    """log 폴더 등을 만들 기준 디렉터리.

    PyInstaller onefile로 빌드된 경우 exe 파일이 있는 폴더,
    스크립트 실행 시에는 프로젝트 루트(src의 상위)를 반환한다.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
