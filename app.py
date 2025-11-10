from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-me"   # change this in real project

# --- Jinja filter to format times ---
@app.template_filter('convert_time')
def convert_time(value):
    try:
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value)
        elif isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value)
            except Exception:
                return value
        else:
            return str(value)
        return dt.strftime("%b %d, %Y %I:%M %p")
    except Exception:
        return str(value)

# --- Fake in-memory data store ---
# now each post has a comments list
POSTS = [
    {
        "user": "Alice",
        "time": datetime.now(),
        "text": "Hello, CampusTalk!",
        "comments": []
    },
]

# ---------------- ROUTES ----------------

# show login page
@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

# handle login form submit
@app.route('/login', methods=['POST'])
def login_handler():
    button = request.form.get('type')  # in case you have 2 buttons
    if button == 'Create':
        return redirect(url_for('create_account'))

    # get username from login form
    username = request.form.get("username", "").strip()
    if not username:
        username = "Guest"

    session["username"] = username
    return redirect(url_for('home'))

# create-account page
@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first = request.form.get("first_name", "").strip()
        last = request.form.get("last_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        major = request.form.get("major", "").strip()
        interests = request.form.get("interests", "").strip()
        year = request.form.get("year", "").strip()

        # store in session for now (no db yet)
        session["first_name"] = first
        session["last_name"] = last
        session["username"] = username or "Guest"
        session["major"] = major
        session["interests"] = interests
        session["year"] = year

        # DON'T do this in real apps, hash it instead
        session["password"] = password

        return redirect(url_for('home'))

    return render_template('create.html')

# main feed page
@app.route('/home', methods=['GET'])
def home():
    username = session.get("username", "Guest")
    first_name = session.get("first_name")
    return render_template(
        'feed.html',
        posts=POSTS,
        username=username,
        first_name=first_name
    )

# add a new post
@app.route('/post', methods=['POST'])
def post():
    text = (request.form.get('post') or '').strip()
    if text:
        username = session.get("username", "Guest")
        POSTS.insert(0, {
            "user": username,
            "time": datetime.now(),
            "text": text,
            "comments": []      # new posts can be commented on
        })
    return redirect(url_for('home'))

# add a comment to a post
@app.route('/comment', methods=['POST'])
def comment():
    post_index = request.form.get("post_index")
    comment_text = (request.form.get("comment_text") or "").strip()
    username = session.get("username", "Guest")

    if post_index is not None and comment_text:
        i = int(post_index)
        if 0 <= i < len(POSTS):
            POSTS[i]["comments"].append({
                "user": username,
                "time": datetime.now(),
                "text": comment_text
            })

    return redirect(url_for('home'))

# logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

