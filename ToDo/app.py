from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint
from dotenv import load_dotenv
from flask.globals import session
from flask_login.login_manager import LoginManager
from flask_login.utils import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from ToDo.forms import UserForm, LoginForm, TodoForm
from . import app, db
from .models import User, Todo

load_dotenv()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('login'))


@app.route('/todo_list/delete/<int:id>')
@login_required
def mark_complete_todo(id):
    """
    marking a todo item as complete
    """
    todo_to_delete = Todo.query.filter_by(id=id).first()
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
    return redirect(url_for('todo_list', status='Deleted Item successfully'))


@app.route('/todo_list/mark_complete/<int:id>')
@login_required
def delete_todo(id):
    """
    deleting a todo item
    """
    mark_complete_item = Todo.query.filter_by(id=id).first()
    if mark_complete_item:
        mark_complete_item.completed = True
        db.session.commit()
    return redirect(url_for('todo_list', status='Todo Marked Complete'))


@app.route('/todo_list/edit/<int:id>')
@login_required
def edit_todo(id):
    """
    editing a todo item
    """
    todo_to_edit = Todo.query.filter_by(id=id).first()
    if todo_to_edit:
        return redirect(url_for('todo_list',
                                id=id,
                                title=todo_to_edit.title,
                                note=todo_to_edit.note,
                                due_date=str(todo_to_edit.due_date.date()),
                                status='Edit mode Activated'),
                        )

    return redirect(url_for('todo_list'), status='This todo does not exist')


@app.route('/todo_list', methods=['GET', 'POST'])
@login_required
def todo_list():
    """
    rendering the todo items page

    """
    # clearing all the flashes
    flashes = session.get('_flashes')
    if flashes:
        flashes.clear()

    form = TodoForm()

    # flashing the status
    if request.args.get('status'):
        flash(request.args.get('status'))

    if form.validate_on_submit():
        if request.args.get('id'):
            # updating a todo item with id
            todo = Todo.query.filter_by(id=request.args.get('id')).first()
            todo.title = form.title.data
            todo.note = form.note.data
            todo.due_date = form.due_date.data
            status = 'Todo Updated!!'
        else:
            # adding a new todo item
            todo = Todo(user_id=current_user.id,
                        title=form.title.data,
                        note=form.note.data,
                        due_date=form.due_date.data,
                        )
            db.session.add(todo)
            status = 'Todo Added!!'
        db.session.commit()
        return redirect(url_for('todo_list'))

    if request.args.get('title') \
            and request.args.get('note') \
            and request.args.get('due_date'):
        form.title.data = request.args.get('title')
        form.note.data = request.args.get('note')

    todos = Todo.query.filter_by(user_id=current_user.id)

    context = {
        "todo_list": list(todos)
    }

    return render_template('todo_list.html', form=form, context=context)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    this is the login api, creating a session for proper login logout functionality
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hashed, form.password.data):
                login_user(user)
                flash("Login SUCCESS")
                return redirect(url_for('todo_list'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    registering a user with hashed password
    """
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password.data, "sha256")
            user = User(username=form.username.data, email=form.email.data, password_hashed=hashed_pw)
            # creating a valid user
            db.session.add(user)
            db.session.commit()
        else:
            # user already exists
            user = User.query.filter_by(email=form.email.data).first()
            return render_template("register.html", form=form, user=user)

        # clearing the form, i.e. we could have also made a redirect to the same page
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''

        flash("User Added Successfully!")
        return render_template("register.html", form=form, user=user)

    user = User.query.filter_by(email=form.email.data).first()
    return render_template("register.html", form=form, user=user)


if __name__ == "__main__":
    app.run(port=3000)
