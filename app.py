from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'income_tax_system')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Helper function to execute stored procedures
def call_procedure(proc_name, args):
    cur = mysql.connection.cursor()
    placeholders = ', '.join(['%s'] * len(args))
    cur.callproc(proc_name, args)
    mysql.connection.commit()
    cur.close()

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        full_name = request.form['full_name']
        pan_number = request.form['pan_number'].upper()
        
        try:
            call_procedure('register_user', [username, email, password, full_name, pan_number])
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    cur = mysql.connection.cursor()
    
    # Get user info
    cur.execute("SELECT * FROM users WHERE user_id = %s", [user_id])
    user = cur.fetchone()
    
    # Get tax records
    cur.execute("SELECT * FROM tax_details WHERE user_id = %s ORDER BY financial_year DESC", [user_id])
    tax_records = cur.fetchall()
    
    cur.close()
    return render_template('dashboard.html', user=user, tax_records=tax_records)

@app.route('/add_tax_record', methods=['GET', 'POST'])
def add_tax_record():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        financial_year = request.form['financial_year']
        income = float(request.form['income'])
        deductions = float(request.form['deductions'])
        tax_paid = float(request.form['tax_paid'])
        
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO tax_details (user_id, financial_year, income, deductions, tax_paid)
                VALUES (%s, %s, %s, %s, %s)
            """, [user_id, financial_year, income, deductions, tax_paid])
            mysql.connection.commit()
            
            # Calculate tax
            cur.callproc('calculate_tax', [user_id, financial_year])
            mysql.connection.commit()
            
            flash('Tax record added successfully!', 'success')
            cur.close()
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error adding tax record: {str(e)}', 'danger')
    
    return render_template('add_tax_record.html')

@app.route('/file_return/<int:tax_id>')
def file_return(tax_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        cur = mysql.connection.cursor()
        
        # Get financial year for the tax record
        cur.execute("SELECT financial_year FROM tax_details WHERE tax_id = %s AND user_id = %s", 
                   [tax_id, session['user_id']])
        record = cur.fetchone()
        
        if record:
            call_procedure('file_tax_return', [session['user_id'], record['financial_year']])
            flash('Tax return filed successfully!', 'success')
        else:
            flash('Record not found', 'danger')
        
        cur.close()
    except Exception as e:
        flash(f'Error filing return: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)