from flask import Flask, redirect, render_template, session
from models import db, connect_db, User, Feedback
from forms import UserForm, UserLoginForm, FeedbackForm
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///feedback_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "hello"

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route("/")
def index():
    return redirect("/register")

@app.route("/register", methods=["POST", "GET"])
def register_page():
    """form that creates a new user."""
    form = UserForm()

    if form.validate_on_submit():
        un = form.username.data
        p = form.password.data
        em = form.email.data
        fn = form.first_name.data
        ln = form.last_name.data

        user = User.register(un, p, em, fn, ln)
        
        db.session.add(user)
        db.session.commit()
        
        session['username'] = user.username
        return redirect(f"/users/{user.username}")
    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login_page():
    """form that logs in user"""
    form = UserLoginForm()

    if form.validate_on_submit():
        un = form.username.data
        p = form. password.data

        user = User.authenticate(un, p)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password"]
    else:
        return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")

    return redirect("/")

@app.route("/users/<username>")
def secret(username):
    if 'username' in session:
        user = User.query.get_or_404(username)

        return render_template("user.html", user=user)
    else:
        return redirect("/register")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if 'username' in session:
        if session['username'] == username:
            user = User.query.filter(User.username == username).first()
            for feedback in user.feedback:
                db.session.delete(feedback)
            db.session.delete(user)
            db.session.commit()
            session.pop("username")
            redirect("/")
        else:
            return redirect(f"/users/{username}")
    else:
       return redirect(f"/users/{username}")

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def feedback_page(username):
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("add_feedback.html", form=form)
    
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Edit feedback form"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if 'username' in session:
        if session['username'] == feedback.username:
            
            if form.validate_on_submit():
                feedback.title = form.title.data
                feedback.content = form.content.data

                db.session.commit()

                return redirect(f"/users/{feedback.username}")
            else:
                return render_template("edit_feedback.html", form=form)
    return redirect("/")
    
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""
    feedback = Feedback.query.get_or_404(feedback_id)
    
    if 'username' in session:
        if session['username'] == feedback.username:
            db.session.delete(feedback)
            db.session.commit()

            return redirect(f"/users/{feedback.username}")
    else:
        return redirect("/")

