from flask import Flask, render_template, request, redirect, url_for, session, abort
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
POSTS = [
    {
        "user": "Alice",
        "time": datetime.now(),
        "text": "Hello, CampusTalk!",
        "comments": [],
        "votes": {}   # username -> +1 / -1
    },
]

# --- Voting helper functions for Jinja ---
def get_post_score(post):
    votes = post.get("votes") or {}
    return sum(votes.values())

def get_comment_score(comment):
    votes = comment.get("votes") or {}
    return sum(votes.values())

def get_post_user_vote(post, username):
    votes = post.get("votes") or {}
    return votes.get(username, 0)

def get_comment_user_vote(comment, username):
    votes = comment.get("votes") or {}
    return votes.get(username, 0)

# register helpers into Jinja
app.jinja_env.globals.update(
    get_post_score=get_post_score,
    get_comment_score=get_comment_score,
    get_post_user_vote=get_post_user_vote,
    get_comment_user_vote=get_comment_user_vote
)

# ---------------- ROUTES ----------------

# show login page
@app.route('/', methods=['GET'])
def login_page():
    # pass user=None so navbar doesn't show logout
    return render_template('login.html', user=None)

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

    return render_template('create.html', user=None)

# main feed page
@app.route('/home', methods=['GET'])
def home():
    username = session.get("username", "Guest")
    first_name = session.get("first_name")
    return render_template(
        'feed.html',
        posts=POSTS,
        username=username,
        first_name=first_name,
        user=username  # lets navbar know someone is "logged in"
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
            "comments": [],
            "votes": {}   # no votes yet
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
                "text": comment_text,
                "votes": {}   # comments can be voted on too
            })

    return redirect(url_for('home'))

# --------- NEW: vote routes ----------

@app.route('/vote_post/<int:post_index>', methods=['POST'])
def vote_post(post_index):
    username = session.get("username", "Guest")

    if not (0 <= post_index < len(POSTS)):
        abort(404)

    vote_type = request.form.get("vote")  # 'up' or 'down'
    if vote_type not in ("up", "down"):
        abort(400)

    post = POSTS[post_index]
    votes = post.setdefault("votes", {})

    current = votes.get(username, 0)
    new_val = 1 if vote_type == "up" else -1

    # Reddit-like toggle: clicking the same arrow again clears your vote
    if current == new_val:
        del votes[username]
    else:
        votes[username] = new_val

    return redirect(url_for('home'))


@app.route('/vote_comment/<int:post_index>/<int:comment_index>', methods=['POST'])
def vote_comment(post_index, comment_index):
    username = session.get("username", "Guest")

    if not (0 <= post_index < len(POSTS)):
        abort(404)

    comments = POSTS[post_index]["comments"]
    if not (0 <= comment_index < len(comments)):
        abort(404)

    vote_type = request.form.get("vote")  # 'up' or 'down'
    if vote_type not in ("up", "down"):
        abort(400)

    comment = comments[comment_index]
    votes = comment.setdefault("votes", {})

    current = votes.get(username, 0)
    new_val = 1 if vote_type == "up" else -1

    if current == new_val:
        del votes[username]
    else:
        votes[username] = new_val

    return redirect(url_for('home'))

# --------- delete routes ----------

# delete a post (only if it's yours)
@app.route('/delete_post/<int:post_index>', methods=['POST'])
def delete_post(post_index):
    username = session.get("username", "Guest")

    if not (0 <= post_index < len(POSTS)):
        abort(404)

    post = POSTS[post_index]

    if post["user"] != username:
        abort(403)

    POSTS.pop(post_index)
    return redirect(url_for('home'))


# delete a comment (only if it's yours)
@app.route('/delete_comment/<int:post_index>/<int:comment_index>', methods=['POST'])
def delete_comment(post_index, comment_index):
    username = session.get("username", "Guest")

    if not (0 <= post_index < len(POSTS)):
        abort(404)

    comments = POSTS[post_index]["comments"]

    if not (0 <= comment_index < len(comments)):
        abort(404)

    comment = comments[comment_index]

    if comment["user"] != username:
        abort(403)

    comments.pop(comment_index)
    return redirect(url_for('home'))


# logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=False, use_reloader=False,
            threaded=True)
