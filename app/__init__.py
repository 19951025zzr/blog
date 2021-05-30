#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
初始化应用
"""
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config
from flask_pagedown import PageDown

login_manager = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()

# 将应用app包下面的模块全部导入此文件，返回应用实例
# 不同模块的蓝本注册到应用上
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    mail.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
