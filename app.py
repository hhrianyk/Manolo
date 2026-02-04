from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'manolo-creoart-secret-key-2025'

# Приклад даних для галереї та послуг
services_data = [
    {
        'id': 1,
        'title': 'Бюті - послуги',
                                 'description': 'Масаж, перукарські послуги, професійний візаж',
'icon': 'spa'
},
{
    'id': 2,
    'title': 'Лаунж-кафе',
    'description': 'Затишна атмосфера з авторськими напоями та десертами',
    'icon': 'coffee'
},
{
    'id': 3,
    'title': 'Колекція ляльок',
    'description': 'Унікальні авторські ляльки для колекціонування та фотосесій',
    'icon': 'doll'
},
{
    'id': 4,
    'title': 'Фотостудія',
    'description': 'Професійне обладнання для портфоліо та креативних зйомок',
    'icon': 'camera'
},
{
    'id': 5,
    'title': 'Дзеркальний зал',
    'description': 'Простір для дефіле, репетицій та особливих подій',
    'icon': 'mirror'
},
{
    'id': 6,
    'title': 'Майстер-класи',
    'description': 'Творчі заходи та події з професійними кейтеринговими послугами',
    'icon': 'event'
}
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/services')
def get_services():
    return jsonify(services_data)


@app.route('/api/events')
def get_events():
    # Приклад подій (в реальному додатку можна брати з БД)
    events = [
        {
            'date': '15 березня 2025',
            'title': 'Майстер-клас з створення ляльок',
            'time': '18:00 - 20:00'
        },
        {
            'date': '22 березня 2025',
            'title': 'Дефіле нової колекції одягу',
            'time': '19:00 - 21:00'
        },
        {
            'date': '5 квітня 2025',
            'title': 'Арт-терапія: масаж та медитація',
            'time': '17:00 - 19:00'
        }
    ]
    return jsonify(events)


@app.route('/api/contact', methods=['POST'])
def contact_form():
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()

        # Валідація
        if not name or not email or not message:
            return jsonify({'success': False, 'error': 'Будь ласка, заповніть всі поля'})

        # Тут можна додати логіку для збереження в базу даних або відправки email
        print(f"Нове повідомлення від {name} ({email}): {message}")

        return jsonify({
            'success': True,
            'message': 'Дякуємо за ваше повідомлення! Ми зв\'яжемося з вами найближчим часом.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/award')
def get_award():
    award = {
        'title': 'Нагорода MedOrion «The Face of Creative Power»',
        'description': 'У жовтні 2025 року студія «Manolo» стала партнером премії «MedOrion Awards 2025». Господиня студії Manolo CreoArt – Єлизавета Бондаренко – була нагороджена премією у номінації «Обличчя молодої України, де сила поєднується з мистецтвом».',
        'year': '2025'
    }
    return jsonify(award)


if __name__ == '__main__':
    app.run(debug=True, port=5000)