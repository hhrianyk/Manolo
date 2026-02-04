// Основні функції для сайту CreoArt Studio "Manolo"

document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація прелоадера
    initPreloader();

    // Ініціалізація навігації
    initNavigation();

    // Ініціалізація анімацій при скролі
    initScrollAnimations();

    // Ініціалізація форми
    initContactForm();

    // Ініціалізація мобільного меню
    initMobileMenu();

    // Ініціалізація анімації заголовків
    initTitleAnimation();
});

function initPreloader() {
    const preloader = document.getElementById('preloader');
    const progressBar = document.querySelector('.loading-progress');

    if (!preloader || !progressBar) return;

    // Симуляція завантаження
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        progressBar.style.width = Math.min(progress, 100) + '%';

        if (progress >= 100) {
            clearInterval(interval);

            // Затримка перед приховуванням
            setTimeout(() => {
                preloader.style.opacity = '0';
                preloader.style.visibility = 'hidden';

                // Видаляємо прелоадер після анімації
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 500);
            }, 300);
        }
    }, 50);
}

function initNavigation() {
    // Плавна прокрутка для посилань
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Оновлення активної навігації
                updateActiveNavLink();
            }
        });
    });

    // Оновлення активної навігації при скролі
    window.addEventListener('scroll', updateActiveNavLink);
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    let currentSection = '';
    const scrollPosition = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });

    // Додавання класу scrolled для навігації
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
}

function initScrollAnimations() {
    // Спостерігач для анімацій при скролі
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');

                // Анімація для чисел у статистиці
                if (entry.target.classList.contains('stat-number')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Спостереження за елементами
    document.querySelectorAll('.fade-in-up, .stat-number, .concept-card, .service-card, .workshop-card').forEach(el => {
        observer.observe(el);
    });
}

function animateCounter(element) {
    const finalValue = parseInt(element.getAttribute('data-count'));
    const duration = 2000; // 2 секунди
    const increment = finalValue / (duration / 16); // 60fps
    let currentValue = 0;

    const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= finalValue) {
            element.textContent = finalValue;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(currentValue);
        }
    }, 16);
}

function initContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Отримання даних форми
        const formData = new FormData(form);
        const name = form.querySelector('input[type="text"]').value;
        const phone = form.querySelector('input[type="tel"]').value;
        const message = form.querySelector('textarea').value;

        // Валідація
        if (!name || !phone || !message) {
            showNotification('Будь ласка, заповніть всі обов\'язкові поля', 'error');
            return;
        }

        // Симуляція відправки
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;

        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Відправка...';
        submitButton.disabled = true;

        // Симуляція запиту
        setTimeout(() => {
            showNotification('Дякуємо за ваш запит! Ми зв\'яжемося з вами найближчим часом.', 'success');
            form.reset();
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 1500);
    });
}

function showNotification(message, type) {
    // Створення сповіщення
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    // Додавання до body
    document.body.appendChild(notification);

    // Показати сповіщення
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Приховати через 5 секунд
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

function initMobileMenu() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (!navToggle || !navMenu) return;

    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');

        // Зміна іконки
        const icon = navToggle.querySelector('i');
        if (navMenu.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Закриття меню при кліку на посилання
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            const icon = navToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        });
    });
}

function initTitleAnimation() {
    // Анімація зміни тексту в герої
    const changingText = document.querySelector('.tagline-changing');
    if (!changingText) return;

    const texts = [
        'можливо все',
        'народжуються ідеї',
        'зустрічаються таланти',
        'відбувається магія'
    ];

    let currentIndex = 0;

    setInterval(() => {
        currentIndex = (currentIndex + 1) % texts.length;
        changingText.style.opacity = '0';

        setTimeout(() => {
            changingText.textContent = texts[currentIndex];
            changingText.style.opacity = '1';
        }, 300);
    }, 3000);
}

// Паралакс ефект для героя
window.addEventListener('scroll', function() {
    const hero = document.querySelector('.hero');
    const scrolled = window.pageYOffset;

    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.3}px)`;
    }

    // Кнопка "Наверх"
    const backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    }
});

// Обробка клавіші ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('navMenu');
        const navToggle = document.getElementById('navToggle');

        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
            const icon = navToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    }
});

// Ініціалізація кнопок майстер-класів
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.workshop-btn').forEach(button => {
        button.addEventListener('click', function() {
            const workshop = this.getAttribute('data-workshop');
            showWorkshopModal(workshop);
        });
    });
});

function showWorkshopModal(workshop) {
    const workshopNames = {
        'doll': 'Створення ляльок',
        'painting': 'Живопис',
        'mixology': 'Міксологія'
    };

    const modalHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Запис на майстер-клас: ${workshopNames[workshop]}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <form class="workshop-form">
                        <div class="form-group">
                            <input type="text" placeholder="Ваше ім'я" required>
                        </div>
                        <div class="form-group">
                            <input type="tel" placeholder="Телефон" required>
                        </div>
                        <div class="form-group">
                            <input type="email" placeholder="Email" required>
                        </div>
                        <div class="form-group">
                            <input type="date" placeholder="Бажана дата" required>
                        </div>
                        <button type="submit" class="btn-gold">
                            <span>Записатися</span>
                            <i class="fas fa-calendar-check"></i>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `;

    // Додавання модального вікна
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Обробка закриття
    const modal = document.querySelector('.modal-overlay');
    const closeBtn = modal.querySelector('.modal-close');

    closeBtn.addEventListener('click', () => {
        modal.remove();
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });

    // Обробка форми
    const form = modal.querySelector('.workshop-form');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        showNotification('Ви успішно записалися на майстер-клас! Ми зв\'яжемося з вами для підтвердження.', 'success');
        modal.remove();
    });
}