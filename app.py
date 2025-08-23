from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load trained model and scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# In-memory user store (replace with DB later)
users = {}

@app.route('/')
def index():
    return redirect('/login')

# -------- Login --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

# -------- Register --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username in users:
            return render_template('register.html', error="Username already exists.")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")

        users[username] = password
        return redirect('/login')
    return render_template('register.html')

# -------- Home --------
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/login')
    return render_template('home.html', username=session['username'])

# -------- Test Page --------
@app.route('/test')
def test():
    if 'username' not in session:
        return redirect('/login')
    return render_template('test.html', username=session['username'])

# -------- Predict --------
@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect('/login')

    try:
        fields = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope'
        ]
        values = [float(request.form[field]) for field in fields]
        input_scaled = scaler.transform([values])
        result = model.predict(input_scaled)[0]

        output = "⚠️ Signs of CAD detected." if result == 1 else "✅ No signs of CAD detected."
        return render_template('result.html', prediction=output, username=session['username'])

    except Exception as e:
        return f"Prediction Error: {e}"

# -------- Logout --------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
