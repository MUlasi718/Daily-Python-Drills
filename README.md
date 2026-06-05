Kitchen OS: Full-Stack Restaurant Management System
Kitchen OS is a lightweight, full-stack web application designed to handle the end-to-end operations of a modern restaurant. Originally built as a terminal-based Python application during a 30-Day Engineering Challenge, it has been refactored into a scalable, cloud-ready Software-as-a-Service (SaaS) prototype using Flask and Bootstrap.

This system bridges the gap between Front-of-House (POS), Back-of-House (KDS), and the Manager's Office (Analytics & HR).

Key Features
Role-Based Access Control (RBAC): Secure login portal that restricts application access based on employee privileges (Admin vs. Standard Employee).

Web-Based Point of Sale (POS): A dynamic, responsive cash register interface featuring an active cart, total calculations, and custom kitchen notes.

Inventory & Recipe Management: Tracks live inventory counts and integrates with the Spoonacular API to dynamically calculate recipe food costs, recommended selling prices, and profit margins.

HR & Time Clock: Built-in payroll tracking that allows employees to punch in/out using unique IDs, calculating shift durations down to the decimal and saving them to the database.

Automated Marketing Pipeline: Cross-references daily specials with a customer contact database to simulate automated Email and SMS marketing dispatches.

EOD Accounting & Analytics: Automatically queries the database to generate timestamped CSV financial exports and visual profit charts for management.

Live Weather Integration: Uses the Open-Meteo API to pull live weather forecasts, helping managers predict foot traffic and prep volume.

Tech Stack
Backend: Python 3, Flask (Web Framework & Routing)

Frontend: HTML5, CSS3, Bootstrap 5, Jinja2 Templating

Database: SQLite3 (Multi-table relational data storage)

External APIs: Spoonacular (Food/Recipe Data), Open-Meteo (Geocoding & Weather)

Data Visualization: Matplotlib, CSV

Engineering Journey
This project was developed incrementally over 30 days, evolving from a simple command-line Python script into a fully integrated web application. It demonstrates core software engineering principles including the HTTP Request-Response cycle, Session Management, REST API integration, CRUD database operations, and secure user authentication.
