from flask import Flask, render_template, request, redirect, url_for, session, flash
from manager import FinanceManager
from user_manager import UserManager

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY_CHANGE_THIS" # Needed for sessions to work securely

finance_manager = FinanceManager()
user_manager = UserManager()

@app.route('/')
def home():
    # SECURITY CHECK: Is the user logged in?
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    current_user = session['username']
    finance_manager.load_data()
    
    # FILTER: Only get expenses for THIS user
    user_expenses = finance_manager.get_user_expenses(current_user)
    user_paychecks = finance_manager.get_user_paychecks(current_user)
    
    # Calculate total for THIS user only
    expenseTotal = sum(e.amount for e in user_expenses)
    incomeTotal = sum(i.amount for i in user_paychecks)
    
    # Prepare chart data for THIS user
    expenseReport = {}
    for e in user_expenses:
        expenseReport[e.category] = expenseReport.get(e.category, 0) + e.amount
        
    incomeReport = {}
    for i in user_paychecks:
        incomeReport[i.job] = incomeReport.get(i.job, 0) + i.amount 

    return render_template(
        'index.html', 
        expenses=user_expenses,
        paychecks=user_paychecks,
        expenseTotal = expenseTotal,
        incomeTotal=incomeTotal,
        expense_chart_labels=list(expenseReport.keys()),
        expense_chart_values=list(expenseReport.values()),
        income_chart_labels=list(incomeReport.keys()),
        income_chart_values=list(incomeReport.values()),
        username=current_user # Pass username to display "Welcome, Bob!"
    )

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if user_manager.verify_user(username, password):
            session['username'] = username # Log them in!
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password!")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message = user_manager.register(username, password)
        if success:
            flash("Account created! Please login.")
            return redirect(url_for('login_page'))
        else:
            flash(message)
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None) # Clear the session
    return redirect(url_for('login_page'))

@app.route('/addExpense', methods=['POST'])
def add_expense():
    if 'username' not in session:
        return redirect(url_for('login_page'))
        
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']

    # Removes leading and trailing whitespaces from category 
    category = category.strip()
    
    # Pass the logged-in user's name to the manager
    finance_manager.add_expense(amount, category, description, session['username'])
    
    return redirect(url_for('home'))

@app.route('/addIncome', methods=['POST'])
def add_income():
    if 'username' not in session:
        return redirect(url_for('login_page'))
        
    amount = float(request.form['amount'])
    job = request.form['job']
    description = request.form['description']

    # Removes leading and trailing whitespaces from category 
    job = job.strip()
    
    # Pass the logged-in user's name to the manager
    finance_manager.add_income(amount, job, description, session['username'])
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
