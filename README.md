# Modern Password Manager
A simple, modern, and secure desktop application for generating, storing, and retrieving passwords. This application uses a dark-themed graphical user interface built with CustomTkinter and a MongoDB database running in a Docker container for data persistence. Passwords are encrypted before being saved to ensure security.

## ✨ Features
Secure Password Generation: Creates strong, random alphanumeric passwords including uppercase letters, lowercase letters, numbers, and special characters.

Encrypted Storage: All credentials (username and password) are encrypted using the cryptography library before being saved.

Easy Retrieval: Quickly find your saved username and password by searching for the website URL.

Clipboard Integration: Copy your password to the clipboard with a single click.

Modern UI: A clean, dark-themed, and intuitive user interface.

## 🛠️ Prerequisites
Before you begin, ensure you have the following software installed on your system:

```Python 3.8+```

```Docker Desktop```

## 🚀 Installation and Setup
Follow these steps to get the application running on your local machine.

* Clone the Repository
    
    First, clone this repository to your local machine using Git:
    ```
    git clone <URL_OF_YOUR_REPOSITORY_GITHUB>

    cd MyPwdManagiah
    ```
* Set Up the Python Environment
    
    It's highly recommended to use a virtual environment to manage project dependencies.

## Create a virtual environment
Create a virtual enviroment using the following command:
```
py -m venv .venv
```

## Activate the virtual environment On Windows (PowerShell):
```
.\.venv\Scripts\Activate.ps1
```
# On macOS/Linux:
```
 source .venv/bin/activate
```

## Start the MongoDB Database with Docker
This application uses a MongoDB database running inside a Docker container.

* Make sure Docker Desktop is running on your machine.  

    If you don't have Docker, download from:    
    https://www.docker.com/products/docker-desktop/

* Run the following command in your terminal to download the mongo:6.0 image and start the container with the correct credentials:  
   
    ⚠️ change the username and password in the command     
    ```
    docker run -d --name my-password-manager-db -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=yourUsername -e MONGO_INITDB_ROOT_PASSWORD=yourPassword mongo:6.0
    ```

   ⚠️ Wait about 10-15 seconds for the database to initialize completely. You can check if the container is running with docker ps.

## Install the required Python packages
pip install customtkinter pymongo cryptography python-dotenv pyperclip

* Configure the Encryption Key  
    The application uses an encryption key stored in an .env file to secure your passwords.     
    Generate a new key by running the generate_key.py script:
    ```
    py generate_key.py
    ```

    * Copy the key that is printed to the terminal.

    * Create a new file in the root of the project named .env.

    * Add the copied key to the .env file like this:
    ```
    ENCRYPTION_KEY=the_key_you_generated_here
    MONGO_URI=mongodb://YOURUSERNAME:YOURPASSWORD@localhost:27017/?authSource=admin
    ```
    ⚠️ Important: Change the username and password in your .env    
    ⚠️ Important: The .gitignore file is configured to ignore the .env file. Never commit this file to a public repository.

## ▶️ Running the Application
Once you have completed all the setup steps, you can run the application with the following command:
```
py app.py
``` 

The graphical user interface should now appear on your screen, ready to use.

## 📝 How to Use
The application is divided into two main tabs:

* Generator Tab     
        1. Enter the Website URL you are creating the password for.    
        2. Enter the Username or Email associated with the account.    
        3. Click the "Generate Password" button. A strong password will be created and displayed.  
        4. If you are satisfied, click the "Save Credentials" button to encrypt and save the data in the database.

* Retriever Tab     
        1. Enter the Website URL for which you want to retrieve the credentials.   
        2. Click the "Search" button.  
        3. If found, the corresponding Username and Password will be displayed.    
        4. You can then click the "Copy Password" button to copy it to your clipboard.
