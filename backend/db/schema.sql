-- Create Users Table
CREATE DATABASE IF NOT EXISTS finance_tracker;
USE finance_tracker;

-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    age INT,
    working_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CATEGORY TABLE
CREATE TABLE category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- PAYMENT METHOD TABLE
CREATE TABLE payment_method (
    payment_method_id INT PRIMARY KEY AUTO_INCREMENT,
    method_name VARCHAR(50) NOT NULL
);

-- INCOME TABLE
CREATE TABLE income (
    income_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    source VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    received_on DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- EXPENSES TABLE
CREATE TABLE expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    category_id INT,
    payment_method_id INT,
    amount DECIMAL(10,2) NOT NULL,
    spent_on DATE,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_method(payment_method_id)
);

-- GOALS TABLE
CREATE TABLE goals (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    title VARCHAR(100),
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0.00,
    deadline DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- BUDGET TABLE
CREATE TABLE budget (
    budget_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    category_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    month VARCHAR(7),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
