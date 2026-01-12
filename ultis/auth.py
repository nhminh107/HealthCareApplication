import hashlib
import pandas as pd
from sqlalchemy.sql.coercions import expect


def passHashing(password):
    return hashlib.sha256(password.encode()).hexdigest()

def createUser(name,password,age,gender,blood_type,phone,role):
    try:
        df = pd.read_csv('../familyData/userData.csv')
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
        df.to_csv('../familyData/userData.csv', index = False)
        return True, "Tạo người dùng"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"

def authenticate(username, password):
    try:
        df = pd.read_csv('../familyData/userData.csv')
        user_row = df[df['name' == username]]

        if user_row.empty:
            return False, "Not found user"
        else:
            userPassword = user_row.iloc[0]['password']
            if userPassword == passHashing(password):
                return True
            else:
                return False, "Incorrect Pass"

    except FileNotFoundError:
        return False, "You can't use this app"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"
