
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from pypdf import PdfReader, PdfWriter


class PDFConcatenator(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("PDF Concatenator")
        self.geometry("600x500")
        self.resizable(True, True)
        self.pdf_list: list[str] = []  # ordered list of file paths

        self._build_ui()

    def _build_ui(self):
        # file list + scrollbar
        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = tk.Listbox(
            list_frame, selectmode=tk.SINGLE, font=("TkDefaultFont", 10)
        )
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(btn_frame, text="Add PDFs…", command=self._add_pdfs).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="Remove", command=self._remove_selected).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="↑ Up", command=self._move_up).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="↓ Down", command=self._move_down).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="Clear All", command=self._clear_all).pack(
            side=tk.LEFT, padx=2
        )

        # merge button + status
        merge_frame = tk.Frame(self)
        merge_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            merge_frame,
            text="Merge & Save As…",
            command=self._merge,
            bg="#4CAF50",
            fg="white",
            font=("TkDefaultFont", 11, "bold"),
        ).pack(side=tk.LEFT, padx=2)

        self.status = tk.Label(merge_frame, text="Ready", anchor=tk.W)
        self.status.pack(side=tk.RIGHT, padx=4)

    # helpers
    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for path in self.pdf_list:
            self.listbox.insert(tk.END, Path(path).name)

    def _selected_index(self) -> int | None:
        sel = self.listbox.curselection()
        return sel[0] if sel else None

    # actions
    def _add_pdfs(self):
        paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if not paths:
            return
        for p in paths:
            self.pdf_list.append(p)
        self._refresh_listbox()
        self.status.config(text=f"{len(self.pdf_list)} PDF(s) loaded")

    def _remove_selected(self):
        idx = self._selected_index()
        if idx is None:
            return
        self.pdf_list.pop(idx)
        self._refresh_listbox()
        self.status.config(text="Removed")

    def _move_up(self):
        idx = self._selected_index()
        if idx is None or idx == 0:
            return
        self.pdf_list[idx], self.pdf_list[idx - 1] = self.pdf_list[idx - 1], self.pdf_list[idx]
        self._refresh_listbox()
        self.listbox.selection_set(idx - 1)

    def _move_down(self):
        idx = self._selected_index()
        if idx is None or idx >= len(self.pdf_list) - 1:
            return
        self.pdf_list[idx], self.pdf_list[idx + 1] = self.pdf_list[idx + 1], self.pdf_list[idx]
        self._refresh_listbox()
        self.listbox.selection_set(idx + 1)

    def _clear_all(self):
        self.pdf_list.clear()
        self._refresh_listbox()
        self.status.config(text="Cleared")

    def _merge(self):
        if not self.pdf_list:
            messagebox.showwarning("No PDFs", "Add at least one PDF to merge.")
            return

        output_path = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="merged.pdf",
        )
        if not output_path:
            return

        self.status.config(text="Merging…")
        self.update()

        try:
            writer = PdfWriter()
            for path in self.pdf_list:
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)

            with open(output_path, "wb") as out:
                writer.write(out)

            total_pages = sum(len(PdfReader(p).pages) for p in self.pdf_list)
            self.status.config(text=f"Done — {total_pages} page(s) saved")
            messagebox.showinfo(
                "Success",
                f"Merged {len(self.pdf_list)} file(s), {total_pages} page(s).\n\n{output_path}",
            )
        except Exception as exc:
            self.status.config(text="Error")
            messagebox.showerror("Error", f"Failed to merge:\n{exc}")


def main():
    app = PDFConcatenator()
    app.mainloop()


if __name__ == "__main__":
    main()
