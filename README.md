# Restaurant Management System

## Overview

The Restaurant Management System is a web-based application developed to streamline restaurant operations at **Rombo Green View Hotel (RGVH)**.

The system supports essential workflows such as order management, payment processing, expense tracking, and administrative oversight. It uses role-based access control to simulate real-world restaurant responsibilities.

### Technology Stack

- **Backend:** Python (Django Framework)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default, configurable)

---

## Features

### Order Management
- Create and manage customer orders
- Update order status
- Assign and manage tables
- Track completed and pending orders

### Payment Processing
- Process customer payments
- Generate receipts
- Track daily transactions
- Monitor operational expenses

### Role-Based Access Control
- Restricts access based on user roles
- Protects financial and administrative data
- Reflects real restaurant operational structure

---

## Technical Specifications

### Backend
- Python 3.6 or higher
- Django Framework

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite (default configuration)
- Can be migrated to PostgreSQL for production environments

---

## Getting Started

Follow the steps below to set up the project locally for development or testing.

### Prerequisites

Ensure you have installed:

- Python 3.6+
- Git
- pip (Python package manager)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/nikodemo-bukwimba/Restaurant-management-system.git
```

### 2. Navigate to the Project Directory
```bash
cd Restaurant-management-system
```

### 3. Create a Virtual Environment

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and visit:
```
http://127.0.0.1:8000/
```

If configured correctly, the application homepage will load.

---

## User Roles and Capabilities

The system includes predefined user roles to simulate real restaurant operations. Each role has clearly defined permissions aligned with operational responsibilities.

### Role Overview

| Role | Description | Key Capabilities |
|------|-------------|------------------|
| Waiter | Front-of-house staff responsible for handling customer orders and table service. | Create and manage customer orders, Update order status, View assigned tables |
| Cashier | Responsible for financial transactions and payment processing. | Process payments, Generate receipts, View financial summaries |
| CEO | Administrative and executive-level user with full system access. | Full system access, View analytics and reports, Manage users and permissions, Monitor expenses |

### Test User Accounts

Use the following credentials to test role-based functionality:

**Waiter**
- Username: `waiter`
- Password: `Go12#34567`

**Cashier**
- Username: `cashier`
- Password: `Go12#34567`

**CEO**
- Username: `ceo`
- Password: `Go12#34567`

### Purpose of Role Separation

Role-based access control ensures:

- Staff members access only features relevant to their responsibilities.
- Sensitive financial and administrative information is restricted.
- The system reflects real-world restaurant operational workflows.
- Contributors clearly understand the purpose of each test account.

---

## Contribution Guidelines

We welcome contributions to improve this project.

### Contribution Workflow

1. Fork the repository
2. Create a new branch:
```bash
   git switch -c feature-name
```
3. Make your changes
4. Commit your work:
```bash
   git commit -m "Describe your changes"
```
5. Push your branch:
```bash
   git push origin feature-name
```
6. Open a Pull Request with a clear explanation of your changes

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

Special thanks to the team at Rombo Green View Hotel for their collaboration and support during development.

Feel free to explore the application and contribute to improving the system.