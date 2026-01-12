import tkinter as tk
from Screen import LoginScreen, MainScreen


def main():
    root = tk.Tk()

    # Ẩn cửa sổ gốc ban đầu (nếu muốn) hoặc dùng nó làm container
    # Ở đây ta dùng root làm cửa sổ Login, sau đó switch sang Main

    def on_login_success(user_name):
        # Khi login thành công:
        # 1. Xóa hết widget của Login
        for widget in root.winfo_children():
            widget.destroy()

        # 2. Khởi tạo Main Screen trên cùng cửa sổ root
        # (Hoặc có thể destroy root cũ và tạo root mới, nhưng cách này mượt hơn)
        app = MainScreen(root, user_name)

    # Khởi tạo màn hình Login
    app = LoginScreen(root, on_login_success)

    root.mainloop()


if __name__ == "__main__":
    main()