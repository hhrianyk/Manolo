import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Конфігурація для Railway
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'manolo-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///manolo.db').replace('postgres://',
                                                                                                      'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Створення директорій
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('instance', exist_ok=True)

db = SQLAlchemy(app)


# ==================== CUSTOM JINJA FILTERS ====================

def from_json(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return []


app.jinja_env.filters['from_json'] = from_json


# ==================== LOGIN DECORATOR ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Будь ласка, увійдіть в адмін-панель', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)

    return decorated_function


# ==================== MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    value_type = db.Column(db.String(20), default='text')


class HeroSection(db.Model):
    __tablename__ = 'hero_section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default='Місце, де можливо все')
    subtitle = db.Column(db.String(300))
    background_image = db.Column(db.String(200))
    cta_text = db.Column(db.String(100), default='Обрати послугу')
    cta_link = db.Column(db.String(200), default='#pricing')
    cta2_text = db.Column(db.String(100), default='Забронювати столик')
    cta2_link = db.Column(db.String(200), default='#contact')
    stats = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-spa')
    image = db.Column(db.String(200))
    features = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class PricingPackage(db.Model):
    __tablename__ = 'pricing_packages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False, default=0)
    currency = db.Column(db.String(10), default='₴')
    period = db.Column(db.String(20), default='сесія')
    features = db.Column(db.Text)
    badge = db.Column(db.String(50))
    is_featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class TeamMember(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    experience = db.Column(db.Integer)
    social_instagram = db.Column(db.String(200))
    social_facebook = db.Column(db.String(200))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='general')
    likes = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    rating = db.Column(db.Integer, default=5)
    text = db.Column(db.Text, nullable=False)
    service = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)


class FAQ(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class DarkCafeItem(db.Model):
    __tablename__ = 'dark_cafe_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-moon')
    extra_info = db.Column(db.String(100))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class InstagramPost(db.Model):
    __tablename__ = 'instagram_posts'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    hashtags = db.Column(db.String(200))
    instagram_url = db.Column(db.String(200))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class ContactRequest(db.Model):
    __tablename__ = 'contact_requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    service = db.Column(db.String(100))
    date = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)


# ==================== ROUTES ====================

@app.route('/')
def index():
    hero = HeroSection.query.filter_by(is_active=True).first()
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
    pricing = PricingPackage.query.filter_by(is_active=True).order_by(PricingPackage.order).all()
    team = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.order).all()
    gallery = GalleryImage.query.filter_by(is_active=True).order_by(GalleryImage.order).all()
    testimonials = Testimonial.query.filter_by(is_approved=True).order_by(Testimonial.order).all()
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order).all()
    dark_cafe = DarkCafeItem.query.filter_by(is_active=True).order_by(DarkCafeItem.order).all()
    instagram_posts = InstagramPost.query.filter_by(is_active=True).order_by(InstagramPost.order).limit(4).all()

    def get_setting(key, default=''):
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

    hero_stats = []
    if hero and hero.stats:
        try:
            hero_stats = json.loads(hero.stats)
        except:
            hero_stats = []

    return render_template('index.html',
                           hero=hero,
                           services=services,
                           pricing=pricing,
                           team=team,
                           gallery=gallery,
                           testimonials=testimonials,
                           faqs=faqs,
                           dark_cafe=dark_cafe,
                           instagram_posts=instagram_posts,
                           hero_stats=hero_stats,
                           site_title=get_setting('site_title', 'CreoArt Studio "Manolo" | Харків 2026'),
                           site_description=get_setting('site_description', 'CreoArt Studio Manolo - простір краси'),
                           address=get_setting('address', 'Chernyshevskaya, 30, Kharkiv'),
                           phone=get_setting('phone', '+38 (050) 123-45-67'),
                           email=get_setting('email', 'info@manolo-creoart.com'),
                           work_hours=get_setting('work_hours', 'Пн-Нд: 10:00 - 22:00'),
                           dark_cafe_hours=get_setting('dark_cafe_hours', 'Темне кафе: 18:00 - 23:00'),
                           instagram_url=get_setting('instagram_url', 'https://www.instagram.com/manolo_creoart_kh/'),
                           telegram_url=get_setting('telegram_url', 'https://t.me/manolo_creoart'),
                           facebook_url=get_setting('facebook_url', '#'),
                           tiktok_url=get_setting('tiktok_url', '#')
                           )


@app.route('/api/contact', methods=['POST'])
def api_contact():
    try:
        data = request.get_json() or request.form
        contact = ContactRequest(
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            service=data.get('service'),
            date=data.get('date'),
            message=data.get('message')
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Заявку відправлено!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ==================== ADMIN AUTH ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Вітаємо в адмін-панелі!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Невірне ім\'я користувача або пароль', 'danger')

    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Ви вийшли з адмін-панелі', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html',
                           total_services=Service.query.count(),
                           total_team=TeamMember.query.count(),
                           total_gallery=GalleryImage.query.count(),
                           total_pricing=PricingPackage.query.count(),
                           total_contacts=ContactRequest.query.filter_by(is_read=False).count(),
                           total_requests=ContactRequest.query.count(),
                           recent_requests=ContactRequest.query.order_by(ContactRequest.created_at.desc()).limit(
                               5).all()
                           )


# ==================== ADMIN HERO ====================

@app.route('/admin/hero', methods=['GET', 'POST'])
@login_required
def admin_hero():
    hero = HeroSection.query.first()

    if request.method == 'POST':
        if not hero:
            hero = HeroSection()
            db.session.add(hero)

        hero.title = request.form.get('title')
        hero.subtitle = request.form.get('subtitle')
        hero.cta_text = request.form.get('cta_text')
        hero.cta_link = request.form.get('cta_link')
        hero.cta2_text = request.form.get('cta2_text')
        hero.cta2_link = request.form.get('cta2_link')

        stats = []
        stat_labels = request.form.getlist('stat_label[]')
        stat_numbers = request.form.getlist('stat_number[]')
        for label, number in zip(stat_labels, stat_numbers):
            if label and number:
                stats.append({'label': label, 'number': number})
        hero.stats = json.dumps(stats)

        if 'background_image' in request.files:
            file = request.files['background_image']
            if file and file.filename:
                filename = secure_filename(f"hero_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file.save(os.path.join('static/images', filename))
                hero.background_image = f"images/{filename}"

        db.session.commit()
        flash('Hero секцію оновлено!', 'success')
        return redirect(url_for('admin_hero'))

    hero_stats = []
    if hero and hero.stats:
        try:
            hero_stats = json.loads(hero.stats)
        except:
            hero_stats = []

    return render_template('admin/hero_edit.html', hero=hero, hero_stats=hero_stats)


# ==================== ADMIN SERVICES ====================

@app.route('/admin/services')
@login_required
def admin_services():
    services = Service.query.order_by(Service.order).all()
    return render_template('admin/services_list.html', services=services)


@app.route('/admin/service/add', methods=['GET', 'POST'])
@app.route('/admin/service/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_service_edit(id=None):
    service = Service.query.get(id) if id else Service()

    if request.method == 'POST':
        service.title = request.form.get('title')
        service.description = request.form.get('description')
        service.icon = request.form.get('icon')
        service.order = int(request.form.get('order', 0))
        service.is_active = 'is_active' in request.form

        features = request.form.getlist('features[]')
        service.features = json.dumps([f for f in features if f])

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(f"service_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file.save(os.path.join('static/images', filename))
                service.image = f"images/{filename}"

        if not id:
            db.session.add(service)

        db.session.commit()
        flash('Послугу збережено!', 'success')
        return redirect(url_for('admin_services'))

    features = json.loads(service.features) if service.features else []
    return render_template('admin/service_edit.html', service=service, features=features)


@app.route('/admin/service/delete/<int:id>')
@login_required
def admin_service_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Послугу видалено!', 'success')
    return redirect(url_for('admin_services'))


# ==================== ADMIN PRICING ====================

@app.route('/admin/pricing')
@login_required
def admin_pricing():
    packages = PricingPackage.query.order_by(PricingPackage.order).all()
    return render_template('admin/pricing_list.html', packages=packages)


@app.route('/admin/pricing/add', methods=['GET', 'POST'])
@app.route('/admin/pricing/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_pricing_edit(id=None):
    package = PricingPackage.query.get(id) if id else PricingPackage()

    if request.method == 'POST':
        package.name = request.form.get('name')
        package.subtitle = request.form.get('subtitle')
        package.price = int(request.form.get('price', 0))
        package.currency = request.form.get('currency', '₴')
        package.period = request.form.get('period')
        package.badge = request.form.get('badge')
        package.is_featured = 'is_featured' in request.form
        package.order = int(request.form.get('order', 0))
        package.is_active = 'is_active' in request.form

        features = request.form.getlist('features[]')
        package.features = json.dumps([f for f in features if f])

        if not id:
            db.session.add(package)

        db.session.commit()
        flash('Пакет збережено!', 'success')
        return redirect(url_for('admin_pricing'))

    features = json.loads(package.features) if package.features else []
    return render_template('admin/pricing_edit.html', package=package, features=features)


@app.route('/admin/pricing/delete/<int:id>')
@login_required
def admin_pricing_delete(id):
    package = PricingPackage.query.get_or_404(id)
    db.session.delete(package)
    db.session.commit()
    flash('Пакет видалено!', 'success')
    return redirect(url_for('admin_pricing'))


# ==================== ADMIN TEAM ====================

@app.route('/admin/team')
@login_required
def admin_team():
    team_members = TeamMember.query.order_by(TeamMember.order).all()
    return render_template('admin/team_list.html', team_members=team_members)


@app.route('/admin/team/add', methods=['GET', 'POST'])
@app.route('/admin/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_team_edit(id=None):
    member = TeamMember.query.get(id) if id else TeamMember()

    if request.method == 'POST':
        member.name = request.form.get('name')
        member.role = request.form.get('role')
        member.description = request.form.get('description')
        member.experience = request.form.get('experience', type=int)
        member.social_instagram = request.form.get('social_instagram')
        member.social_facebook = request.form.get('social_facebook')
        member.order = int(request.form.get('order', 0))
        member.is_active = 'is_active' in request.form

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(f"team_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file.save(os.path.join('static/images', filename))
                member.image = f"images/{filename}"

        if not id:
            db.session.add(member)

        db.session.commit()
        flash('Члена команди збережено!', 'success')
        return redirect(url_for('admin_team'))

    return render_template('admin/team_edit.html', member=member)


@app.route('/admin/team/delete/<int:id>')
@login_required
def admin_team_delete(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Члена команди видалено!', 'success')
    return redirect(url_for('admin_team'))


# ==================== ADMIN GALLERY ====================

@app.route('/admin/gallery')
@login_required
def admin_gallery():
    gallery_images = GalleryImage.query.order_by(GalleryImage.order).all()
    return render_template('admin/gallery_list.html', gallery_images=gallery_images)


@app.route('/admin/gallery/add', methods=['GET', 'POST'])
@app.route('/admin/gallery/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_gallery_edit(id=None):
    image = GalleryImage.query.get(id) if id else GalleryImage()

    if request.method == 'POST':
        image.title = request.form.get('title')
        image.description = request.form.get('description')
        image.category = request.form.get('category')
        image.likes = int(request.form.get('likes', 0))
        image.order = int(request.form.get('order', 0))
        image.is_active = 'is_active' in request.form

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(f"gallery_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file.save(os.path.join('static/images', filename))
                image.image = f"images/{filename}"

        if not id and not image.image:
            flash('Будь ласка, оберіть зображення', 'danger')
            return render_template('admin/gallery_edit.html', image=image)

        if not id:
            db.session.add(image)

        db.session.commit()
        flash('Зображення збережено!', 'success')
        return redirect(url_for('admin_gallery'))

    return render_template('admin/gallery_edit.html', image=image)


@app.route('/admin/gallery/delete/<int:id>')
@login_required
def admin_gallery_delete(id):
    image = GalleryImage.query.get_or_404(id)
    db.session.delete(image)
    db.session.commit()
    flash('Зображення видалено!', 'success')
    return redirect(url_for('admin_gallery'))


# ==================== ADMIN DARK CAFE ====================

@app.route('/admin/dark-cafe')
@login_required
def admin_dark_cafe():
    items = DarkCafeItem.query.order_by(DarkCafeItem.order).all()
    return render_template('admin/dark_cafe_list.html', items=items)


@app.route('/admin/dark-cafe/add', methods=['GET', 'POST'])
@app.route('/admin/dark-cafe/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_dark_cafe_edit(id=None):
    item = DarkCafeItem.query.get(id) if id else DarkCafeItem()

    if request.method == 'POST':
        item.title = request.form.get('title')
        item.description = request.form.get('description')
        item.icon = request.form.get('icon')
        item.extra_info = request.form.get('extra_info')
        item.order = int(request.form.get('order', 0))
        item.is_active = 'is_active' in request.form

        if not id:
            db.session.add(item)

        db.session.commit()
        flash('Елемент збережено!', 'success')
        return redirect(url_for('admin_dark_cafe'))

    return render_template('admin/dark_cafe_edit.html', item=item)


@app.route('/admin/dark-cafe/delete/<int:id>')
@login_required
def admin_dark_cafe_delete(id):
    item = DarkCafeItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Елемент видалено!', 'success')
    return redirect(url_for('admin_dark_cafe'))


# ==================== ADMIN TESTIMONIALS ====================

@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    testimonials = Testimonial.query.order_by(Testimonial.order).all()
    return render_template('admin/testimonials_list.html', testimonials=testimonials)


@app.route('/admin/testimonial/add', methods=['GET', 'POST'])
@app.route('/admin/testimonial/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_testimonial_edit(id=None):
    testimonial = Testimonial.query.get(id) if id else Testimonial()

    if request.method == 'POST':
        testimonial.name = request.form.get('name')
        testimonial.rating = int(request.form.get('rating', 5))
        testimonial.text = request.form.get('text')
        testimonial.service = request.form.get('service')
        testimonial.is_approved = 'is_approved' in request.form
        testimonial.order = int(request.form.get('order', 0))

        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename:
                filename = secure_filename(f"avatar_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file.save(os.path.join('static/images', filename))
                testimonial.avatar = f"images/{filename}"

        if not id:
            db.session.add(testimonial)

        db.session.commit()
        flash('Відгук збережено!', 'success')
        return redirect(url_for('admin_testimonials'))

    return render_template('admin/testimonial_edit.html', testimonial=testimonial)


@app.route('/admin/testimonial/delete/<int:id>')
@login_required
def admin_testimonial_delete(id):
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Відгук видалено!', 'success')
    return redirect(url_for('admin_testimonials'))


# ==================== ADMIN FAQS ====================

@app.route('/admin/faqs')
@login_required
def admin_faqs():
    faqs = FAQ.query.order_by(FAQ.order).all()
    return render_template('admin/faqs_list.html', faqs=faqs)


@app.route('/admin/faq/add', methods=['GET', 'POST'])
@app.route('/admin/faq/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_faq_edit(id=None):
    faq = FAQ.query.get(id) if id else FAQ()

    if request.method == 'POST':
        faq.question = request.form.get('question')
        faq.answer = request.form.get('answer')
        faq.order = int(request.form.get('order', 0))
        faq.is_active = 'is_active' in request.form

        if not id:
            db.session.add(faq)

        db.session.commit()
        flash('FAQ збережено!', 'success')
        return redirect(url_for('admin_faqs'))

    return render_template('admin/faq_edit.html', faq=faq)


@app.route('/admin/faq/delete/<int:id>')
@login_required
def admin_faq_delete(id):
    faq = FAQ.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('FAQ видалено!', 'success')
    return redirect(url_for('admin_faqs'))


# ==================== ADMIN INSTAGRAM ====================

@app.route('/admin/instagram')
@login_required
def admin_instagram():
    posts = InstagramPost.query.order_by(InstagramPost.order).all()
    return render_template('admin/instagram_list.html', posts=posts)


@app.route('/admin/instagram/add', methods=['GET', 'POST'])
@app.route('/admin/instagram/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_instagram_edit(id=None):
    post = InstagramPost.query.get(id) if id else InstagramPost()

    if request.method == 'POST':
        post.caption = request.form.get('caption')
        post.likes = int(request.form.get('likes', 0))
        post.hashtags = request.form.get('hashtags')
        post.instagram_url = request.form.get('instagram_url')
        post.order = int(request.form.get('order', 0))
        post.is_active = 'is_active' in request.form

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(f"insta_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                file.save(os.path.join('static/images', filename))
                post.image = f"images/{filename}"

        if not id and not post.image:
            flash('Будь ласка, оберіть зображення', 'danger')
            return render_template('admin/instagram_edit.html', post=post)

        if not id:
            db.session.add(post)

        db.session.commit()
        flash('Instagram пост збережено!', 'success')
        return redirect(url_for('admin_instagram'))

    return render_template('admin/instagram_edit.html', post=post)


@app.route('/admin/instagram/delete/<int:id>')
@login_required
def admin_instagram_delete(id):
    post = InstagramPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост видалено!', 'success')
    return redirect(url_for('admin_instagram'))


# ==================== ADMIN CONTACTS ====================

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    requests = ContactRequest.query.order_by(ContactRequest.created_at.desc()).all()
    return render_template('admin/contacts_list.html', requests=requests)


@app.route('/admin/contact/read/<int:id>')
@login_required
def admin_contact_read(id):
    contact = ContactRequest.query.get_or_404(id)
    contact.is_read = True
    db.session.commit()
    flash('Заявку позначено як прочитану', 'success')
    return redirect(url_for('admin_contacts'))


@app.route('/admin/contact/delete/<int:id>')
@login_required
def admin_contact_delete(id):
    contact = ContactRequest.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Заявку видалено', 'success')
    return redirect(url_for('admin_contacts'))


# ==================== ADMIN SETTINGS ====================

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        settings = {
            'site_title': request.form.get('site_title'),
            'site_description': request.form.get('site_description'),
            'address': request.form.get('address'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
            'work_hours': request.form.get('work_hours'),
            'dark_cafe_hours': request.form.get('dark_cafe_hours'),
            'instagram_url': request.form.get('instagram_url'),
            'telegram_url': request.form.get('telegram_url'),
            'facebook_url': request.form.get('facebook_url'),
            'tiktok_url': request.form.get('tiktok_url'),
        }

        for key, value in settings.items():
            setting = SiteSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = SiteSetting(key=key, value=value)
                db.session.add(setting)

        db.session.commit()
        flash('Налаштування збережено!', 'success')
        return redirect(url_for('admin_settings'))

    def get_setting(key, default=''):
        setting = SiteSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

    settings = {
        'site_title': get_setting('site_title', 'CreoArt Studio "Manolo" | Харків 2026'),
        'site_description': get_setting('site_description', 'CreoArt Studio Manolo - простір краси'),
        'address': get_setting('address', 'Chernyshevskaya, 30, Kharkiv'),
        'phone': get_setting('phone', '+38 (050) 123-45-67'),
        'email': get_setting('email', 'info@manolo-creoart.com'),
        'work_hours': get_setting('work_hours', 'Пн-Нд: 10:00 - 22:00'),
        'dark_cafe_hours': get_setting('dark_cafe_hours', 'Темне кафе: 18:00 - 23:00'),
        'instagram_url': get_setting('instagram_url', 'https://www.instagram.com/manolo_creoart_kh/'),
        'telegram_url': get_setting('telegram_url', 'https://t.me/manolo_creoart'),
        'facebook_url': get_setting('facebook_url', '#'),
        'tiktok_url': get_setting('tiktok_url', '#'),
    }

    return render_template('admin/settings.html', settings=settings)


# ==================== ADMIN COLORS ====================

@app.route('/admin/colors', methods=['GET', 'POST'])
@login_required
def admin_colors():
    def get_color(key, default):
        setting = SiteSetting.query.filter_by(key=f'color_{key}').first()
        return setting.value if setting else default

    if request.method == 'POST':
        colors = {
            'bg_deep': request.form.get('bg_deep'),
            'bg_surface': request.form.get('bg_surface'),
            'chocolate': request.form.get('chocolate'),
            'chocolate_light': request.form.get('chocolate_light'),
            'chocolate_dark': request.form.get('chocolate_dark'),
            'text_main': request.form.get('text_main'),
            'text_body': request.form.get('text_body'),
        }

        for key, value in colors.items():
            if value:
                setting = SiteSetting.query.filter_by(key=f'color_{key}').first()
                if setting:
                    setting.value = value
                else:
                    setting = SiteSetting(key=f'color_{key}', value=value)
                    db.session.add(setting)

        db.session.commit()
        generate_color_css(colors)
        flash('Кольорову палітру збережено!', 'success')
        return redirect(url_for('admin_colors'))

    colors = {
        'bg_deep': get_color('bg_deep', '#0A0A0A'),
        'bg_surface': get_color('bg_surface', '#151515'),
        'chocolate': get_color('chocolate', '#D2691E'),
        'chocolate_light': get_color('chocolate_light', '#E28B42'),
        'chocolate_dark': get_color('chocolate_dark', '#8B4513'),
        'text_main': get_color('text_main', '#FFFFFF'),
        'text_body': get_color('text_body', '#B0B0B0'),
    }

    return render_template('admin/colors.html', colors=colors)


@app.route('/admin/reset-colors')
@login_required
def admin_reset_colors():
    default_colors = {
        'bg_deep': '#0A0A0A',
        'bg_surface': '#151515',
        'chocolate': '#D2691E',
        'chocolate_light': '#E28B42',
        'chocolate_dark': '#8B4513',
        'text_main': '#FFFFFF',
        'text_body': '#B0B0B0',
    }

    for key, value in default_colors.items():
        setting = SiteSetting.query.filter_by(key=f'color_{key}').first()
        if setting:
            setting.value = value
        else:
            setting = SiteSetting(key=f'color_{key}', value=value)
            db.session.add(setting)

    db.session.commit()
    generate_color_css(default_colors)
    flash('Кольори скинуто до стандартних!', 'success')
    return redirect(url_for('admin_colors'))


def generate_color_css(colors):
    css_content = f""":root {{
    --bg-deep: {colors.get('bg_deep', '#0A0A0A')};
    --bg-surface: {colors.get('bg_surface', '#151515')};
    --chocolate: {colors.get('chocolate', '#D2691E')};
    --chocolate-light: {colors.get('chocolate_light', '#E28B42')};
    --chocolate-dark: {colors.get('chocolate_dark', '#8B4513')};
    --text-main: {colors.get('text_main', '#FFFFFF')};
    --text-body: {colors.get('text_body', '#B0B0B0')};
}}
"""
    with open('static/css/colors.css', 'w', encoding='utf-8') as f:
        f.write(css_content)


# ==================== INITIALIZE DATABASE ====================

def init_db():
    db.create_all()

    # Create admin user
    if not User.query.first():
        admin = User(username='admin', email='admin@manolo-creoart.com')
        admin.set_password('admin123')
        db.session.add(admin)

    # Create default hero
    if not HeroSection.query.first():
        hero = HeroSection(
            title='Місце, де можливо <span class="text-gradient">все</span>',
            subtitle="Б'юті. Гастрономія. Арт-простір. Твоя точка тяжіння у центрі міста.",
            cta_text='Обрати послугу',
            cta_link='#pricing',
            cta2_text='Забронювати столик',
            cta2_link='#contact',
            stats=json.dumps([
                {'label': 'Клієнтів', 'number': '1500+'},
                {'label': 'Ляльок', 'number': '50+'},
                {'label': 'Майстер-класів', 'number': '120+'}
            ]),
            is_active=True
        )
        db.session.add(hero)

    # Create default services
    if not Service.query.first():
        services = [
            Service(title="Б'юті зона", description="Макіяж, укладки, догляд. Ми створюємо образи, що закохують.",
                    icon="fa-spa", features=json.dumps(['Денний макіяж', 'Вечірній образ', 'Професійний догляд']),
                    order=1, is_active=True),
            Service(title="Фотостудія & Циклорама", description="Професійна фотостудія з циклорамою.",
                    icon="fa-camera", features=json.dumps(['Циклорама', 'Професійне обладнання', 'Ретуш фотографій']),
                    order=2, is_active=True),
            Service(title="Майстер-класи & Івенти", description="Проведення заходів, майстер-класів та подій.",
                    icon="fa-users", features=json.dumps(['Організація подій', 'Кейтеринг', 'Технічне обладнання']),
                    order=3, is_active=True),
        ]
        for s in services:
            db.session.add(s)

    # Create default pricing
    if not PricingPackage.query.first():
        packages = [
            PricingPackage(name="Light", subtitle="Для повсякденної краси", price=1500, currency="₴", period="сесія",
                           features=json.dumps(
                               ['Денний макіяж', 'Легка укладка', 'Кава to go', 'Консультація стиліста']),
                           badge="Найпопулярніший", order=1, is_active=True),
            PricingPackage(name="Gold", subtitle="Для особливих подій", price=3200, currency="₴", period="пакет",
                           features=json.dumps(
                               ['Вечірній образ', 'Оренда сукні (1 год)', 'Фотосесія (30 хв)', 'Ігристе + закуски',
                                'Професійний ретуш']),
                           badge="Краще співвідношення", is_featured=True, order=2, is_active=True),
            PricingPackage(name="Elite", subtitle="Повний досвід Manolo", price=5500, currency="₴", period="експіріенс",
                           features=json.dumps(['Повний образ VIP', 'Супровід стиліста', 'Зйомка у дзеркальному залі',
                                                'Дегустація меню', 'Фотоальбом', 'Подарунковий сертифікат']),
                           badge="Люкс пакет", order=3, is_active=True),
        ]
        for p in packages:
            db.session.add(p)

    # Create default dark cafe items
    if not DarkCafeItem.query.first():
        items = [
            DarkCafeItem(title="Повна темрява", description="Займіться смаками без візуальних упереджень.",
                         icon="fa-moon", extra_info="18:00 - 23:00", order=1, is_active=True),
            DarkCafeItem(title="Шоколадна дегустація", description="5 видів шоколаду від білого до екстра-чорного.",
                         icon="fa-wine-glass-alt", extra_info="450 ₴ за сет", order=2, is_active=True),
            DarkCafeItem(title="Кіно у темряві", description="Артхаус кінопокази за кавою.", icon="fa-film",
                         extra_info="Щоп'ятниці", order=3, is_active=True),
        ]
        for i in items:
            db.session.add(i)

    # Create default FAQs
    if not FAQ.query.first():
        faqs = [
            FAQ(question="Як записатися на послугу?",
                answer="Ви можете скористатися формою на сайті, написати нам в Instagram Direct або зателефонувати.",
                order=1, is_active=True),
            FAQ(question="Чи можна орендувати студію під захід?",
                answer="Так, ми надаємо простір для проведення майстер-класів, презентацій та камерних вечірок.",
                order=2, is_active=True),
            FAQ(question="Як працює темне кафе?",
                answer="Темне кафе працює з 18:00 до 23:00. Всі відвідувачі проходять адаптацію до темряви.", order=3,
                is_active=True),
            FAQ(question="Чи є парковка?", answer="Так, для клієнтів ми надаємо безкоштовну парковку на території.",
                order=4, is_active=True),
        ]
        for f in faqs:
            db.session.add(f)

    db.session.commit()

    # Generate initial color CSS
    generate_color_css({
        'bg_deep': '#0A0A0A',
        'bg_surface': '#151515',
        'chocolate': '#D2691E',
        'chocolate_light': '#E28B42',
        'chocolate_dark': '#8B4513',
        'text_main': '#FFFFFF',
        'text_body': '#B0B0B0',
    })


with app.app_context():
    init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)