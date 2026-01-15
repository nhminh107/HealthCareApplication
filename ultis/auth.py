import hashlib
import pandas as pd
import os

FILE_PATH = '../familyData/userData.csv'


def passHashing(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Hàm kiểm tra và khởi tạo Admin mặc định
def initialize_system():
    # Kiểm tra thư mục tồn tại chưa
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    # Nếu file chưa tồn tại hoặc rỗng, tạo mới và thêm Admin
    if not os.path.exists(FILE_PATH) or os.stat(FILE_PATH).st_size == 0:
        df = pd.DataFrame(columns=['user_id', 'name', 'password', 'age', 'gender', 'blood_type', 'phone', 'role'])
        # Tạo Admin mặc định: Admin / abcd1234
        admin_user = {
            'user_id': 1,
            'name': 'Admin',
            'password': passHashing('abcd1234'),
            'age': 30,
            'gender': 'Male',
            'blood_type': 'O',
            'phone': '0000000000',
            'role': 'admin'  # Role quan trọng
        }
        df = pd.concat([df, pd.DataFrame([admin_user])], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        print("Đã khởi tạo tài khoản Admin mặc định.")




def createUser(name, password, age, gender, blood_type, phone, role='user'):
    try:
        df = pd.read_csv(FILE_PATH)
        if name in df['name'].values:
            return False, "Tên đã tồn tại"

        new_id = df['user_id'].max() + 1 if len(df) > 0 else 1

        new_user = {
            'user_id': new_id,
            'name': name,
            'password': passHashing(password),
            'age': age,
            'gender': gender,
            'blood_type': blood_type,
            'phone': phone,
            'role': role
        }

        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        return True, "Tạo người dùng thành công"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"


def authenticate(username, password):
    try:
        df = pd.read_csv(FILE_PATH)
        user_row = df[df['name'] == username]  # Sửa lỗi cú pháp df['name' == username] cũ

        if user_row.empty:
            return False, "Không tìm thấy người dùng", None
        else:
            user_data = user_row.iloc[0]
            if user_data['password'] == passHashing(password):
                # TRẢ VỀ THÊM ROLE
                return True, "Đăng nhập thành công", user_data['role']
            else:
                return False, "Sai mật khẩu", None

    except FileNotFoundError:
        initialize_system()  # Thử tạo lại nếu mất file
        return False, "Dữ liệu vừa được khởi tạo lại, vui lòng thử lại.", None
    except Exception as e:
        return False, f"Lỗi: {str(e)}", None