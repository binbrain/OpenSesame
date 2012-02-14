from OpenSesame.keyring import OpenKeyring 
import gnomekeyring as gkr

class TestKeyRing(object):

    def setup(self):
        self.keyring = "test"
        self._test_first_time()

    def teardown(self):
        gkr.delete_sync(self.keyring)

    def _load_passwords(self):
        self.openkeyring.save_password(password="Awawmak9", searchable="twitter", phonetic="Aw-aw-mak-NINE")
        self.openkeyring.save_password(password="AjtievTyz8", searchable="facebook", phonetic="Aw-aw-mak-NINE")
        self.openkeyring.save_password(password="Exoawb6fleOn", searchable="ssh dollars", phonetic="Aw-aw-mak-NINE")
        self.openkeyring.save_password(password="Ganocuk2", searchable="ssh sheckels", phonetic="Aw-aw-mak-NINE")
        self.openkeyring.save_password(password="GeejUnvoj8", searchable="gmail", phonetic="Aw-aw-mak-NINE")

    def _test_first_time(self):
        assert(self.keyring not in gkr.list_keyring_names_sync())
        self.openkeyring = OpenKeyring(self.keyring)
        assert(self.keyring in gkr.list_keyring_names_sync())

    def test_save_password(self):
        pos = self.openkeyring.save_password(password="Awawmak9", searchable="twitter", phonetic="Aw-aw-mak-NINE")
        attrs = gkr.item_get_attributes_sync(self.keyring, pos)
        assert(attrs.has_key('phonetic'))
        assert(attrs['phonetic'] == "Aw-aw-mak-NINE")
        info = gkr.item_get_info_sync(self.keyring, pos)
        assert(info.get_display_name() == "twitter")
        assert(info.get_secret() == "Awawmak9")

    def test_overwrite_password(self):
        """Creating a new key with an already existing searchable
        overwrites the old key, but saves the old password in the 
        new keys attributes just in case
        """
        pass

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
