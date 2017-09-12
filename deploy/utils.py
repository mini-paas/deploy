# coding=utf-8
from nginx_deploy.deploy_conf import *
from Crypto.Cipher import AES
from tempfile import NamedTemporaryFile
from django.core.servers.basehttp import FileWrapper
from django.utils.http import urlquote
from django.views.generic import *
from django.http import JsonResponse, QueryDict
from bkstorages.backends.rgw import RGWBoto3Storage
from django.core.files import File
from django.views.generic import DetailView, ListView, View, CreateView , UpdateView, DeleteView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from serializers import *
from rest_framework import viewsets
import crypt
from binascii import b2a_hex, a2b_hex
import hashlib
import random
import string
import subprocess
import urllib
import zipfile
import os


BASE_DIR = '/data/BK_App_FilePool/yw_deploy/bkdownload'
FileUploadDir_local = '%s/uploads' % BASE_DIR
FileUploadDir = '/uploads'
MaxUploadFiles = 6
storage = RGWBoto3Storage()


def random_str(length):
    source = string.ascii_lowercase + string.digits
    rand_str = random.sample(source, length)
    return ''.join(rand_str)


def get_asset_info(i, **args):
    infr,infor = [], {}

    if isinstance(args['passwdold'], list):
        for ia in args['passwdold']:
            infor['password'] = ia
            infor['ip'] = i
            infor['username'] = args['user']
            infor['port'] = 36000
            infr.append(infor)
            infor = {}
    else:
        infor['password'] = args['passwdold']
        infor['ip'] = i
        infor['username'] = args['user']
        infor['port'] = 36000
        infr.append(infor)

    return infr


def gen_resource(i, **args):
    res = []

    info = get_asset_info(i, **args)
    res.extend(info)

    return res


class PyCrypt(object):

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    @staticmethod
    def gen_rand_pass(length=16, especial=False):

        salt_key = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        symbol = '!@$%^&*()_'
        salt_list = []
        if especial:
            for i in range(length - 4):
                salt_list.append(random.choice(salt_key))
            for i in range(4):
                salt_list.append(random.choice(symbol))
        else:
            for i in range(length):
                salt_list.append(random.choice(salt_key))
        salt = ''.join(salt_list)
        return salt

    @staticmethod
    def md5_crypt(string):
        return hashlib.new("md5", string).hexdigest()

    @staticmethod
    def gen_sha512(salt, password):
        return crypt.crypt(password, '$6$%s$' % salt)

    def encrypt(self, passwd=None, length=32):
        if not passwd:
            passwd = self.gen_rand_pass()
        cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
        try:
            count = len(passwd)
        except TypeError:
            raise ServerError('Encrypt password error, TYpe error.')

        add = (length - (count % length))
        passwd += ('\0' * add)
        cipher_text = cryptor.encrypt(passwd)
        return b2a_hex(cipher_text)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
        try:
            plain_text = cryptor.decrypt(a2b_hex(text))
        except TypeError:
            raise ServerError('Decrypt password error, TYpe error.')
        return plain_text.rstrip('\0')


CRYPTOR = PyCrypt('pqweasdzxc124214')


def bash(cmd):
    return subprocess.call(cmd, shell=True)

