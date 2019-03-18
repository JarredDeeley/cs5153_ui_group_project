# Clean Code

**Usage: Dev port on 5000**

**Install [yarn](https://yarnpkg.com/lang/en/docs/install/#debian-stable) package manager or nodejs package manager (npm)**

**Create virtual environment**
```bash
# If using python 3
python3 -m venv venv
# if using python 3.4 or less
virtualenv venv

source venv/bin/activate
pip install -r requirements.txt
```

**Using virtual environment**
```bash
#inside app folder
source venv/bin/activate
flask db upgrade   # To do database migrations
yarn              # To install node packages
yarn seed         # To populate database
yarn s/npm s      # To start flask server
```

**For Interactive Shell**
```bash
flask shell
# or
yarn shell
```

**To see routes**
```bash
flask list-routes
or
yarn routes
```

**After adding new libs**

Be sure to update the requirements.txt
```bash
pip freeze > requirements.txt
```
Logging into admin interface

* username: admin
* password: admin
* email: admin@example.com

Logging into as normal user

* username: Can check for username after logging into admin interface
* password: Password1234
* email: Can check for user email after logging into admin interface
