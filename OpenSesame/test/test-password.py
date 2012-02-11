from OpenSesame import password

def test_create_passwords():
    passwords = password.create_passwords()
    assert(len(passwords) == 6)
