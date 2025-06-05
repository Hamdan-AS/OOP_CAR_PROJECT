==================================================  
# 🚗 CAR RENTAL SYSTEM (Python OOP)  
==================================================

📁 **Project Title:** Car Rental System  
🎓 **Course:** CS-116 - Object Oriented Programming  
📅 **Semester:** Spring 2025  
👨‍💻 **Developers:** [Taha,Anas, Hamdan]  
💻 **Language:** Python 3.x  
📄 **Main File:** `MASTER_FINALE.py`  
📦 **Data Files:** `cars.csv`, `users.csv` and others  

------------------------------------------------------  
## 🔧 STEP-BY-STEP FUNCTIONAL OVERVIEW  
------------------------------------------------------

### 1. 📥 PROGRAM STARTUP 🚀  
- The program begins by executing `seed_data()` which:  
  - 📂 Loads existing car data from `cars.csv`  
  - 👥 Loads registered users from `users.csv`  
  - ⚙️ If no data is found, it creates sample cars and a default admin  

### 2. 🛠️ MAIN MENU OPTIONS 📝  
Upon running, users can choose:  
1. 🔐 Admin Login  
2. 🆕 Register New Client  
3. 👤 Client Login  
0. ❌ Exit Program  

### 3. 🔐 ADMIN LOGIN 🔑  
- Use default credentials (`admin` / `admin123`) on first run  
- Access Admin Dashboard with options to:  
  - 👥 View all users or clients  
  - ➕➖ Add or remove cars  
  - 🚘 View reserved cars  

### 4. 🧾 CLIENT REGISTRATION & LOGIN ✍️  
- Register as a new client with basic information  
- 🆔 Username is auto-generated (e.g., `john_AB12`)  
- 📂 New client is added to `users.csv` and logged in  

### 5. 👤 CLIENT DASHBOARD OPTIONS 💼  
- 🚗 View available cars  
- 🛒 Rent a car (if balance is sufficient and car is available)  
- 🔄 Return a car  
- 📜 View rental history  
- 💰 Check and add balance  
- 🔓 Logout  

### 6. 💾 DATA PERSISTENCE 📊  
- 💾 All cars and users are saved persistently in `cars.csv` and `users.csv`  
- 🗃️ `CSVHandler` class handles all read/write operations  
- 💾 Data is saved after every change or on program exit  

------------------------------------------------------------  
## 🧱 OBJECT-ORIENTED DESIGN FEATURES 🛠️  
------------------------------------------------------------

✔️ Inheritance — `Client` and `Administer` inherit from `User`  
✔️ Encapsulation — Private balance and password fields 🔐  
✔️ Method Overriding — `Administer.renting()` is blocked 🚫  
✔️ Association — `Rental` links `Client` and `Car` 🔗  
✔️ Exception Handling — Validation and error control throughout ⚠️  
✔️ Static & Class Methods — `generate_username_tag()`, `CSVHandler` functions 🔧  

--------------------------------------------------  
## 📂 FILE STRUCTURE 📁  
--------------------------------------------------

- `MASTER_FINALE.py` → Main program logic and classes 🐍  
- `cars.csv` → List of all available and reserved cars 🚗  
- `users.csv` → Registered admins and clients 👥  
- `rentals.csv` → *(Optional for future use)* 🗂️  

--------------------------------------------------  
## 🧪 SAMPLE TEST CASES ✅  
--------------------------------------------------

✅ Client rents a car successfully (sufficient balance, car available)  
❌ Rental fails due to insufficient balance  
➕ Admin adds a car and then removes it using its ID  
🔄 Rental status updates car availability correctly  

--------------------------------------------------  
## 🔐 SECURITY NOTE ⚠️  
--------------------------------------------------

⚠️ Passwords are currently stored in plain text  
💡 For future expansion: We can use `hashlib` for SHA-256 password hashing 🔒  

==================================================
