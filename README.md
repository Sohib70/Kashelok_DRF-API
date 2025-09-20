📌 Shaxsiy Koshelok (Finance API)

Bu loyiha — foydalanuvchi autentifikatsiyasi (Users app) va moliyaviy boshqaruv (Finance app) imkoniyatlarini o‘z ichiga olgan Django Rest Framework API.
Foydalanuvchilar tizimga kirib, kirim/chiqimlarini yozishi, umumiy balans va davr kesimidagi hisobotlarni ko‘rishi mumkin.

🚀 Texnologiyalar

Python 3.10+

Django 5+

Django REST Framework

SimpleJWT (JWT autentifikatsiya uchun)

SQLite (standart, PostgreSQL qo‘llash mumkin)

⚙️ O‘rnatish
# Repo yuklab olish
git clone <repo-link>
cd <repo-folder>

# virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# kerakli kutubxonalarni o‘rnatish
pip install -r requirements.txt

# migratsiyalar
python manage.py migrate

# superuser yaratish
python manage.py createsuperuser

# serverni ishga tushirish
python manage.py runserver

📖 API Hujjatlar
🔹 Swagger UI

Interaktiv API hujjat:
👉 http://127.0.0.1:8000/api/schema/swagger-ui/

🔹 Redoc

Alternativ API hujjat:
👉 http://127.0.0.1:8000/api/schema/redoc/

🔹 Postman Collection

Tayyor Postman hujjati:
Koshelok API Postman Documentation
👉 https://documenter.getpostman.com/view/47089784/2sB3HtFGhk

👤 Users App (Auth)
🔹 Ro‘yxatdan o‘tish
POST /users/signup/

{
  "email_phone_number": "example@gmail.com"
}

🔹 Kodni tasdiqlash
POST /users/code_verify/

{ "code": "1234" }

🔹 Yangi kod olish
GET /users/new_verify/

🔹 Login
POST /users/login/

{
  "user_input": "example@gmail.com",
  "password": "12345678"
}

🔹 Logout
POST /users/logout/

{ "refresh": "xxx" }

🔹 Ma’lumotlarni yangilash
PUT /users/change_info/

{
  "first_name": "Ali",
  "last_name": "Valiyev",
  "username": "ali123",
  "password": "12345678",
  "password_confirm": "12345678"
}

🔹 Rasm yuklash
PATCH /users/image/
(Form-data orqali photo yuboriladi)

🔹 Parolni unutganda
POST /users/forgot/

{ "phone_email": "example@gmail.com" }

🔹 Parolni reset qilish
PUT /users/reset/

{
  "code": "1234",
  "password": "newpass",
  "confirm_password": "newpass"
}

🔹 Parolni yangilash (login bo‘lgandan keyin)
PUT /users/update/

{
  "old_pass": "old123",
  "new_pass": "new123",
  "confirm_new_pass": "new123"
}

💰 Finance App
🔹 Kategoriya yaratish
POST /finance/categories/

{
  "name": "Ovqatlanish",
  "type": "expense"
}

🔹 Kategoriyalar ro‘yxati
GET /finance/categories/


Javob:

[
  {
    "id": 1,
    "name": "Ovqatlanish",
    "type": "expense",
    "total_amount": 250000
  }
]

🔹 Tranzaksiya yaratish
POST /finance/transactions/

{
  "category": 1,
  "amount": 50000,
  "comment": "Nonushta",
  "date": "2025-09-21"
}

🔹 Tranzaksiyalar ro‘yxati
GET /finance/transactions/

🔹 Dashboard
GET /finance/dashboard/


Javob:

{
  "balance": 200000,
  "categories": [
    { "category_name": "Ovqatlanish", "type": "expense", "total": 50000 },
    { "category_name": "Maosh", "type": "income", "total": 250000 }
  ]
}

🔹 Summary (hisobot)
GET /finance/summary/<period>/


period = daily | weekly | monthly

Javob:

{
  "start_date": "2025-09-21",
  "end_date": "2025-09-21",
  "income": 250000,
  "expense": 50000,
  "balance": 200000
}


📌 Custom davr uchun:

GET /finance/summary/daily/?start_date=2025-09-01&end_date=2025-09-15

🔑 JWT Token ishlatish

Har bir so‘rovda:

Authorization: Bearer <access_token>


Agar access muddati tugasa, refresh orqali yangilash mumkin:

POST /users/token/refresh/

{ "refresh": "xxx" }