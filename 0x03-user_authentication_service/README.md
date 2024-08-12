# 0x03. User authentication service

## Project Overview

This project is a simple user authentication service built with Flask, Python's lightweight web framework. The purpose of this project is to demonstrate the basic principles of user authentication, including user registration, login, session management, and handling HTTP status codes.

## Features

- **User Registration:** Allows users to create a new account with a username, email, and password.
- **User Login:** Authenticates users based on their email and password.
- **Session Management:** Maintains user session using cookies after successful login.
- **User Profile:** A simple profile page that displays a welcome message to the logged-in user.
- **Password Hashing:** Ensures that user passwords are securely stored using bcrypt.

## Requirements

- Ubuntu 18.04 LTS.
- Python 3.7
- pip (Python package installer)
- `pycodestyle` (version 2.5)
- `SQLAlchemy` 1.3.x
- All files must be executable.
- Flask app should only interact with `Auth` and never with `DB` directly.
- Only public methods of `Auth` and `DB` should be used outside these classes.
