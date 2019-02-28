# Clean Code

**Usage: Dev port on 5000**

**Install [yarn](https://yarnpkg.com/lang/en/docs/install/#debian-stable) package manager or nodejs package manager (npm)**

```bash
#inside app folder
pip install virtualenv
source venv/bin/activate
flask db upgrade   # To do database migrations
yarn              # To install node packages
yarn seed         # To populate database
yarn start/npm start
```

**For Interactive Shell**
```bash
flask shell
# or
yarn s
```

Logging into admin there is an admin user
* username: admin
* password: admin
* email: admin@example.com
