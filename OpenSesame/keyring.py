"""
GNOME-keyring intergration wrapper. Python GNOME-keyring automagically saves 
queries into secured memory. This implementation is mindful to not remove
secrets into unsecured Python memory.
    
quick search descriptions of keys loaded into secure memory
http://developer.gnome.org/gnome-keyring/stable/gnome-keyring-Non-pageable-Memory.html
"""

import gnomekeyring as gkr
import time
import password

class OpenKeyring(object):
    def __init__(self, keyring="opensesame"):
        """Get OpenSesame keyring name stored in gconf
        """
        self.keyring = keyring
        self.default_keyring = gkr.get_default_keyring_sync()
        if self.keyring not in gkr.list_keyring_names_sync():
            self.first_time_setup()
        self.unlock_keyring()

    def unlock_keyring(self):
        info = gkr.get_info_sync(self.keyring)
        if info.get_is_locked():
            found_pos = self._auto_unlock_key_position()
            item_info = gkr.item_get_info_sync(self.default_keyring, found_pos)
            gkr.unlock_sync(self.keyring, item_info.get_secret()) 

    def first_time_setup(self):
        """First time running Open Sesame? 
        
        Create keyring and an auto-unlock key in default keyring. Make sure
        these things don't already exist.
        """
        if not self._auto_unlock_key_position():
            pw, phonetic  = password.create_passwords()[0]
            desc = "opensesame"
            attrs = {'application': desc, 'phonetic': phonetic}
            gkr.item_create_sync(self.default_keyring
                                ,gkr.ITEM_GENERIC_SECRET
                                ,desc
                                ,attrs
                                ,pw
                                ,True)
        found_pos = self._auto_unlock_key_position()
        item_info = gkr.item_get_info_sync(self.default_keyring, found_pos)
        gkr.create_sync(self.keyring, item_info.get_secret())

    def _auto_unlock_key_position(self):
        """Find the open sesame password in the default keyring
        """
        found_pos = None
        default_keyring_ids = gkr.list_item_ids_sync(self.default_keyring)
        for pos in default_keyring_ids:
            item_attrs = gkr.item_get_attributes_sync(self.default_keyring, pos)
            app = 'application'
            if item_attrs.has_key(app) and item_attrs[app] == "opensesame":
                found_pos = pos
                break
        return found_pos
    
    def get_password(self, pos):
        """Don't actually return the password though, keep it in secure memory
        by returning the item
        """
        return gkr.item_get_info_sync(self.keyring, pos)

    def get_position_searchable(self):
        """Return dict of the position and corrasponding searchable str
        """
        ids = gkr.list_item_ids_sync(self.keyring)
        position_searchable = {}
        for i in ids:
            item_attrs = gkr.item_get_attributes_sync(self.keyring, i)
            position_searchable[i] = item_attrs['searchable'] 
        return position_searchable

    def _match_exists(self, searchable):
        """Make sure the searchable description doesn't already exist
        """
        position_searchable = self.get_position_searchable()
        for pos,val in position_searchable.iteritems():
            if val == searchable:
                return pos
        return False

    def save_password(self, password, **attrs):
        """Save the new password, but don't wipe out an older version of 
        searchable
        """
        pos_of_match = self._match_exists(attrs['searchable'])
        print pos_of_match
        if pos_of_match:
            old_password_date = 'old_password_' + time.strftime("%Y/%m/%d")
            attrs[old_password_date] = self.get_password(pos_of_match).get_secret()
            gkr.item_delete_sync(self.keyring, pos_of_match)
        desc = attrs['searchable']
        pos = gkr.item_create_sync(self.keyring
                                  ,gkr.ITEM_GENERIC_SECRET
                                  ,desc
                                  ,attrs
                                  ,password
                                  ,True)
        return pos
