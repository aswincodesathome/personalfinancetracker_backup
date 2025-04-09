# Entities and Relationships for Personal Finance Tracker

This document defines the core entities, attributes, relationships, and constraints used in the Personal Finance Tracker DBMS project.

---

## 🔹 ENTITIES & ATTRIBUTES

### 1. User
- user_id (PK)
- name
- age
- email
- password
- working_status (employed, student, etc.)

### 2. Income
- income_id (PK)
- user_id (FK)
- source (e.g., Salary, Freelancing)
- amount
- date_received

### 3. Expense
- expense_id (PK)
- user_id (FK)
- category_id (FK)
- payment_method_id (FK)
- amount
- description
- date

### 4. Category
- category_id (PK)
- name (e.g., Food, Transport, Rent)

### 5. Budget
- budget_id (PK)
- user_id (FK)
- category_id (FK)
- amount_limit
- month_year

### 6. Goal
- goal_id (PK)
- user_id (FK)
- goal_name
- target_amount
- deadline
- current_saved

### 7. Payment_Method
- payment_method_id (PK)
- user_id (FK)
- method_type (Cash, Card, UPI)
- details (optional notes)

---

## 🔗 RELATIONSHIPS

- A **User** can have multiple **Incomes**, **Expenses**, **Budgets**, **Goals**, and **Payment Methods**.
- An **Expense** belongs to one **Category** and one **Payment Method**.
- A **Budget** is set by a **User** for a specific **Category**.
- A **Goal** is personal and linked to a **User**.

---

## ♾️ CARDINALITY

- User → Income: 1 to many
- User → Expense: 1 to many
- User → Goal: 1 to many
- User → Payment_Method: 1 to many
- Category → Expense: 1 to many
- Payment_Method → Expense: 1 to many

---

## 📌 PARTICIPATION CONSTRAINTS

- Every **Expense** must be linked to a **User**, **Category**, and **Payment Method** (total participation).
- Every **Income** must be linked to a **User**.
- Every **Budget** must have a **User** and a **Category**.

---

## 📝 Notes

- All IDs are primary keys (PK).
- FK = Foreign Key.
- Date formats should follow `YYYY-MM-DD`.

