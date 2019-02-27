from orator.seeds import Seeder
from orator.orm import Factory
from werkzeug.security import generate_password_hash

class UserTableSeeder(Seeder):

    factory = Factory()

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(User, self.users_factory)

        # Add admin user
        self.db.table('users').insert({
            'username': 'admin',
            'email': 'admin@gmail.com',
            'roles': [1],
            'password_hash': generate_password_hash('admin')
        })
        self.factory(User, 100).create()

        def users_factory(faker):
            return {
                'username': faker.name(),
                'email': faker.email(),
                'password_hash': generate_password_hash(faker.text())
            }
