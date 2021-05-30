#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User


class RegistForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('账号', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须匹配')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('提交注册')

    # 校验邮箱地址是否唯一
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('邮箱已注册.')

    # 校验账号是否唯一
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('账号已注册.')

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登陆')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须匹配')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    submit = SubmitField('重设密码')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须匹配')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('重设密码')


class ChangeEmailForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField('输入密码', validators=[DataRequired()])
    submit = SubmitField('更新邮箱')

    # 校验邮箱地址是否唯一
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('邮箱已注册.')