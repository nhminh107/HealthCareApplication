import numpy as np
import pandas as pd

# Import các module chứa model đã train
# Lưu ý: Việc import này sẽ chạy code training trong các file đó (do cấu trúc file gốc của bạn).
from Models import diabetes_model
from Models import combined_model
from Models import heart_model


class DiabetesModel:
    def __init__(self):
        # Lấy pipeline đã train từ module
        self.model = diabetes_model.diabetesModel

    def predict(self, Pregnancies, Glucose, BloodPressure, SkinThickness,
                Insulin, BMI, DiabetesPedigreeFunction, Age):
        # Mapping dữ liệu vào dictionary để dễ quản lý
        xDict = {
            'Pregnancies': Pregnancies,
            'Glucose': Glucose,
            'BloodPressure': BloodPressure,
            'SkinThickness': SkinThickness,
            'Insulin': Insulin,
            'BMI': BMI,
            'DiabetesPedigreeFunction': DiabetesPedigreeFunction,
            'Age': Age
        }

        # Đảm bảo thứ tự cột khớp với lúc train (quan trọng)
        colOrd = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                  'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

        # Tạo list giá trị theo đúng thứ tự
        xVal = [xDict[col] for col in colOrd]

        # Reshape thành mảng 2D (1 dòng, n cột) vì model sklearn yêu cầu
        xFinal = np.array(xVal).reshape(1, -1)

        prediction = self.model.predict(xFinal)
        return int(prediction[0])  # Trả về 0 hoặc 1


class NLPModel:
    def __init__(self):
        self.model = combined_model.combinedModel
        # Map kết quả số về lại nhãn chữ
        self.label_map = {
            7: 'Suicidal',
            6: 'Bipolar',
            5: 'Depression',
            4: 'Personality disorder',
            3: 'Anxiety',
            2: 'Stress',
            1: 'Normal'
        }

    def predict(self, sentence):
        # Pipeline NLP (TfidfVectorizer) yêu cầu đầu vào là một Iterable chứa string (List[str])
        # Không reshape thành (1, -1) ở đây vì TfidfVectorizer xử lý list text trực tiếp
        prediction_idx = self.model.predict([sentence])[0]

        # Trả về tên bệnh tương ứng
        return self.label_map.get(prediction_idx, "Unknown")


class HeartModel:
    def __init__(self):
        self.model = heart_model.heartModel

    def predict(self, age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, exercise_angina, slope):
        """
        Dựa trên logic drop cột trong heart_model.py, các features còn lại có khả năng là:
        age, sex, cp, trestbps, chol, fbs, exang, slope
        """
        # Gom dữ liệu thành mảng 2D
        xVal = [age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, exercise_angina, slope]
        xFinal = np.array(xVal).reshape(1, -1)

        prediction = self.model.predict(xFinal)
        return int(prediction[0])  # Trả về 0 hoặc 1


