"""화면 2 — 진행 화면(Progress bar / n/m / 로그 / 요약 / 닫기·완료 버튼)."""
import queue
import tkinter as tk
from tkinter import messagebox, ttk

from converter import ConvertWorker
from logger import JobLogger
from paths import app_base_dir

POLL_INTERVAL_MS = 100


class ProgressFrame(ttk.Frame):
    def __init__(self, master, config: dict):
        super().__init__(master, padding=16)
        self.master = master
        self.conv_config = config
        self.total = len(config["rows"])
        self.events: queue.Queue = queue.Queue()
        self.worker: ConvertWorker | None = None
        self.done = False
        self.cancel_requested = False

        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ttk.Label(self, text="변환 진행", font=("", 14, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )

        self.progressbar = ttk.Progressbar(self, maximum=self.total, value=0)
        self.progressbar.grid(row=1, column=0, sticky="we", pady=(0, 10))
        self.count_label = ttk.Label(self, text=f"0 / {self.total}")
        self.count_label.grid(row=1, column=1, sticky="e", padx=(10, 0), pady=(0, 10))

        log_frame = ttk.Frame(self)
        log_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, state="disabled", wrap="none", height=14)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scroll_y = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scroll_y.set)

        self.summary_label = ttk.Label(self, text="", font=("", 10, "bold"))
        self.summary_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.logpath_label = ttk.Label(self, text="")
        self.logpath_label.grid(row=4, column=0, columnspan=2, sticky="w")

        self.close_btn = ttk.Button(self, text="닫기", width=10, command=self.on_close_clicked)
        self.close_btn.grid(row=5, column=0, columnspan=2, sticky="e", pady=(12, 0))

    # --- 작업 시작/이벤트 처리 ------------------------------------------
    def start(self) -> None:
        logger = JobLogger(app_base_dir())
        if logger.error:
            messagebox.showwarning(
                "로그",
                "log 폴더를 만들 수 없어 화면 로그만 기록합니다.\n" + logger.error,
            )
        self.worker = ConvertWorker(
            rows=self.conv_config["rows"],
            out_dir=self.conv_config["out_dir"],
            ext=self.conv_config["ext"],
            box_size=self.conv_config["box_size"],
            border=self.conv_config["border"],
            events=self.events,
            logger=logger,
        )
        self.worker.start()
        self.after(POLL_INTERVAL_MS, self._poll_events)

    def _poll_events(self) -> None:
        while True:
            try:
                event = self.events.get_nowait()
            except queue.Empty:
                break
            kind = event[0]
            if kind == "log":
                self._append_log(event[1])
            elif kind == "progress":
                n = event[1]
                self.progressbar["value"] = n
                self.count_label.config(text=f"{n} / {self.total}")
            elif kind == "done":
                self._on_done(event[1])
        if not self.done:
            self.after(POLL_INTERVAL_MS, self._poll_events)

    def _append_log(self, line: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", line + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _on_done(self, stats: dict) -> None:
        self.done = True
        if stats["cancelled"]:
            summary = (
                f"취소됨: {stats['total']}개 중 {stats['success']}개 성공 "
                f"(실패 {stats['fail']}개, 나머지 미처리)"
            )
        else:
            summary = (
                f"완료: {stats['total']}개 중 {stats['success']}개 성공 "
                f"(실패 {stats['fail']}개)"
            )
        self.summary_label.config(text=summary)
        if stats["log_path"] is not None:
            self.logpath_label.config(text=f"로그 저장 위치: {stats['log_path']}")
        else:
            self.logpath_label.config(text="로그 파일 저장 실패 (화면 로그만 기록됨)")
        self.close_btn.config(text="완료", state="normal")

        if self.cancel_requested:
            self.master.destroy()

    # --- 닫기/완료 버튼 --------------------------------------------------
    def on_close_clicked(self) -> None:
        if self.done:
            self.master.destroy()
            return
        # 팝업이 떠 있는 동안 작업이 멈춰 있어야 하므로 먼저 일시정지
        self.worker.pause()
        answer = messagebox.askyesno("작업 취소", "정말 작업을 취소하시겠습니까?")
        if answer:
            self.cancel_requested = True
            self.close_btn.config(state="disabled")
            self.worker.cancel()  # 워커가 로그를 마무리하면 done 이벤트에서 종료
        else:
            self.worker.resume()
