from flask import Flask, render_template, request, redirect, flash, session
import re, secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32) 

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_valid_phone(phone):
    phone_regex = r'^\+?[0-9]{10,15}$'
    return re.match(phone_regex, phone) is not None

def is_valid_password(password):
    password_regex = r'.{8,}'
    return re.match(password_regex, password) is not None

def is_valid_inn(inn):
    return len(inn) == 12

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'surname': request.form.get('surname'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm_password')
        }
        
        errors = []
        if not all(data.values()):
            errors.append("❌Все поля должны быть заполнены")
        if data['password'] != data['confirm_password']:
            errors.append("❌Пароли не совпадают!")
        if not is_valid_email(data['email']):
            errors.append('❌Некорректный адрес электронной почты!')
        if not is_valid_phone(data['phone']):
            errors.append("❌Некорректный номер телефона!")
        if not is_valid_password(data['password']):
            errors.append("❌Пароль должен быть от 8 символов")
        if errors:
            for error in errors:
                flash(error)
            return redirect('/')
        
        session['user_data'] = data
        return redirect('/passport')
    
    return render_template('form.html')

@app.route('/passport', methods=['GET', 'POST'])
def passport():
    if request.method == 'POST':
        passport_data = {
            'inn': request.form.get('inn'),
            'address': request.form.get('address'),
            'passport_series': request.form.get('passport_series'),
            'passport_number': request.form.get('passport_number'),
            'passport_place_of_birth': request.form.get('passport_place_of_birth'),

        }
        errors = []
        if not all(passport_data.values()):
            errors.append("Все поля должны быть заполнены")
        if not is_valid_inn(passport_data['inn']):
            errors.append("Некорректный ИНН!")
        if errors:
            for error in errors: 
                flash(error)
            return redirect('/passport')
        
        combined_data = session['user_data']
        combined_data.update(passport_data)
        
        session.pop('user_data', None)
        return redirect('/success')
    
    return render_template('passport.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/api/success', methods=['GET'])
def api_success():
    return {'message': 'Форма успешно отправлена!'}, 200

if __name__ == '__main__':
    app.run(debug=True)