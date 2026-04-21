# Lockbox 

I wanted to build something practical that solves a realworld problem (password fatigue and credential reuse). This project was a great way for me to challenge myself and learn more about backend security, relational databases, and test driven devellopment.

## What it does
Lockbox helps users generate strong, random passwords and stores them securely in an encrypted vault. 
Secure Authentication: Users can create an account and log in. User passwords are salted and hashed before being stored.
Password Generation: Automatically generates secure passwords (using a mix of uppercase, lowercase, numbers, and symbols).
Encrypted Storage: The generated passwords are symmetrically encrypted before going into the database, meaning they are never stored in plain text.
Data Isolation: Uses relational database foreign keys so users can only ever access and decrypt their own vault entries.
Clean UI: A simple, minimalistic interface built with Bootstrap that shows password constraints and makes navigation easy.

## Tech Stack
Backend: Python, Flask
Database: SQLite, SQLAlchemy (ORM)
Frontend: HTML, CSS, Bootstrap
Testing: Pytest
Libraries: Flask-Login (session management), Flask-WTF (forms & CSRF protection)

## What I Learned & Technical Highlights
Database Design: I designed a relational database in Third Normal Form (3NF) using a one-to-many relationship between a `User` table and a `UserPasswords` table. Using SQLAlchemy helped  me naturally prevent SQL Injection attacks.
Project Architecture: I split the codebase up logically (`routes.py`, `models.py`, `forms.py`, `services.py`) to keep the code clean and maintainable.
Automated Testing: I wrote comprehensive unit tests using Pytest to verify my database models, form validations, routing, and encryption/decryption logic. 

## How to run

1. Clone the repository:
   ```bash
   git clone [https://github.com/ericanamangillan-bit/Lockbox-App](https://github.com/ericanamangillan-bit/Lockbox-App)
   cd lockbox