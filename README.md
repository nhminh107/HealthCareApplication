# HealthCareApplication

HealthCareApplication là **dự án cá nhân** được xây dựng nhằm **làm quen với việc thiết kế và tổ chức một ứng dụng quản lý chăm sóc sức khỏe**, tập trung vào cách xây dựng cấu trúc thư mục, mô hình dữ liệu và xử lý logic nghiệp vụ bằng **Python**.

> ⚠️ **Lưu ý:**  
> Đây **không phải sản phẩm thương mại**. Dự án được thực hiện với mục đích **học tập, thực hành và nâng cao kỹ năng lập trình**, đặc biệt là tư duy OOP và tổ chức code.

---

## 🎯 Mục tiêu dự án

- Làm quen với việc thiết kế **ứng dụng Healthcare** ở mức cơ bản  
- Rèn luyện kỹ năng **Object-Oriented Programming (OOP)**  
- Thực hành chia module, quản lý dữ liệu và mở rộng hệ thống  
- Tạo nền tảng để phát triển các tính năng phức tạp hơn trong tương lai

---

## 📌 Tổng quan

Ứng dụng tập trung vào việc mô hình hóa:
- Dữ liệu liên quan đến **sức khỏe**
- Thông tin **cá nhân / gia đình**
- Các **model nghiệp vụ**
- Các **tiện ích hỗ trợ xử lý dữ liệu**

Dự án hiện ở giai đoạn **prototype / learning project**.

---

## 📁 Cấu trúc thư mục

HealthCareApplication/
├── Data/ # Chứa dữ liệu và logic xử lý dữ liệu
├── Models/ # Các class / model nghiệp vụ (OOP)
├── familyData/ # Dữ liệu và logic liên quan đến gia đình
├── ultis/ # Các hàm tiện ích (helper / utility)
└── README.md # Tài liệu mô tả dự án


---

## ⚙️ Công nghệ sử dụng

- **Ngôn ngữ:** Python 3  
- **Paradigm:** Object-Oriented Programming (OOP)  
- **Mục đích:** Học tập & thực hành

---

## 🚀 Cách chạy dự án

1. Clone repository:

```bash
git clone https://github.com/nhminh107/HealthCareApplication.git
cd HealthCareApplication
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows
python main.py
