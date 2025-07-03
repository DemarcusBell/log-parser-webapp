# Log Parser Web App

A lightweight Flask-based web application that allows users to upload server log files and extract key information like IP addresses, error messages, and timestamps. This tool is useful for security analysts and SOC teams who need quick triage on raw logs.

## 🔧 Features

- Upload `.log` files through a user-friendly web interface
- Parse logs using regular expressions
  - Extract IP addresses
  - Extract timestamps
  - Identify error strings (e.g., 404, 500, etc.)
- Export parsed output to downloadable JSON

## 🛠 Tech Stack

- Python 3
- Flask (Web Framework)
- Regex (Log Parsing)
- HTML/CSS (Frontend)
- JSON (Output Format)

## 📁 File Structure

