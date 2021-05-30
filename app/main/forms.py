#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import User, Role
from flask_pagedown.fields import PageDownField



class EditProfileForm(FlaskForm):
    name = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能由字母，数字，点，下划线组成')])
    confirmed = BooleanField('已确认')
    role = SelectField('角色', coerce=int)
    name = StringField('昵称', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已经注册过')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('此用户名已经注册过')


class PostForm(FlaskForm):
    body = PageDownField("你现在有什么想法？", validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('提交')