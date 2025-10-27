from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# --- Jinja filter ---
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

# --- Fake data store for feed ---
POSTS = [
    {"user": "Alice", "time": datetime.now(), "text": "Hello, CampusTalk!"},
]

# --- Routes ---

# Start app on the login page
@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_handler():
    button = request.form.get('type')  # "Login" or "Create"
    if button == 'Create':
        return redirect(url_for('create_account'))
    # TODO: validate username/password here
    return redirect(url_for('home'))

@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # TODO: save fields then go home
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('feed.html', posts=POSTS, username="Bailey")

@app.route('/post', methods=['POST'])
def post():
    text = (request.form.get('post') or '').strip()
    if text:
        POSTS.insert(0, {"user": "Bailey", "time": datetime.now(), "text": text})
    return redirect(url_for('home'))

# Optional: navbar logout button target
@app.route('/logout', methods=['POST'])
def logout():
    # TODO: clear session if you add one
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
