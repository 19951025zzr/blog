#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import configparser


section = "Default"
BASEPATH = os.path.abspath('conf.ini')
conf = configparser.ConfigParser()
conf.read_file(open(BASEPATH))
admin_email = conf.get(section, "FLASKY_ADMIN")
email_password = conf.get(section, "MAIL_PASSWORD")


class Config:
    SECRET_KEY = 'secret_key'
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'blog'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = admin_email
    MAIL_PASSWORD = email_password
    FLASKY_MAIL_SUBJECT_PREFIX = '[博客]'
    FLASKY_MAIL_SENDER = '博客 zzr'
    FLASKY_ADMIN = admin_email
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


