from OpenSesame.keyring import OpenKeyring 
import gnomekeyring as gkr

import mock

class TestKeyRing(object):

    def setup(self):
        self.keyring = "test_openseame"
        self._first_time()

    def teardown(self):
        gkr.delete_sync(self.keyring)

    def _load_passwords(self):
        self.openkeyring.save_password(password="Awawmak9", searchable="twitter")
        self.openkeyring.save_password(password="AjtievTyz8", searchable="facebook")
        self.openkeyring.save_password(password="Exoawb6fleOn", searchable="ssh dollars")
        self.openkeyring.save_password(password="Ganocuk2", searchable="ssh sheckels")
        self.openkeyring.save_password(password="GeejUnvoj8", searchable="gmail")

    def _first_time(self):
        assert(self.keyring not in gkr.list_keyring_names_sync())
        self.openkeyring = OpenKeyring(self.keyring)
        assert(self.keyring in gkr.list_keyring_names_sync())

    def test_save_password(self):
        pos = self.openkeyring.save_password(password="Awawmak9", searchable="twitter")
        info = gkr.item_get_info_sync(self.keyring, pos)
        assert(info.get_display_name() == "twitter")
        assert(info.get_secret() == "Awawmak9")

    @mock.patch('time.time', mock.Mock(return_value=1345315249))
    def test_overwrite_password(self):
        """Creating a new key with an already existing searchable
        overwrites the old key, but saves the old password in a 
        new key with the prepended date
        """
        self.openkeyring.save_password(password="password1", searchable="blogA")
        self.openkeyring.save_password(password="password2", searchable="blogA")
        assert(len(gkr.list_item_ids_sync(self.keyring)) == 2)

    def test_get_position_searchable(self):
        self._load_passwords()
        id_searchable = self.openkeyring.get_position_searchable()
        assert(len(id_searchable) == 5)

    def test_match_exists(self):
        self._load_passwords()
        assert(not self.openkeyring._match_exists("Nothing"))
        assert(self.openkeyring._match_exists("twitter"))

    def test_unlock_keyring(self):
        gkr.lock_sync(self.keyring)
        info = gkr.get_info_sync(self.keyring)
        assert(info.get_is_locked())
        self.openkeyring.unlock_keyring()
        info = gkr.get_info_sync(self.keyring)
        assert(not info.get_is_locked())
