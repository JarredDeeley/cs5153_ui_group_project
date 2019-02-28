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
yarn s/npm s      # To start flask server
```

**For Interactive Shell**
```bash
flask shell
# or
yarn shell
```

**To see routes**

Still working on this so for now to see routes
```bash
python
from app import app
app.url_map
```
```bash
flask list-routes
```

Logging into admin interface

* username: admin
* password: admin
* email: admin@example.com

Logging into as normal user

* username: <Can check for username after logging into admin>
* password: Password1234
* email: <Can check for user email after logging into admin>
