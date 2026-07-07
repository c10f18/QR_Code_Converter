"""LSE QR Converter 엔트리포인트 — 창 생성 및 화면 전환."""
import tkinter as tk

from ui_progress_frame import ProgressFrame
from ui_setup_frame import SetupFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LSE QR Converter")
        self.geometry("560x520")
        self.minsize(560, 520)

        self.setup_frame = SetupFrame(self, on_run=self._start_conversion, on_close=self.destroy)
        self.setup_frame.pack(fill="both", expand=True)

    def _start_conversion(self, config: dict) -> None:
        self.setup_frame.destroy()
        progress = ProgressFrame(self, config)
        progress.pack(fill="both", expand=True)
        # 창 X 버튼도 닫기 버튼과 동일하게 취소 확인을 거치도록 연결
        self.protocol("WM_DELETE_WINDOW", progress.on_close_clicked)
        progress.start()


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
