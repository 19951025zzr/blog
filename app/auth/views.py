#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app.auth import auth
from flask import render_template,url_for,current_app,flash, redirect, request
from flask_login import login_required, current_user,login_user, logout_user
from app.auth.forms import RegistForm, LoginForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from app import db
from app.models import User
from app.email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint\
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data.lower()
                    )
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '请确认邮箱', 'auth/email/confirm', user=user, token=token)
        flash('您现在可以登陆了.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您已成功确认账户，谢谢')
    else:
        flash('确认链接已经无效 或者 过期')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '请确认你的邮件', 'auth/email/confirm', user=current_user, token=token)
    flash('一个新的确认邮件已发送到你的邮箱')
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        # 根据邮箱查用户是否存在，并且验证密码一致性
        if user and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('邮箱或密码无效.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已登出!')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('您已成功改密码')
            return redirect(url_for('main.index'))
        else:
            flash('填入密码无效')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '请重置密码', 'auth/email/reset_password', user=user, token=token)
            flash('一封带有重置密码说明的邮件已经发送到你的邮箱,请查收')
            return redirect(url_for('auth.login'))
        flash('输入的邮箱地址无效')
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('你的新密码已更新')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '更改邮箱', 'auth/email/change_email', user=current_user, token=token)
            flash('一封说明新的邮箱地址的邮件已经发送到你的邮箱')
            return redirect(url_for('main.index'))
        else:
            flash('密码错误')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('已经更改邮箱成功')
    else:
        flash('无效的请求')
    return redirect(url_for('main.index'))