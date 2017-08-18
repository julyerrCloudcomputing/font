# -*- coding: utf-8 -*-
from os import path, remove
from flask import render_template, redirect, url_for, flash, session, request
from forms import Login_Form, Register_Form, Update_Form, Delete_Form, student_update_pwd_Form
from models import Users
from flask_login import login_user, logout_user, login_required
from flaskapp import app, db
from werkzeug import security
from werkzeug.utils import secure_filename


'''@app.after_request
def after_request(param):
    print request.args
    return param'''


@app.route('/')
def index():
    # print "session ==", session
    # print 'user_id' in session.keys()
    if 'user_id' in session.keys():  # 若已经登录
        # print session['user_id']
        if session['is_admin'] is False:  # 普通用户登录
            return render_template('ok.html', name=session['user_id'])
        else:  # 管理员账户登录
            return render_template('admin.html')
    form = Login_Form()
    return render_template('login.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.name.data).first()
        if user is not None and security.check_password_hash(user.password_hash, form.pwd.data):
            login_user(user)
            flash('登录成功')
            if user.is_admin is True:
                session['is_admin'] = True
                return render_template('admin.html')
            session['is_admin'] = False
            return render_template('ok.html', name=form.name.data)
        else:
            flash('用户名或密码错误')
            return render_template('login.html', form=form)


# 用户登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('is_admin')
    flash('你已退出登录')
    form = Login_Form()
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():  # 只有管理员才能注册用户
    if 'user_id' in session.keys() and session['is_admin'] is True:  # 是管理员登录
        form = Register_Form()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.name.data).first()
            if user is not None:
                flash('帐号'+form.name.data+'已存在，无法再次创建')
                return redirect(url_for('index'))
            user = Users(name=form.name.data, pwd=security.generate_password_hash(form.pwd.data))
            db.session.add(user)
            db.session.commit()
            db.session.close()
            flash('注册成功')
            return redirect(url_for('index'))  # url_for的参数是路由函数的名字
        return render_template('register.html', form=form)
    elif 'user_id' in session.keys() and session['is_admin'] is False:  # 普通用户登录
        # print session
        return render_template('ok.html', name=session['user_id'])
    else:  # 没有登录
        form = Login_Form()
        return render_template('login.html', form=form)


@app.route('/update_pwd', methods=['GET', 'POST'])
def update_pwd():  # 修改非管理员密码
    if 'user_id' in session.keys() and session['is_admin'] is True:  # 是管理员登录
        form = Update_Form()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.name.data).first()
            if user is None:
                flash('查无此人，请输入正确的用户名')
                return redirect(url_for('update_pwd'))
            elif user.is_admin:
                flash('不可修改管理员的密码')
                return redirect(url_for('update_pwd'))
            else:
                user.password_hash = security.generate_password_hash(form.pwd.data)
                db.session.commit()
                db.session.close()
                flash('修改成功')
                return redirect(url_for('index'))  # url_for的参数是路由函数的名字
        return render_template('update_pwd.html', form=form)
    elif 'user_id' in session.keys() and session['is_admin'] is False:  # 普通用户登录
        # print session
        return render_template('ok.html', name=session['user_id'])
    else:  # 没有登录
        form = Login_Form()
        return render_template('login.html', form=form)


@app.route('/student_update_pwd', methods=['GET', 'POST'])
def student_update_pwd():
    if 'user_id' in session.keys() and session['is_admin'] is False:  # 普通用户登录
        form = student_update_pwd_Form()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=session['user_id']).first()
            user.password_hash = security.generate_password_hash(form.new_pwd.data)
            db.session.commit()
            db.session.close()
            flash('修改成功')
            return redirect(url_for('logout'))  # redirect(url_for('index'))
        return render_template('student_update_pwd.html', form=form)
    elif 'user_id' in session.keys() and session['is_admin'] is True:
        return render_template('admin.html')
    else:
        form = Login_Form()
        return render_template('login.html', form=form)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'user_id' in session.keys() and session['is_admin'] is True:  # 是管理员登录
        form = Delete_Form()
        users = Users.query.filter_by(is_admin='0')
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.name.data).first()
            if user is None:
                flash('查无此人，请输入正确的用户名')
                return redirect(url_for('delete'))
            else:
                db.session.delete(user)
                db.session.commit()
                db.session.close()
                flash('删除成功')
                return redirect(url_for('delete'))  # url_for的参数是路由函数的名字
        return render_template('delete.html', form=form, users=users)
    elif 'user_id' in session.keys() and session['is_admin'] is False:  # 普通用户登录
        # print session
        return render_template('ok.html', name=session['user_id'])
    else:  # 没有登录
        form = Login_Form()
        return render_template('login.html', form=form)


@app.route('/batch_import', methods=['GET', 'POST'])
def batch_import():
    if 'user_id' in session.keys() and session['is_admin'] is True:  # 是管理员登录
        if request.method == 'POST':
            f = request.files['file']
            if f.filename == '':
                flash('请选择一个csv文件')
                return redirect(url_for('batch_import'))
            basepath = path.abspath(path.dirname(__file__))
            f.filename = 'student.csv'
            upload_path = path.join(basepath, 'static/uploads', secure_filename(f.filename))
            f.save(upload_path)
            flash('上传名单成功')
            ret = create_accounts()
            if ret == 'ok':
                flash('创建账户成功')
            else:
                flash('创建失败')
            return redirect(url_for('batch_import'))
        return render_template('batch_import.html')
    elif 'user_id' in session.keys() and session['is_admin'] is False:  # 普通用户登录
        # print session
        return render_template('ok.html', name=session['user_id'])
    else:  # 没有登录
        form = Login_Form()
        return render_template('login.html', form=form)


def create_accounts():
    basepath = path.abspath(path.dirname(__file__))
    student_accounts = path.join(basepath, 'static/uploads', 'student.csv')
    with open(student_accounts, 'r') as file:
        for line in file:
            linelst = line.split(',')
            username = linelst[0]
            password = linelst[1]
            user = Users.query.filter_by(username=username).first()
            if user is not None:
                flash(username+' 已存在')
                continue
            user = Users(name=username, pwd=security.generate_password_hash(password[:-2]))
            # 文件中每一行末尾都有两个不可见字符/r/n
            db.session.add(user)
            db.session.commit()
            db.session.close()
    remove(student_accounts)
    return 'ok'
