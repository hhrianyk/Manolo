document.addEventListener('DOMContentLoaded', () => {
    // 1. Enhanced Preloader
    const preloader = document.querySelector('.preloader');
    window.addEventListener('load', () => {
        setTimeout(() => {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
                document.body.style.overflow = 'visible';
            }, 600);
        }, 1500);
    });

    // 2. Parallax Effects
    const heroBg = document.querySelector('.hero-bg');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        if (heroBg) {
            heroBg.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });

    // 3. Sticky Navigation with Shadow
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // 4. Enhanced Mobile Menu with Touch Support
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');

    const toggleMenu = () => {
        navMenu.classList.toggle('active');
        const spans = hamburger.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            document.body.style.overflow = 'hidden';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
            document.body.style.overflow = 'visible';
        }
    };

    hamburger.addEventListener('click', toggleMenu);

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {
            if (navMenu.classList.contains('active')) {
                toggleMenu();
            }
        }
    });

    // Touch swipe to close menu
    let touchStartX = 0;
    let touchEndX = 0;

    navMenu.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    navMenu.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (touchStartX - touchEndX > 100) { // Swipe left
            toggleMenu();
        }
    });

    // 5. Advanced Scroll Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active-anim');

                // Add staggered animation for children
                if (entry.target.classList.contains('services-grid')) {
                    const cards = entry.target.querySelectorAll('.service-card');
                    cards.forEach((card, index) => {
                        setTimeout(() => {
                            card.classList.add('pop-in');
                        }, index * 200);
                    });
                }
            }
        });
    }, observerOptions);

    // Observe all animated elements
    document.querySelectorAll('.fade-up, .reveal-left, .reveal-right, .reveal-bottom, .reveal-scale').forEach(el => {
        observer.observe(el);
    });

    // 6. Smooth Scroll with Offset for Fixed Header
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerHeight = navbar.offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                if (navMenu.classList.contains('active')) {
                    toggleMenu();
                }
            }
        });
    });

    // 7. Interactive Form Validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Simple validation
            const inputs = contactForm.querySelectorAll('input[required], select[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderBottomColor = '#ff4757';
                } else {
                    input.style.borderBottomColor = '';
                }
            });

            if (isValid) {
                // Show success message
                const submitBtn = contactForm.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;

                submitBtn.innerHTML = '<i class="fas fa-check"></i> Надіслано!';
                submitBtn.style.background = 'var(--chocolate-dark)';

                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.style.background = '';
                    contactForm.reset();
                }, 2000);
            }
        });
    }

    // 8. Chocolate-themed Cursor Effects (Desktop only)
    if (window.innerWidth > 768) {
        const cursor = document.createElement('div');
        cursor.classList.add('custom-cursor');
        document.body.appendChild(cursor);

        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });

        // Add hover effect for interactive elements
        const interactiveElements = document.querySelectorAll('a, button, .service-card, .insta-post');
        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.classList.add('cursor-hover');
            });
            el.addEventListener('mouseleave', () => {
                cursor.classList.remove('cursor-hover');
            });
        });
    }

    // 9. Real-time Date Display
    const updateDate = () => {
        const dateElement = document.querySelector('.current-date');
        if (dateElement) {
            const now = new Date();
            const options = {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            };
            dateElement.textContent = now.toLocaleDateString('uk-UA', options);
        }
    };
    updateDate();
    setInterval(updateDate, 60000); // Update every minute

    // 10. Lazy Loading Images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.classList.add('loaded');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // 11. Chocolate Counter Animation
    const startCounters = () => {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const increment = target / 100;
            let current = 0;

            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.textContent = Math.ceil(current);
                    setTimeout(updateCounter, 20);
                } else {
                    counter.textContent = target;
                }
            };
            updateCounter();
        });
    };

    // Start counters when section is visible
    const counterSection = document.querySelector('.stats-section');
    if (counterSection) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startCounters();
                    counterObserver.unobserve(entry.target);
                }
            });
        });
        counterObserver.observe(counterSection);
    }

    // 12. Chocolate Temperature Effect (Seasonal)
    const updateChocolateTemp = () => {
        const tempElement = document.querySelector('.chocolate-temp');
        if (tempElement) {
            const hour = new Date().getHours();
            let temp = 'чорна';

            if (hour >= 6 && hour < 12) temp = 'молочна';
            else if (hour >= 12 && hour < 18) temp = 'темна';
            else if (hour >= 18 && hour < 22) temp = 'біла';

            tempElement.textContent = temp;
            tempElement.style.color = temp === 'молочна' ? '#E28B42' :
                                   temp === 'темна' ? '#8B4513' :
                                   temp === 'біла' ? '#F5DEB3' : '#000';
        }
    };
    updateChocolateTemp();
});

// 13. Keyboard Navigation Support
document.addEventListener('keydown', (e) => {
    // Close menu on Escape
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('navMenu');
        if (navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            document.body.style.overflow = 'visible';
        }
    }
});

// 14. Performance Monitoring
window.addEventListener('load', () => {
    if ('performance' in window) {
        const timing = performance.getEntriesByType('navigation')[0];
        console.log('Page loaded in:', timing.domContentLoadedEventEnd - timing.fetchStart, 'ms');
    }
});