"""화면 1 — 설정 화면(엑셀 선택/템플릿/저장 경로/확장자/QR 파라미터)."""
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import converter
import excel_template

EXT_ITEMS = ("PNG", "JPG")
EXT_MAP = {"PNG": ".png", "JPG": ".jpg"}


class SetupFrame(ttk.Frame):
    def __init__(self, master, on_run, on_close):
        super().__init__(master, padding=16)
        self.on_run = on_run
        self.on_close = on_close

        self.excel_var = tk.StringVar()
        self.dir_var = tk.StringVar()
        self.ext_var = tk.StringVar(value="PNG")
        self.box_var = tk.StringVar(value="50")
        self.border_var = tk.StringVar(value="1")

        self._build()

    def _build(self) -> None:
        self.columnconfigure(1, weight=1)

        title = ttk.Label(self, text="LSE QR Converter", font=("", 14, "bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

        # 엑셀 파일
        ttk.Label(self, text="엑셀 파일:").grid(row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.excel_var).grid(
            row=1, column=1, sticky="we", padx=6
        )
        ttk.Button(self, text="찾아보기", command=self._browse_excel).grid(
            row=1, column=2, sticky="e"
        )
        ttk.Button(self, text="엑셀 템플릿 다운로드", command=self._download_template).grid(
            row=2, column=1, sticky="w", padx=6, pady=(6, 0)
        )
        notice = tk.Label(
            self,
            text="※ 유의사항: QR Code 이름 중복이 없도록 주의!",
            fg="#d0342c",
            anchor="w",
        )
        notice.grid(row=3, column=0, columnspan=3, sticky="w", pady=(6, 14))

        # QR 저장 경로
        ttk.Label(self, text="QR 저장 경로:").grid(row=4, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.dir_var).grid(
            row=4, column=1, sticky="we", padx=6
        )
        ttk.Button(self, text="폴더 선택", command=self._browse_dir).grid(
            row=4, column=2, sticky="e"
        )

        # 저장 확장자
        ttk.Label(self, text="저장 확장자:").grid(row=5, column=0, sticky="w", pady=(14, 0))
        ext_combo = ttk.Combobox(
            self,
            textvariable=self.ext_var,
            values=EXT_ITEMS,
            state="readonly",
            width=8,
        )
        ext_combo.grid(row=5, column=1, sticky="w", padx=6, pady=(14, 0))

        # QR 속성 (box_size / border) — 구분된 영역, 항목별 한 줄 + 기본값 표기
        qr_frame = ttk.LabelFrame(self, text="QR 속성", padding=(12, 8))
        qr_frame.grid(row=6, column=0, columnspan=3, sticky="we", pady=(14, 0))

        ttk.Label(qr_frame, text="QR 크기(box_size):").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            qr_frame, from_=1, to=50, textvariable=self.box_var, width=5
        ).grid(row=0, column=1, sticky="w", padx=8)
        ttk.Label(qr_frame, text="(기본값 50, 입력 범위 1~50)", foreground="#777777").grid(
            row=0, column=2, sticky="w"
        )

        ttk.Label(qr_frame, text="테두리(border):").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        ttk.Spinbox(
            qr_frame, from_=0, to=20, textvariable=self.border_var, width=5
        ).grid(row=1, column=1, sticky="w", padx=8, pady=(8, 0))
        ttk.Label(qr_frame, text="(기본값 1, 입력 범위 0~20)", foreground="#777777").grid(
            row=1, column=2, sticky="w", pady=(8, 0)
        )

        # 실행 / 닫기
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=7, column=0, columnspan=3, sticky="se", pady=(30, 0))
        self.rowconfigure(7, weight=1)
        ttk.Button(btn_frame, text="실행", width=10, command=self._run_clicked).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(btn_frame, text="닫기", width=10, command=self.on_close).pack(side="left")

    # --- 버튼 핸들러 ---------------------------------------------------
    def _browse_excel(self) -> None:
        path = filedialog.askopenfilename(
            title="엑셀 파일 선택",
            filetypes=[("Excel 파일", "*.xlsx"), ("모든 파일", "*.*")],
        )
        if path:
            self.excel_var.set(path)

    def _browse_dir(self) -> None:
        path = filedialog.askdirectory(title="QR 코드 저장 폴더 선택")
        if path:
            self.dir_var.set(path)

    def _download_template(self) -> None:
        path = filedialog.asksaveasfilename(
            title="엑셀 템플릿 저장",
            defaultextension=".xlsx",
            initialfile=excel_template.DEFAULT_FILENAME,
            filetypes=[("Excel 파일", "*.xlsx")],
        )
        if not path:
            return
        try:
            excel_template.create_template(path)
            messagebox.showinfo("완료", f"템플릿이 저장되었습니다.\n{path}")
        except Exception as e:
            messagebox.showerror("오류", f"템플릿 저장에 실패했습니다.\n{e}")

    def _run_clicked(self) -> None:
        excel_path = self.excel_var.get().strip()
        out_dir = self.dir_var.get().strip()

        if not excel_path:
            messagebox.showwarning("확인", "엑셀 파일을 선택해 주세요.")
            return
        if not Path(excel_path).is_file():
            messagebox.showwarning("확인", "선택한 엑셀 파일을 찾을 수 없습니다.")
            return
        if not out_dir:
            messagebox.showwarning("확인", "QR 코드 저장 폴더를 선택해 주세요.")
            return
        if not Path(out_dir).is_dir():
            messagebox.showwarning("확인", "QR 코드 저장 폴더가 존재하지 않습니다.")
            return

        # 저장 폴더 쓰기 권한 검증
        try:
            probe = Path(out_dir) / ".qr_write_test.tmp"
            with open(probe, "w") as f:
                f.write("")
            os.remove(probe)
        except OSError as e:
            messagebox.showerror("오류", f"저장 폴더에 쓸 수 없습니다.\n{e}")
            return

        # QR 파라미터 검증
        try:
            box_size = int(self.box_var.get())
            border = int(self.border_var.get())
            if box_size < 1 or border < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "확인",
                "QR 크기(box_size)는 1 이상, 테두리(border)는 0 이상의 정수여야 합니다.",
            )
            return

        # 엑셀 파싱 및 건수 확인 (작업 시작 전에 총 건수 확정)
        try:
            rows = converter.read_rows(excel_path)
        except Exception as e:
            messagebox.showerror("오류", f"엑셀 파일을 읽을 수 없습니다.\n{e}")
            return
        if not rows:
            messagebox.showwarning("확인", "엑셀에 변환할 데이터가 없습니다.")
            return

        self.on_run(
            {
                "rows": rows,
                "out_dir": Path(out_dir),
                "ext": EXT_MAP[self.ext_var.get()],
                "box_size": box_size,
                "border": border,
            }
        )
