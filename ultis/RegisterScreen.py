from auth import createUser
from tkinter import ttk, messagebox

class RegisterScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Tạo tài khoản mới (Admin Only)")
        self.master.geometry("400x500")

        fields = [
            ("Tên đăng nhập", "text"),
            ("Mật khẩu", "password"),
            ("Tuổi", "number"),
            ("Giới tính (Male/Female)", "text"),
            ("Nhóm máu (A, B, AB, O)", "text"),
            ("SĐT", "number"),
            ("Vai trò (admin/user)", "text")
        ]

        self.entries = {}

        ttk.Label(master, text="ĐĂNG KÝ THÀNH VIÊN", font=("bold", 14)).pack(pady=15)

        form_frame = ttk.Frame(master)
        form_frame.pack(pady=5)

        for idx, (lbl, type_) in enumerate(fields):
            ttk.Label(form_frame, text=lbl).grid(row=idx, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            if type_ == "password":
                entry.config(show="*")
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[lbl] = entry

        ttk.Button(master, text="Tạo tài khoản", command=self.submit, bg="#4CAF50", fg="white").pack(pady=20)

    def submit(self):
        data = {k: v.get() for k, v in self.entries.items()}

        # Validate cơ bản
        if any(v == "" for v in data.values()):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ các trường")
            return

        success, msg = createUser(
            name=data["Tên đăng nhập"],
            password=data["Mật khẩu"],
            age=data["Tuổi"],
            gender=data["Giới tính (Male/Female)"],
            blood_type=data["Nhóm máu (A, B, AB, O)"],
            phone=data["SĐT"],
            role=data["Vai trò (admin/user)"]
        )

        if success:
            messagebox.showinfo("Thành công", msg)
            self.master.destroy()
        else:
            messagebox.showerror("Lỗi", msg)