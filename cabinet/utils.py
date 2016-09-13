#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import os
import nacl.utils

from nacl.secret import SecretBox

from argon2 import hash_password_raw


class CryptoHelper:
    def _fix_salt(self, salt):
        # if salt is too short, lenghten it
        while len(salt) < 8:
            salt = salt * 2

        # salt needs to be bytes
        return bytes(salt, 'utf-8')

    def encrypt(self, data, password, salt):
        salt = self._fix_salt(salt)
        key = hash_password_raw(password, hash_len=32, salt=salt)
        box = SecretBox(key)
        nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        encrypted_data = box.encrypt(data, nonce,
                                     encoder=nacl.encoding.Base64Encoder)

        return encrypted_data

    def decrypt(self, data, password, salt):
        salt = self._fix_salt(salt)
        key = hash_password_raw(password, hash_len=32, salt=salt)
        box = SecretBox(key)
        data = box.decrypt(data, encoder=nacl.encoding.Base64Encoder)

        return data


def mkdir_p(path):
    """
    Creates the path and all the intermediate directories that don't
    exist

    Might raise OSError

    :param path: path to create
    :type path: str
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
