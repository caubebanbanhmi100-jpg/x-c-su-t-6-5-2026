import tkinter as tk
from tkinter import messagebox

class ProbSolverDetailed:
    def __init__(self, root):
        self.root = root
        self.root.title("Giải Xác Suất Chi Tiết")
        self.root.geometry("400x850")
        
        # Mã Unicode cho ký hiệu
        self.GIAO = u"\u2229"      
        self.HOP = u"\u222a"       
        self.DOI = u"\u0305"       
        
        self.entries = {}
        self.independent = tk.BooleanVar(value=False)
        self.setup_ui()

    def setup_ui(self):
        # 1. Checkbox độc lập
        f_top = tk.Frame(self.root, pady=5)
        f_top.pack()
        tk.Checkbutton(f_top, text=f"A, B độc lập (P(A{self.GIAO}B)=P(A)P(B))", 
                       variable=self.independent, fg="red").pack()

        # 2. Khung nhập liệu (Dùng Grid để thẳng hàng)
        f_in = tk.LabelFrame(self.root, text=" Nhập dữ liệu ", padx=10, pady=10)
        f_in.pack(fill="x", padx=10)

        fields = [
            ("P(A)", "A"), ("P(B)", "B"), 
            ("P(A|B)", "A_B"), ("P(B|A)", "B_A"),
            (f"P(A|B{self.DOI})", "A_dB"), (f"P(B|A{self.DOI})", "B_dA"),
            (f"P(A {self.GIAO} B)", "AgB"), (f"P(A {self.HOP} B)", "AhB"),
            (f"P(A{self.DOI})", "dA"), (f"P(B{self.DOI})", "dB")
        ]

        for i, (label, key) in enumerate(fields):
            tk.Label(f_in, text=label, width=12, anchor="w").grid(row=i, column=0, pady=2)
            ent = tk.Entry(f_in)
            ent.grid(row=i, column=1, sticky="ew", pady=2)
            f_in.grid_columnconfigure(1, weight=1)
            self.entries[key] = ent

        # 3. Nút bấm
        f_btn = tk.Frame(self.root, pady=10)
        f_btn.pack(fill="x", padx=10)
        tk.Button(f_btn, text="TÍNH & HIỆN QUY TRÌNH", command=self.solve, 
                  bg="#1a73e8", fg="white", font=("Arial", 10, "bold"), height=2).pack(side="left", fill="x", expand=True, padx=2)
        tk.Button(f_btn, text="XÓA", command=self.clear, bg="#dadce0", height=2).pack(side="right", fill="x", expand=True, padx=2)

        # 4. Vùng hiển thị (Kết quả + Quy trình chung một chỗ)
        self.res = tk.Text(self.root, height=20, state="disabled", bg="#f8f9fa", font=("Arial", 10), padx=10, pady=10)
        self.res.pack(fill="both", padx=10, pady=5)

    def clear(self):
        for e in self.entries.values(): e.delete(0, tk.END)
        self.res.config(state="normal")
        self.res.delete("1.0", tk.END)
        self.res.config(state="disabled")

    def solve(self):
        try:
            p = {k: float(e.get()) if e.get() else None for k, e in self.entries.items()}
            is_ind = self.independent.get()
            process = []

            # Suy luận logic & Trình bày quy trình
            for _ in range(5):
                # Biến cố đối
                if p['A'] is not None and p['dA'] is None:
                    p['dA'] = round(1 - p['A'], 4)
                    process.append(f"P(A{self.DOI}) = 1 - P(A) = 1 - {p['A']} = {p['dA']}")
                
                if p['B'] is not None and p['dB'] is None:
                    p['dB'] = round(1 - p['B'], 4)
                    process.append(f"P(B{self.DOI}) = 1 - P(B) = 1 - {p['B']} = {p['dB']}")

                # Công thức nhân / Độc lập
                if is_ind and p['A'] is not None and p['B'] is not None and p['AgB'] is None:
                    p['AgB'] = round(p['A'] * p['B'], 4)
                    process.append(f"P(A{self.GIAO}B) = P(A).P(B) = {p['A']}.{p['B']} = {p['AgB']}")
                elif p['B'] is not None and p['A_B'] is not None and p['AgB'] is None:
                    p['AgB'] = round(p['B'] * p['A_B'], 4)
                    process.append(f"P(A{self.GIAO}B) = P(B).P(A|B) = {p['B']}.{p['A_B']} = {p['AgB']}")

                # Xác suất toàn phần
                if p['B'] is not None and p['A_B'] is not None and p['dB'] is not None and p['A_dB'] is not None and p['A'] is None:
                    p['A'] = round(p['B']*p['A_B'] + p['dB']*p['A_dB'], 4)
                    process.append(f"P(A) = P(B).P(A|B) + P(B{self.DOI}).P(A|B{self.DOI})\n     = {p['B']}.{p['A_B']} + {p['dB']}.{p['A_dB']} = {p['A']}")

                # Định lý Bayes
                if p['AgB'] is not None and p['A'] and p['B_A'] is None:
                    p['B_A'] = round(p['AgB'] / p['A'], 4)
                    process.append(f"P(B|A) = P(A{self.GIAO}B) / P(A) = {p['AgB']} / {p['A']} = {p['B_A']}")

            # Hiển thị
            self.res.config(state="normal")
            self.res.delete("1.0", tk.END)
            self.res.insert(tk.END, "--- KẾT QUẢ CUỐI ---\n")
            names = {'A':'P(A)', 'B':'P(B)', 'AgB':f'P(A{self.GIAO}B)', 'B_A':'P(B|A)', 'dA':f'P(A{self.DOI})'}
            for k, v in p.items():
                if v is not None and k in names:
                    self.res.insert(tk.END, f"{names[k]} = {v}\n")
            
            if process:
                self.res.insert(tk.END, "\n--- QUY TRÌNH TÍNH ---\n")
                # Loại bỏ các bước lặp lại
                unique_steps = []
                for s in process:
                    if s not in unique_steps: unique_steps.append(s)
                self.res.insert(tk.END, "\n\n".join(unique_steps))
            
            self.res.config(state="disabled")

        except Exception:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")

if __name__ == "__main__":
    root = tk.Tk()
    ProbSolverDetailed(root)
    root.mainloop()
