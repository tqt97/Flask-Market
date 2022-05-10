from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    selling_form = SellItemForm()
    purchase_form = PurchaseForm()
    if request.method == 'POST':
        # Purchase item logic
        purchased_item = request.form.get('purchased_item')
        if p_item_object := Item.query.filter_by(name=purchased_item).first():
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    f'You have purchased {p_item_object.name} for {p_item_object.price} $.', category='success')
            else:
                flash('You do not have enough money to purchase this item.',
                      category='danger')
        # Sell the item logic
        sold_item = request.form.get('sold_item')
        if s_item_object := Item.query.filter_by(name=sold_item).first():
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    f'You have sold {s_item_object.name} for {s_item_object.price} $.', category='success')
            else:
                flash(
                    f'Something went wrong with the item {s_item_object.name}!', category='danger')
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

    if request.method == 'GET':
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              password=form.password1.data, email_address=form.email_address.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account created successfully.You are logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_hash(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'You have successfully logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Invalid username or password', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', category='success')
    return redirect(url_for('index'))
