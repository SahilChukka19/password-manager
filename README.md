# Password Vault: Secure, Easy-to-Use Password Manager

A simple password manager built using Python and Tkinter for the GUI. This application securely stores and manages passwords for different websites, using encryption for protection. It offers features like user authentication, password visibility toggle, and the ability to add, edit, and delete passwords.

## Features
- **User Authentication**: Login and registration functionality.
- **Password Management**: Store passwords securely for various websites.
- **Encryption**: Strong encryption for password protection.
- **Password Visibility Toggle**: View passwords when needed.
- **Add, Edit, Delete**: Manage your passwords easily.

## Requirements
- Python 3
- `tkinter` (for GUI)
- `cryptography` (for encryption)
- SQLite (for database)

## Setup Instructions

### 1. Clone the Repository
First, clone this repository to your local machine:

```bash
git clone https://github.com/SahilChukka19/password-manager.git
cd password-manager
```
### 2. Install Dependencies
Ensure that you have Python 3.x installed. Install the required libraries by running:
```bash
pip install -r requirements.txt
```

### 3.  Database Setup
To set up the database, you need to run the `setup_db.py` script. This will create the necessary tables and database for the application.
```bash
python database/setup_db.py
```

### 4 Generating the secrets.key File
The application uses an encryption key (secrets.key) to securely store passwords. The key must never be pushed to version control or shared publicly.

To generate the secrets.key file, follow these steps:

#### 1. Create a `config` folder in the root directory
#### 2.  Create a secrets.key file inside the `config/`folder.
#### 3. Run the `encryption.py` which is located inside the `security` directory script to generate and save the key in the `secrets.key` file.
```bash
python security/encryption.py
```

### 5. Run the Application
To start the password manager, execute the following command:
```bash
python main.py
```
This will launch the login screen. If you don't have an account, you can register. Once logged in, you'll have access to the main app to manage your passwords.



## Usage

### Login
* Enter your username and password to log in.
* If you don't have an account, you can register a new user.
### Register
* Click on the "Register" button on the login screen.
* Provide a username and password, and you'll be able to log in immediately.
### Add Password
* After logging in, you can add a password for a specific website.
* Enter the website, username, and password, and it will be securely stored in the database.
### Edit Password
* To edit an existing password, select it from the list.
* Modify the details and save the changes.
### Delete Password
* To delete a password, select it from the list and confirm the deletion.
### Logout
* You can log out of the application from the main screen.
## Security Considerations
* The application uses encryption to securely store passwords in the database.
* The secrets.key file is crucial for encryption, so keep it safe and do not push it to public repositories.
* The application does not store passwords in plain text, ensuring your sensitive data is protected.

## Acknowledgements
* This project uses the `cryptography` library for encryption.
* The application uses the Tkinter library for creating the GUI.

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sahil-chukka)

[![gmail](https://img.shields.io/badge/gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sahil.chukka@gmail.com)


