from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Show the login page
@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

# Handle the form with the two buttons
@app.route('/login', methods=['POST'])
def login_handler():
    button = request.form.get('type')  # "Login" or "Create"
    if button == 'Create':
        return redirect(url_for('create_account'))
    # TODO: put real login checks here (username/password)
    return redirect(url_for('home'))

# Personalization page (Create)
@app.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Grab personalization fields from create.html
        username = request.form.get('username')
        major = request.form.get('major')
        interests = request.form.get('interests')
        year = request.form.get('year')
        # TODO: save these somewhere (DB/session)
        return redirect(url_for('home'))
    return render_template('create.html')

# Home page after login/setup
@app.route('/home')
def home():
    # If you have a dedicated home.html, use that; otherwise feed.html is fine.
    return render_template('feed.html')

if __name__ == '__main__':
    app.run(debug=True)

