from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from dotenv import load_dotenv
import openai
import json

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finwise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OpenAI configuration
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    monthly_income = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    debts = db.relationship('Debt', backref='user', lazy=True, cascade='all, delete-orphan')
    investments = db.relationship('Investment', backref='user', lazy=True, cascade='all, delete-orphan')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=False, default=date.today)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    target_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50))

class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    remaining_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    emi_amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expected_return = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=date.today)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        monthly_income = float(request.form.get('monthly_income', 0))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return redirect(url_for('signup'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            monthly_income=monthly_income
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Dashboard route removed

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form.get('description', '')
        expense_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        
        expense = Expense(
            user_id=current_user.id,
            category=category,
            amount=amount,
            description=description,
            date=expense_date
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html')

@app.route('/add_goal', methods=['GET', 'POST'])
@login_required
def add_goal():
    if request.method == 'POST':
        name = request.form['name']
        target_amount = float(request.form['target_amount'])
        target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d').date()
        category = request.form.get('category', 'General')
        
        goal = Goal(
            user_id=current_user.id,
            name=name,
            target_amount=target_amount,
            target_date=target_date,
            category=category
        )
        
        db.session.add(goal)
        db.session.commit()
        
        flash('Goal added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_goal.html')

@app.route('/api/today-expenses')
@login_required
def api_today_expenses():
    today = date.today()
    today_expenses = Expense.query.filter_by(user_id=current_user.id, date=today).all()
    
    expenses_data = []
    for expense in today_expenses:
        expenses_data.append({
            'category': expense.category,
            'amount': expense.amount,
            'description': expense.description,
            'date': expense.date.isoformat()
        })
    
    return jsonify({'expenses': expenses_data})

@app.route('/ai_advisor', methods=['GET', 'POST'])
@login_required
def ai_advisor():
    # Get user's financial data for both GET and POST requests
    total_expenses = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    debts = Debt.query.filter_by(user_id=current_user.id).all()
    
    # Prepare user context for AI
    user_context = {
        'monthly_income': current_user.monthly_income,
        'monthly_expenses': total_expenses,
        'monthly_savings': current_user.monthly_income - total_expenses,
        'goals': [{'name': g.name, 'target': g.target_amount, 'current': g.current_amount} for g in goals],
        'debts': [{'name': d.name, 'remaining': d.remaining_amount, 'interest': d.interest_rate} for d in debts]
    }
    
    if request.method == 'POST':
        # Generate AI advice (mock response for demo)
        mock_advice = f"""# Your Personalized Financial Advice

## 📊 Budget Analysis
**Monthly Income:** ₹{user_context['monthly_income']:,.2f}
**Monthly Expenses:** ₹{user_context['monthly_expenses']:,.2f}
**Monthly Savings:** ₹{user_context['monthly_savings']:,.2f}

**Savings Rate:** {(user_context['monthly_savings']/user_context['monthly_income']*100):.1f}%

## 💡 Budget Optimization Suggestions
{'✅ Great job! Your savings rate is healthy.' if user_context['monthly_savings'] > 0 else '⚠️ Consider reducing expenses to increase savings.'}

**Recommendations:**
• Track daily expenses to identify spending patterns
• Set a monthly budget limit for each category
• Use the 50/30/20 rule: 50% needs, 30% wants, 20% savings
• Review subscriptions and cancel unused services

## 🏦 Investment Advice for Indians
**For Beginners:**
1. **Emergency Fund:** Keep 3-6 months expenses in a savings account
2. **PPF:** Tax-free returns, invest up to ₹1.5L/year
3. **SIP in Mutual Funds:** Start with ₹500-1000/month
4. **Fixed Deposits:** Safe option for conservative investors

**Recommended SIP Allocation:**
• 40% Equity Funds (for long-term growth)
• 30% Debt Funds (for stability)
• 20% Hybrid Funds (balanced approach)
• 10% Gold ETFs (inflation hedge)

## 🎯 Goal Achievement Plan
{'You have goals set! Here is how to achieve them:' if user_context['goals'] else 'Start by setting clear financial goals:'}

**Strategy:**
• Automate monthly investments
• Increase SIP amount by 10% annually
• Review and rebalance portfolio every 6 months

## 📈 Debt Management
{'Focus on high-interest debt first' if user_context['debts'] else 'Great! No debt detected.'}

**Tips:**
• Pay more than minimum EMI when possible
• Consider debt consolidation for lower interest
• Avoid taking new debt for non-essential items

## 🇮🇳 Tax-Saving Options
• **ELSS Funds:** ₹1.5L deduction under 80C
• **PPF:** Tax-free interest and maturity
• **NPS:** Additional ₹50K deduction
• **Health Insurance:** ₹25K deduction for premium

---

*This advice is generated based on your current financial data. For personalized advice, consult a certified financial advisor.*"""

        return render_template('ai_advisor.html', advice=mock_advice, user_context=user_context)
    
    # For GET request, render the form with financial context
    return render_template('ai_advisor.html', total_expenses=total_expenses, goals=goals)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
