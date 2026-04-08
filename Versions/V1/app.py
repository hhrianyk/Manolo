from flask import Flask, render_template

app = Flask(__name__)

# Дані про послуги (на основі ваших картинок)
services_list = [
    {
        'title': 'Б\'юті Сфера',
        'desc': 'Масаж, перукарське мистецтво та професійний візаж. Повне перевтілення.',
        'img': 'beauty-services.jpg',
        'icon': 'fa-spa'
    },
    {
        'title': 'Лаунж Кафе',
        'desc': 'Спокійна атмосфера, затишок та авторські напої. Місце для релаксу.',
        'img': 'lounge-cafe.jpg',
        'icon': 'fa-coffee'
    },
    {
        'title': 'Арт Простір',
        'desc': 'Дзеркальний зал для дефіле, фотостудія для портфоліо та дизайнерський одяг.',
        'img': 'photo-studio.jpg', # Або gallery-mirror-hall.jpg
        'icon': 'fa-camera'
    },
    {
        'title': 'Івенти & Кейтеринг',
        'desc': 'Проведення заходів, майстер-класів та подій з вишуканим супроводом.',
        'img': 'gallery-restaurant.jpg', # Або dark-restaurant.jpg
        'icon': 'fa-wine-glass'
    }
]

# Команда
team_list = [
    {'name': 'Єлизавета Бондаренко', 'role': 'CEO & Founder', 'img': 'ceo.jpg'},
    {'name': 'Олександра', 'role': 'Арт-директор', 'img': 'art-dir.jpg'},
    {'name': 'Ірина', 'role': 'Top Stylist', 'img': 'stylist.jpg'},
    {'name': 'Марко', 'role': 'Шеф-кухар', 'img': 'chef.jpg'}
]

@app.route('/')
def index():
    return render_template('index.html', services=services_list, team=team_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)