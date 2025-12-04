# StudyEdge Education Consultancy – Web Application

This repository contains the official website for **StudyEdge Education Consultancy**, built with **Django** and **Tailwind CSS**. The platform provides a modern landing page along with integrated **Contact Form** and **Student Support Form**, all managed through the Django **Admin Panel**.

---

## 🚀 Features

* ✅ Modern responsive landing page using **Tailwind CSS**
* ✅ Contact form integrated with Django Admin
* ✅ Student support / inquiry form integrated with Admin
* ✅ Secure Django Admin Panel for managing submissions
* ✅ Clean project structure following Django best practices
* ✅ Static files handled with Tailwind build
* ✅ Ready for production deployment

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, Tailwind CSS
* **Database:** SQLite (default, can be changed)
* **Admin Panel:** Django Admin
* **Build Tool:** Node.js + Tailwind CLI

---

## 📂 Project Structure (Overview)

```
project-studyedge/
│
├── core/                # Main Django app (views, models, urls)
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, Images)
├── theme/               # Tailwind configuration
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sixdgt/project-studyedge.git
cd project-studyedge
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Node Modules (for Tailwind)

```bash
npm install
```

### 5️⃣ Build Tailwind CSS

```bash
npm run dev
```

### 6️⃣ Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Create Admin Superuser

```bash
python manage.py createsuperuser
```

### 8️⃣ Start Development Server

```bash
python manage.py runserver
```

Now open in your browser:

```
http://127.0.0.1:8000/
```

---

## 🧑‍💼 Admin Panel

Access the admin panel at:

```
http://127.0.0.1:8000/admin/
```

From the admin panel you can:

* Manage contact form submissions
* Manage student support requests
* Control site data

---

## 📝 Forms Integrated

### ✅ Contact Form

* Collects user inquiries
* Automatically saved in Django Admin

### ✅ Student Support Form

* Collects detailed student support requests
* Managed via Admin dashboard

---

## 📦 Environment Variables (Optional)

You can create a `.env` file for:

* `SECRET_KEY`
* `DEBUG`
* `DATABASE_URL`

---

## ✅ Deployment Ready

This project can be deployed on:

* PythonAnywhere
* DigitalOcean
* Vercel (Frontend) + Render (Backend)
* Railway

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push and create a Pull Request

---

## 📄 License

This project is licensed for educational and commercial use.

---

## 📞 Project Owner

**StudyEdge Education Consultancy Pvt. Ltd.**
Website built using Django & Tailwind CSS

---

✅ If you like this project, don’t forget to ⭐ the repository!
