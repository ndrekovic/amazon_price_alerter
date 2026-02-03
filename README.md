# Amazon Price Alerter (in Progress)

The amazon price alerter allows the user to create a list of products and send a email if the product's
current price is below a user-defined desired price.

## Features

- Track prices of Amazon products
- Send email alerts when price drops below target
- Easy web interface to manage tracked products

# 💻 Tech Stack:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-yellow?style=for-the-badge&logo=JavaScript)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

## Installations

1. Clone the repository:
   ```bash
   git clone https://github.com/ndrekovic/amazon_price_alerter.git
   ```

2. Install a virtual environment to work on and activate it (recommended):
   ```bash
   python3 -m venv <venv_name>
   source <venv_name>/bin/activate
   ```

3. Install the libraries/packages/modules required to run the project:
   ```bash
   pip install -r requirements.txt
   ```

4. Environment Variables:
   Create a `.env` file in the project root with:
   ```bash 
   EMAIL_USER=your@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

5. Run database migrations (run after every change in models.py):
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. Start the developmemt server to run the project (optional: port):
   ```bash
   python3 manage.py runserver # default port 8000
   python3 manage.py runserver 8080 # custom port
   ```

7. 📧 Gmail Setup
    1. Enable 2FA in Google Account
    2. Create App Password
    3. Use App Password in .env

   Link: https://myaccount.google.com/apppasswords


8. Open web browser and type:
   ```bash
   http://127.0.0.1:8000/
   or
   http://127.0.0.1:<port>/    (if you use a custom port)
   ```

### Cron Setup

1. Add cron job
   ```bash
   crontab -e
   ```

2. Insert
   ```bash
   */30 * * * * cd /path/to/project && source venv/bin/activate && python manage.py update_prices >> cron.log 2>&1
   ```

3. Check jobs
   ```bash
   crontab -l
   ```

4. Logs
   ```bash
   cron.log
   ```

### Run Tests

Run tests for all Django test files

   ```bash
   python manage.py test
   ```

### Project Structure

   ```bash
   amazon_price_alerter/
    ├─ products/
    ├─ venv/
    ├─ manage.py
    ├─ cron.log
   ```

### Security

   ```bash   
   - Never commit `.env` or any sensitive credentials
   - Use Gmail App Passwords, not your real password
   - Keep `venv/` and `node_modules/` out of git
   ```

### 🚀 Future Improvements / ToDo List

- Make image backgrounds transparent
- Make Dashboad prettier (functionality first)
- Add more tests for edge cases
- Dockerize the application for easier deployment
