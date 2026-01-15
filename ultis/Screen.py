import tkinter as tk
from tkinter import ttk, messagebox
from data_manager import DataManagement
from auth import authenticate
from RegisterScreen import RegisterScreen
# --- Import Model Management (Cần file modelManagement.py cùng thư mục) ---
try:
    from modelManagement import DiabetesModel, NLPModel, HeartModel

    MODEL_AVAILABLE = True
except ImportError:
    MODEL_AVAILABLE = False
    print("Warning: Không tìm thấy modelManagement.py hoặc các file model. Chức năng dự đoán sẽ bị tắt.")


# ==============================================================================
# 1. LOGIN SCREEN
# ==============================================================================
class LoginScreen:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.master.title("Đăng nhập Hệ thống Gia đình")
        self.master.geometry("400x300")
        self.master.config(bg="#f0f2f5")

        frame = tk.Frame(master, bg="white", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="ĐĂNG NHẬP", font=("Helvetica", 16, "bold"), bg="white", fg="#333").pack(pady=10)

        # Username
        tk.Label(frame, text="Tên đăng nhập:", bg="white").pack(anchor=tk.W)
        self.entry_user = tk.Entry(frame, width=30)
        self.entry_user.pack(pady=5)

        # Password
        tk.Label(frame, text="Mật khẩu:", bg="white").pack(anchor=tk.W)
        self.entry_pass = tk.Entry(frame, show="*", width=30)
        self.entry_pass.pack(pady=5)

        # Button
        tk.Button(frame, text="Đăng nhập", command=self.check_login, bg="#1877f2", fg="white", width=20).pack(pady=20)

    def check_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        # authenticate giờ trả về 3 giá trị: status, msg, role
        success, msg, role = authenticate(user, pwd)

        if success:
            self.on_login_success(user, role)  # Truyền thêm role sang Main
        else:
            messagebox.showerror("Lỗi", msg)


# ==============================================================================
# 2. MAIN SCREEN (Menu chính)
# ==============================================================================
class MainScreen:
    def __init__(self, master, user_name, role):
        self.master = master
        self.user_name = user_name
        self.master.title(f"Health Dashboard - {user_name}")
        self.master.geometry("1000x600")
        self.role = role  # Lưu role


        # Khởi tạo các instance model (chỉ load 1 lần để tối ưu)
        if MODEL_AVAILABLE:
            try:
                self.md_diabetes = DiabetesModel()
                self.md_nlp = NLPModel()
                self.md_heart = HeartModel()
            except Exception as e:
                print(f"Lỗi load model: {e}")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="30")
        main_frame.pack(expand=True, fill='both')

        tk.Label(main_frame, text=f"Xin chào, {self.user_name}!", font=("Helvetica", 24, "bold"), fg="#007bff").pack(
            pady=(10, 30))

        # Container buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        # Danh sách chức năng & command tương ứng
        buttons = [
            ("👤 Thông tin Cá nhân", "#2196F3", self.open_user_info),
            ("📊 Dự đoán Tâm lí (NLP)", "#9C27B0", self.open_nlp_predict),
            ("❤️ Sức khỏe tim mạch", "#F44336", self.open_heart_predict),
            ("📈 Dự đoán tiểu đường", "#FF9800", self.open_diabetes_predict),
            ("🚪 Đăng xuất", "#607D8B", self.logout)
        ]

        if self.role == 'admin':
            buttons.insert(0, ("⚙️ Quản lý Người dùng (Admin)", "#333333", self.open_register))

            # Grid layout tự động tính toán lại
        for i, (text, color, cmd) in enumerate(buttons):
            row = i // 2
            col = i % 2
            tk.Button(
                btn_frame, text=text, command=cmd, bg=color, fg="white",
                font=("Helvetica", 10, "bold"), width=28, height=2
            ).grid(row=row, column=col, padx=10, pady=10)

    def open_register(self):
        win = tk.Toplevel(self.master)
        RegisterScreen(win)

    # --- Navigation Methods ---
    def open_user_info(self):
        win = tk.Toplevel(self.master)
        UserInfoScreen(win, self.user_name)

    def open_nlp_predict(self):
        if not MODEL_AVAILABLE: return messagebox.showerror("Lỗi", "Không tìm thấy Model")
        PredictScreen(self.master, "Dự đoán Tâm lí (NLP)",
                      [('Mô tả trạng thái (Tiếng Anh)', 'text')],
                      self.run_nlp)

    def open_heart_predict(self):
        if not MODEL_AVAILABLE: return messagebox.showerror("Lỗi", "Không tìm thấy Model")
        fields = [('Age', 'num'), ('Sex (1:M, 0:F)', 'num'), ('Chest Pain (0-3)', 'num'),
                  ('Resting BP', 'num'), ('Cholesterol', 'num'), ('Fasting BS (1/0)', 'num'),
                  ('Exercise Angina (1/0)', 'num'), ('Slope (0-2)', 'num')]
        PredictScreen(self.master, "Dự đoán Bệnh Tim", fields, self.run_heart)

    def open_diabetes_predict(self):
        if not MODEL_AVAILABLE: return messagebox.showerror("Lỗi", "Không tìm thấy Model")
        fields = [('Pregnancies', 'num'), ('Glucose', 'num'), ('BloodPressure', 'num'),
                  ('SkinThickness', 'num'), ('Insulin', 'num'), ('BMI', 'num'),
                  ('DiabetesPedigree', 'num'), ('Age', 'num')]
        PredictScreen(self.master, "Dự đoán Tiểu đường", fields, self.run_diabetes)

    def logout(self):
        self.master.destroy()

    # --- Callbacks gọi Model ---
    def run_nlp(self, values):
        res = self.md_nlp.predict(values[0])
        return f"Kết quả phân tích: {res}"

    def run_heart(self, vals):
        # Convert list string to int/float
        args = [float(x) for x in vals]
        res = self.md_heart.predict(*args)
        return "CÓ nguy cơ bệnh tim" if res == 1 else "Sức khỏe tim mạch BÌNH THƯỜNG"

    def run_diabetes(self, vals):
        args = [float(x) for x in vals]
        res = self.md_diabetes.predict(*args)
        return "Dương tính với Tiểu đường (Cần đi khám)" if res == 1 else "Âm tính (Bình thường)"


# ==============================================================================
# 3. GENERIC PREDICTION SCREEN (Dùng chung cho các model)
# ==============================================================================
class PredictScreen:
    def __init__(self, master, title, fields, predict_callback):
        self.win = tk.Toplevel(master)
        self.win.title(title)
        self.win.geometry("400x500")
        self.fields = fields  # List of tuple (Label, Type)
        self.callback = predict_callback
        self.entries = []

        tk.Label(self.win, text=title, font=("Helvetica", 14, "bold")).pack(pady=10)

        form_frame = tk.Frame(self.win)
        form_frame.pack(pady=10)

        for i, (lbl, ftype) in enumerate(fields):
            tk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            ent = tk.Entry(form_frame)
            ent.grid(row=i, column=1, padx=5, pady=5)
            self.entries.append(ent)

        tk.Button(self.win, text="DỰ ĐOÁN", command=self.do_predict, bg="green", fg="white").pack(pady=20)
        self.lbl_result = tk.Label(self.win, text="", font=("Helvetica", 12, "bold"), fg="red")
        self.lbl_result.pack()

    def do_predict(self):
        try:
            values = [e.get() for e in self.entries]
            if any(v == "" for v in values):
                messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
                return

            result_text = self.callback(values)
            self.lbl_result.config(text=result_text)
        except Exception as e:
            messagebox.showerror("Lỗi model", str(e))


# ==============================================================================
# 4. USER INFO SCREEN (Đã chỉnh sửa phần Xóa thuốc)
# ==============================================================================
class UserInfoScreen:
    def __init__(self, master, user_name):
        self.master = master
        self.user_name = user_name
        self.user_data = None
        master.title(f"Thông tin - {user_name}")
        master.geometry("900x600")

        if self.load_data():
            self.create_widgets()

    def load_data(self):
        data, message = DataManagement.get_user_info(self.user_name)
        if data is None:
            messagebox.showerror("Lỗi", message)
            return False
        self.user_data = data
        return True

    def create_widgets(self):
        # ... (Code hiển thị Info giữ nguyên như bản bạn gửi) ...
        # Phần hiển thị thông tin User
        info_frame = tk.LabelFrame(self.master, text="📋 Thông tin cá nhân", font=("bold"), padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)

        u = self.user_data['user_info']
        details = [f"Họ tên: {u.get('name')}", f"Tuổi: {u.get('age')}",
                   f"Giới tính: {u.get('gender')}", f"SĐT: {u.get('phone')}"]

        for i, txt in enumerate(details):
            tk.Label(info_frame, text=txt).grid(row=i // 2, column=i % 2, sticky="w", padx=20)

        tk.Button(info_frame, text="✏️ Chỉnh sửa (Demo)", command=self.edit_user_info).grid(row=2, columnspan=2,
                                                                                            pady=10)

        self.display_pharmacy_list()

    def display_pharmacy_list(self):
        p_frame = tk.LabelFrame(self.master, text="💊 Danh sách thuốc", font=("bold"))
        p_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        cols = ('Tên thuốc', 'Ghi chú')
        self.tree = ttk.Treeview(p_frame, columns=cols, show='headings', height=8)
        self.tree.heading('Tên thuốc', text='Tên thuốc');
        self.tree.column('Tên thuốc', anchor="center")
        self.tree.heading('Ghi chú', text='Ghi chú');
        self.tree.column('Ghi chú', anchor="center")

        for p in self.user_data['pharmacy']:
            self.tree.insert('', tk.END, values=(p.get('pharmacy'), p.get('notes')))

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons
        btn_box = tk.Frame(p_frame)
        btn_box.pack(fill=tk.X, pady=5)
        tk.Button(btn_box, text="➕ Thêm", command=self.add_pharmacy, bg="#4CAF50", fg="white").pack(side=tk.LEFT,
                                                                                                    padx=5)
        tk.Button(btn_box, text="🗑️ Xóa", command=self.delete_pharmacy, bg="#f44336", fg="white").pack(side=tk.LEFT,
                                                                                                       padx=5)

    def delete_pharmacy(self):
        selected = self.tree.selection()
        if not selected: return messagebox.showwarning("Cảnh báo", "Chọn thuốc cần xóa")

        if messagebox.askyesno("Xác nhận", "Xóa thuốc này?"):
            for item in selected:
                vals = self.tree.item(item)['values']
                # Gọi DataManager để xóa trong CSV
                success, msg = DataManagement.deletePharmacy(self.user_name, vals[0], vals[1])
                if success:
                    self.tree.delete(item)
                else:
                    messagebox.showerror("Lỗi", msg)

    def add_pharmacy(self):
        # Popup nhập liệu nhanh
        pop = tk.Toplevel(self.master)
        pop.title("Thêm thuốc")
        tk.Label(pop, text="Tên thuốc:").pack();
        e1 = tk.Entry(pop);
        e1.pack()
        tk.Label(pop, text="Ghi chú:").pack();
        e2 = tk.Entry(pop);
        e2.pack()

        def save():
            succ, msg = DataManagement.editPharmacy(self.user_name, e1.get(), e2.get())
            if succ:
                messagebox.showinfo("OK", msg)
                pop.destroy()
                self.refresh()
            else:
                messagebox.showerror("Lỗi", msg)

        tk.Button(pop, text="Lưu", command=save).pack(pady=10)

    def edit_user_info(self):
        messagebox.showinfo("Info", "Tính năng chỉnh sửa User tương tự như trong code cũ của bạn.")

    def refresh(self):
        for w in self.master.winfo_children(): w.destroy()
        if self.load_data(): self.create_widgets()