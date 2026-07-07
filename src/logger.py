"""화면 + 파일 동시 기록용 로그 파일 관리.

log 폴더는 exe(또는 프로젝트 루트)와 같은 레벨에 자동 생성되고,
파일명은 timestamp(YYYYMMDD_HHMMSS.log)로 만든다.
로그는 발생 즉시 flush하여 중간에 취소되어도 내용이 보존된다.
"""
from datetime import datetime
from pathlib import Path


class JobLogger:
    def __init__(self, base_dir: Path):
        self.path: Path | None = None
        self.error: str | None = None
        self._fh = None
        try:
            log_dir = base_dir / "log"
            log_dir.mkdir(parents=True, exist_ok=True)
            self.path = log_dir / (datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
            self._fh = open(self.path, "a", encoding="utf-8")
        except OSError as e:
            self.error = str(e)
            self.path = None
            self._fh = None

    def write(self, line: str) -> None:
        if self._fh is None:
            return
        try:
            self._fh.write(line + "\n")
            self._fh.flush()
        except OSError:
            pass

    def close(self) -> None:
        if self._fh is not None:
            try:
                self._fh.close()
            except OSError:
                pass
            self._fh = None
