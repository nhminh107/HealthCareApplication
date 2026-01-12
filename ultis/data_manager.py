import pandas as pd


class DataManagement:
    @staticmethod
    def get_user_info(user_name):
        try:
            df = pd.read_csv('../familyData/userData.csv')
            data_row = df[df['name'] == user_name]

            if data_row.empty:
                return None, "Không tìm thấy người dùng"

            # Lấy thông tin cá nhân
            user_info = data_row.iloc[0].to_dict()

            # Lấy danh sách thuốc
            df2 = pd.read_csv('../familyData/test.csv')
            data_row2 = df2[df2['user_name'] == user_name]
            pharmacy_list = data_row2.to_dict('records')

            # Kết hợp dữ liệu
            result = {
                'user_info': user_info,
                'pharmacy': pharmacy_list
            }

            return result, "Thành công"

        except Exception as e:
            return None, f"Lỗi: {str(e)}"

    @staticmethod
    def editData(user_name, col_name, value):
        try:
            df = pd.read_csv('../familyData/userData.csv')

            # Tìm index của user
            user_index = df[df['name'] == user_name].index

            if user_index.empty:
                return False, "Không tìm thấy người dùng"

            df.loc[user_index[0], col_name] = value

            # Lưu lại file CSV
            df.to_csv('../familyData/userData.csv', index=False)

            return True, "Đã thay đổi dữ liệu"

        except KeyError:
            return False, f"Không tìm thấy cột '{col_name}'"
        except Exception as e:
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    def editPharmacy(user_name, pName, pNotes):
        FILE_PATH = '../familyData/test.csv'
        try:
            df = pd.read_csv(FILE_PATH)

            # Tạo dictionary của dòng mới
            new_record_dict = {
                'user_name': user_name,
                'pharmacy': pName,
                'notes': pNotes
            }

            # 🌟 SỬA LỖI: Chuyển đổi dict thành DataFrame
            new_df_record = pd.DataFrame([new_record_dict])

            # Nối DataFrame gốc với DataFrame của record mới
            df = pd.concat([df, new_df_record], ignore_index=True)

            # Lưu lại file CSV
            df.to_csv(FILE_PATH, index=False)

            return True, "Đã thêm thuốc thành công"

        except Exception as e:
            # Bạn nên thêm FileNotFoundError ở đây nếu file test.csv chưa tồn tại
            return False, f"Lỗi: {str(e)}"

    @staticmethod
    @staticmethod
    def deletePharmacy(user_name, pName, pNotes):
        FILE_PATH = '../familyData/test.csv'

        try:
            df = pd.read_csv(FILE_PATH)
            condition = (df['user_name'] == user_name) & \
                        (df['pharmacy'] == pName) & \
                        (df['notes'] == pNotes)

            if not condition.any():
                return False, "Không tìm thấy mục thuốc cần xóa khớp với thông tin cung cấp."

            # 3. LỌC: Tạo DataFrame mới (df_new) bằng cách loại bỏ các hàng khớp
            # Toán tử '~' (dấu ngã) đảo ngược điều kiện, giữ lại các hàng KHÔNG khớp.
            df_new = df[~condition]

            # 4. Ghi đè file CSV với dữ liệu mới (đã xóa)
            df_new.to_csv(FILE_PATH, index=False)

            return True, "Đã xóa thuốc khỏi danh sách thành công."

        except FileNotFoundError:
            return False, f"Lỗi: Không tìm thấy file dữ liệu thuốc tại {FILE_PATH}."
        except KeyError:
            return False, "Lỗi tên cột. Vui lòng kiểm tra lại tên cột 'user_name', 'pharmacy' và 'notes' trong file."
        except Exception as e:
            return False, f"Lỗi không xác định khi xóa: {str(e)}"