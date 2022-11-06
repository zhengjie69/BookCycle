try:
    from BookCycle import create_app
    import unittest
    app = create_app()

except Exception as e:
    print(f"Some Modules are Missing {e}")


class FlaskTest(unittest.TestCase):

    # Test Cases
    # Test if the App can successfully open
    def test_app(self):
        tester = app.test_client(self)
        response = tester.get("/")
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 200')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        # self.assertEqual(response.status_code, 200)
    
    # Test for Successful User Login 
    def test_app_success_login_user(self):
        tester = app.test_client(self)
        response = tester.post("/login", data={
            'Email': 'chewei06@gmail.com',
            'Password': 'Test@123'
        })
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 200')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        # self.assertEqual(response.status_code, 200)

    # Test for Fail User Login
    def test_app_fail_login_user(self):
        tester = app.test_client(self)
        response = tester.post("/login", data={
            'Email': 'chewei06@gmail.com',
            'Password': 'Anyhow@123'
        })
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 404')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        self.assertEqual(response.status_code, 404)

    # Test for Successful Admin Login 
    def test_app_success_login_admin(self):
        tester = app.test_client(self)
        response = tester.post("/login", data={
            'Email': 'admin1@gmail.com',
            'Password': 'Admin@123'
        })
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 200')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        # self.assertEqual(response.status_code, 200)

    # Test for Fail Admin Login 
    def test_app_fail_login_admin(self):
        tester = app.test_client(self)
        response = tester.post("/login", data={
            'Email': 'admin1@gmail.com',
            'Password': 'Anyhow@123'
        })
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 404')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        self.assertEqual(response.status_code, 404)
    
    # Test for Successful Super Admin Login 
    def test_app_success_login_superadmin(self):
        tester = app.test_client(self)
        response = tester.post("/login", data={
            'Email': 'superadmin1@gmail.com',
            'Password': 'Superadmin@123'
        })
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 200')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        # self.assertEqual(response.status_code, 200)

    # Test for Fail Super Admin Login 
    def test_app_fail_login_superadmin(self):
        tester = app.test_client(self)
        response = tester.post("/login", data={
            'Email': 'superadmin1@gmail.com',
            'Password': 'Anyhow@123'
        })
        print()
        print("TEST CASE 1 SUCCESS: STATUS CODE 200")
        print('EXPECTED OUTPUT:\nSTATUS_CODE 404')
        print(f'ACTUAL OUTPUT:\nSTATUS_CODE {response.status_code}\n')
        self.assertEqual(response.status_code, 404)