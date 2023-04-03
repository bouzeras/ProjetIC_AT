import unittest
from app import app, db, Groupe, Utilisateur

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_group(self):
        data = {
            'nom': 'Test Group',
            'description': 'This is a test group',
            'membres': '4',
            'last_group_config': 'LAST_MIN'
        }
        response = self.app.post('/form_group', data=data)
        self.assertEqual(response.status_code, 302)

        group = Groupe.query.filter_by(nom='Test Group').first()
        self.assertIsNotNone(group)
        self.assertEqual(group.nom, 'Test Group')
        self.assertEqual(group.description, 'This is a test group')
        self.assertEqual(group.membres, 'Utilisateur 1-Utilisateur 2-Utilisateur 3-Utilisateur 4')

        users = Utilisateur.query.filter_by(groupe_id=group.id).all()
        self.assertEqual(len(users), 4)
        self.assertEqual(users[0].nom, 'Utilisateur 1')
        self.assertEqual(users[1].nom, 'Utilisateur 2')
        self.assertEqual(users[2].nom, 'Utilisateur 3')
        self.assertEqual(users[3].nom, 'Utilisateur 4')

    def test_join_random_group(self):
        group1 = Groupe('Test Group 1', 'This is a test group', 'Utilisateur 1-Utilisateur 2-Utilisateur 3', '', False)
        group2 = Groupe('Test Group 2', 'This is another test group', 'Utilisateur 4-Utilisateur 5', '', False)
        group3 = Groupe('Test Group 3', 'This is a third test group', 'Utilisateur 6', '', False)
        db.session.add_all([group1, group2, group3])
        db.session.commit()

        # Test joining a random group with more than two members
        response = self.app.get('/join_random_group')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/group_list')

        group = Groupe.query.filter_by(nom='Test Group 1').first()
        self.assertIsNotNone(group)
        self.assertEqual(group.membres, 'Utilisateur 2-Utilisateur 3')

        # Test joining a random group with two members
        response = self.app.get('/join_random_group')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/group_list')

        group = Groupe.query.filter_by(nom='Test Group 2').first()
        self.assertIsNone(group)

        # Test joining a random group with one member
        response = self.app.get('/join_random_group')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/group_list')

        group = Groupe.query.filter_by(nom='Test Group 3').first()
        self.assertIsNotNone(group)
        self.assertEqual(group.membres, 'Utilisateur 6')

if __name__ == '__main__':
    unittest.main()
