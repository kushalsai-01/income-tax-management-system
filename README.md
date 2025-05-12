# 💰 Income Tax Management System

A full-fledged Income Tax Management System built using **Python (Flask)** for backend and **HTML/CSS** for frontend. This system helps automate the calculation, filing, and management of tax details for employees, making it efficient for both users and administrators.

---

## 🔧 Features

- 🔐 Secure user and admin login
- 📥 Employee income and deduction data entry
- 🧮 Auto income tax calculation using slabs
- 🗂️ Tax summary generation
- 📊 Admin dashboard with employee record management
- 🖨️ Printable tax reports

---

## 🧑‍💻 Technologies Used

- **Backend**: Python + Flask  
- **Frontend**: HTML, CSS, Bootstrap  
- **Database**: SQLite3  
- **Tools**: VS Code, Git

---

## 🗃️ Database Schema (Simplified)

- **Employee**
  - `id`, `name`, `email`, `pan`, `salary`, `deductions`

- **TaxRecord**
  - `id`, `employee_id`, `financial_year`, `taxable_income`, `tax_amount`

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/kushalsai-01/income-tax-management-system.git
   cd income-tax-management-system
