from orator.seeds import Seeder

class RoleTableSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.db.table('roles').insert({
            'name': 'admin',
            'description': 'The admin controls all!!'
        })
