import tkinter as tk
from Screen import LoginScreen, MainScreen
import auth

auth.initialize_system()


def main():
    root = tk.Tk()

    # Ẩn cửa sổ gốc ban đầu (nếu muốn) hoặc dùng nó làm container
    # Ở đây ta dùng root làm cửa sổ Login, sau đó switch sang Main

    # main.py
    def on_login_success(user_name, role):  # Nhận thêm role
        for widget in root.winfo_children():
            widget.destroy()
        app = MainScreen(root, user_name, role)  # Truyền role vào Main

    # Khởi tạo màn hình Login
    app = LoginScreen(root, on_login_success)

    root.mainloop()


if __name__ == "__main__":
    main()