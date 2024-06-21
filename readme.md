USER MANUAL 

This manual provides a comprehensive guide to setting up Python, XAMPP with MySQL, and Django. Follow each step carefully to ensure a smooth installation and configuration process.


Setup Python

Step 1: Download Python
Go to the Python official website (https://www.python.org/downloads/)
Click on the download button to get the latest version of Python.
Once downloaded, run the installer.
Step 2: Install Python
During the installation process, make sure to check the box that says "Add Python to PATH".
Click on "Install Now" to proceed with the installation.
Follow the prompts to complete the installation.
Step 3: Verify Installation
Open the Command Prompt (cmd) or Terminal.
Type python --version and press Enter. You should see the Python version number.


Setup XAMPP and MySQL
Step 1: Download XAMPP
Go to the XAMPP official website (https://www.apachefriends.org/) 
Click on the download button for your operating system.
Step 2: Install XAMPP
Run the downloaded installer.
Follow the installation instructions and choose the components you want to install. Make sure to include MySQL.
Once the installation is complete, open the XAMPP Control Panel.
Step 3: Start Apache and MySQL
In the XAMPP Control Panel, click the "Start" button next to Apache.
Click the "Start" button next to MySQL.
Step 4: Configure MySQL
Open your web browser and go to http://localhost/phpmyadmin.
Create a new database by clicking on the "New" button on the left sidebar.
Enter a name for your database and click "Create".


Setup Django
Step 1: Install Django
Open the Command Prompt (cmd) or Terminal.
Type pip install django and press Enter. This will install the latest version of Django.
Step 2: Create a Django Project
In the Command Prompt (cmd) or Terminal, navigate to the directory where you want to create your Django project.
Type django-admin startproject projectname (replace projectname with your desired project name) and press Enter.
Navigate into the project directory by typing cd projectname.
Step 3: Configure Database Settings
Open the settings.py file located in your project directory.
Find the DATABASES section and update it to use MySQL:

Replace your_db_name, your_db_user, and your_db_password with the appropriate values.
Step 4: Install MySQL Client
In the Command Prompt (cmd) or Terminal, type pip install mysqlclient and press Enter.
Step 5: Migrate Database
In the Command Prompt (cmd) or Terminal, type python manage.py migrate and press Enter. This will apply to the initial database migrations.
Step 6: Run the Development Server
In the Command Prompt (cmd) or Terminal, type python manage.py runserver and press Enter.
Open your web browser and go to http://localhost:8000 to see your Django project running.
