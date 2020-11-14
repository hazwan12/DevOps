from flask import render_template, url_for, flash, redirect, request, abort
from devops import app, db, bcrypt
from devops.forms import RegistrationForm, LoginForm, BugForm, UpdateForm, CommentForm
from devops.models import User, Bug, Comment
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    bugs = Bug.query.all()
    return render_template("content/home.html", bugs=bugs)

@app.route("/aboutus")
def aboutus():
    return render_template("content/about.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')      
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                        role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('content/account.html', title='Account')

@app.route("/newbug", methods=['GET', 'POST'])
@login_required
def newbug():
    form = BugForm()
    if form.validate_on_submit():
        bug = Bug(summary=form.summary.data, product=form.product.data, platform=form.platform.data,
                    whatHappen=form.whatHappen.data, howHappen=form.howHappen.data,
                    shouldHappen=form.shouldHappen.data, status=form.status.default, priority=form.priority.default,
                    author=current_user)
        db.session.add(bug)
        db.session.commit()
        flash('Your bug report has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("content/newbug.html", title='New Bug', form=form, legend='Create Bug Report')

@app.route("/bug/<int:bug_id>")
def bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    comments = Comment.query.filter_by(bug_id=bug_id).all()
    return render_template('content/bug.html', title=bug.summary, bug=bug, comments=comments)

@app.route("/bug/<int:bug_id>/update", methods=['GET', 'POST'])
@login_required
def update_bug(bug_id):
    avail_developer_list = User.query.filter_by(role='Developer').all()
    avail_reviewer_list = User.query.filter_by(role='Reviewer').all()
    developer_list = [(i.id, i.username) for i in avail_developer_list]
    reviewer_list = [(i.id, i.username) for i in avail_reviewer_list]
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role == 'Reporter':
        abort(403)
    form = UpdateForm()
    form.assigned_to.choices = developer_list
    form.reviewed_by.choices = reviewer_list
    if form.validate_on_submit():
        bug.summary = form.summary.data
        bug.product = form.product.data
        bug.platform = form.platform.data
        bug.whatHappen = form.whatHappen.data
        bug.howHappen = form.howHappen.data
        bug.shouldHappen = form.shouldHappen.data
        bug.developer_id = form.assigned_to.data
        bug.reviewer_id = form.reviewed_by.data
        bug.priority = form.priority.data
        bug.status = form.status.data
        db.session.commit()
        flash('Bug report has been updated!', 'success')
        return redirect(url_for('bug', bug_id=bug.id))
    elif request.method == 'GET':
        form.summary.data = bug.summary
        form.product.data = bug.product
        form.platform.data = bug.platform
        form.whatHappen.data = bug.whatHappen
        form.howHappen.data = bug.howHappen
        form.shouldHappen.data = bug.shouldHappen
    return render_template("content/update.html", title='Update Bug Report', form=form,
        legend='Update Bug Report')

@app.route("/bug/<int:bug_id>/delete", methods=['POST'])
@login_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role == 'Reporter':
        abort(403)
    db.session.delete(bug)
    db.session.commit()
    flash('Bug report has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/bug/<int:bug_id>/start_working", methods=['POST'])
@login_required
def start_working(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role != 'Developer':
        abort(403)
    bug.status = 'Work in progress'
    db.session.commit()
    flash('Bug report status has been changed to WIP!', 'success')
    return redirect(url_for('home'))

@app.route("/bug/<int:bug_id>/pending_for_review", methods=['POST'])
@login_required
def submit_to_reviewer(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role != 'Developer':
        abort(403)
    bug.status = 'Pending for review'
    db.session.commit()
    flash('Bug report has been submitted to reviewer!', 'success')
    return redirect(url_for('home'))

@app.route("/bug/<int:bug_id>/back_to_developer", methods=['POST'])
@login_required
def back_to_developer(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role != 'Reviewer':
        abort(403)
    bug.status = 'Work in progress'
    db.session.commit()
    flash('Bug report has been assigned back to developer!', 'success')
    return redirect(url_for('home'))

@app.route("/bug/<int:bug_id>/close_bug", methods=['POST'])
@login_required
def close_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role != 'Reviewer':
        abort(403)
    bug.status = 'Done'
    db.session.commit()
    flash('Bug report has been closed!', 'success')
    return redirect(url_for('home'))

@app.route("/bug/<int:bug_id>", methods=['POST'])
@login_required
def post_comment(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    cmt = request.form
    comment = Comment(comment=cmt.get("comment"), bug_id=bug.id, username=current_user.username)
    db.session.add(comment)
    db.session.commit()
    flash('Commented!', 'success')
    return redirect(url_for('home'))