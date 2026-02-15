# Restaurant Management System

## Overview

The Restaurant Management System is a sophisticated web application designed to streamline operations within a restaurant, developed specifically for **Rombo Green View Hotel (RGVH)**. This application effectively manages core functionalities such as order placement, waiter payments, and expense tracking, making it an essential tool for restaurant management. Built primarily on the **Django framework** using **Python**, the system also incorporates modern web technologies like **HTML**, **CSS**, and **JavaScript** for an engaging user interface.

## Features

### Key Features Include:

- **Order Management**:
  - Simplifies the process for customers to place orders directly through an intuitive user interface.
  - Manages order status updates and modifications efficiently.

- **Payment Processing**:
  - Facilitates transparent management of waiter payments and integrates various payment methods.
  - Tracks expenses related to food supplies, staffing, and operational costs, ensuring financial clarity.

- **User Roles and Permissions**:
  - **Waiters** can manage customer orders and update the status of their tables.
  - **Cashiers** handle payment processing and generate financial reports.
  - **CEOs** and management staff have comprehensive oversight and access to all functionalities, including analytics and performance metrics.

### Technical Specifications

- **Backend**:
  - Developed in **Python** using the **Django** framework, ensuring robust performance and security.
- **Frontend**:
  - The user interface is built using **HTML**, **CSS**, and **JavaScript**, providing a responsive and user-friendly experience across devices.
- **Database**:
  - Uses **SQLite** for lightweight and efficient data storage, with the possibility of migrating to more robust databases like PostgreSQL for larger operations in the future.

## Getting Started

The following instructions outline how to set up the project on your local machine for development or testing purposes.

### Prerequisites

- Ensure you have **Python 3.6 or higher** installed on your machine.
- Familiarity with Git and command-line operations will be beneficial.

### Installation Steps

1. **Clone the Repository**:
   - Open your terminal (PowerShell on Windows, terminal on macOS/Linux) and execute the following command:
     ```bash
     git clone https://github.com/nikodemo-bukwimba/Restaurant-management-system.git
     ```

2. **Navigate to the Cloned Directory**:
   - Move into the project directory:
     ```bash
     cd Restaurant-management-system
     ```

3. **Open the Project in Your Code Editor** (optional):
   - For users of Visual Studio Code:
     ```bash
     code .
     ```

4. **Create a Virtual Environment**:
   - It’s best practice to create a virtual environment for Python projects to manage dependencies.
   - For **Windows (PowerShell)**:
     ```bash
     python -m venv venv
     .\venv\Scripts\Activate
     ```
   - For **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

5. **Install Project Dependencies**:
   - With the virtual environment activated, install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

6. **Run the Application**:
   - Launch the Django development server:
     ```bash
     python manage.py runserver
     ```

7. **Access the Application**:
   - Open a web browser and navigate to:
     [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - You should see the application's landing page, indicating the server is running correctly.

### User Roles and Login Credentials

Test the application using predefined user accounts that demonstrate different roles within the system:

- **Waiter**:
  - Username: `waiter`
  - Password: `Go12#34567`

- **Cashier**:
  - Username: `cashier`
  - Password: `Go12#34567`

- **CEO**:
  - Username: `ceo`
  - Password: `Go12#34567`

Each role has distinct permissions tailored to their responsibilities, allowing users to navigate and execute tasks relevant to their position within the system.

## Contribution Guidelines

We actively welcome contributions to enhance the functionality and performance of this project! Here’s how you can contribute:

1. **Fork the Repository**:
   - Use the "Fork" button at the top right of the repository page to create your own copy.

2. **Create a Feature Branch**:
   - In your local copy, create a new branch for your feature or fix:
     ```bash
     git switch -c feature-name
     ```

3. **Make Your Changes**:
   - Implement your changes and improve the code base as needed.

4. **Commit Your Changes**:
   - Commit your work with a clear and descriptive message:
     ```bash
     git commit -m "Add new feature or fix issue"
     ```

5. **Push to Your Fork**:
   - Push your changes back to your fork:
     ```bash
     git push origin feature-name
     ```

6. **Open a Pull Request**:
   - Navigate to the original repository and create a new Pull Request. Clearly explain your changes for review.

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file in the repository.

## Acknowledgments

Special thanks to the contributors and the team at Rombo Green View Hotel for their support and collaboration in developing this project.

---

Feel free to explore the application and contribute to making it better! Happy contributing.
