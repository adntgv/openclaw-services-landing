// Mobile Menu Toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileMenuToggle.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
        mobileMenuToggle.setAttribute('aria-expanded', navLinks.classList.contains('active'));
    });
}

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            mobileMenuToggle.textContent = '☰';
            mobileMenuToggle.setAttribute('aria-expanded', 'false');
        }
    });
});

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed nav
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Contact Form Handling
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(contactForm);
        const data = {
            name: formData.get('name'),
            contact: formData.get('contact'),
            service: formData.get('service'),
            message: formData.get('message')
        };
        
        // Create Telegram message
        const telegramMessage = `
🆕 Новый запрос с OpenClaw Services

👤 Имя: ${data.name}
📱 Контакт: ${data.contact}
🛠️ Услуга: ${getServiceName(data.service)}

💬 Сообщение:
${data.message}
        `.trim();
        
        try {
            // Send to Telegram via bridge API (if available)
            const response = await fetch('http://127.0.0.1:18800/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer X_K6rjUFN1YGNUHXWxRWlA1iCNwrD1sGoYD_OMQNMKM'
                },
                body: JSON.stringify({
                    chat_id: '6454712844', // Aidyn's Telegram ID
                    text: telegramMessage
                })
            });
            
            if (response.ok) {
                showSuccess('Запрос отправлен! Ответим в течение 24 часов.');
                contactForm.reset();
            } else {
                throw new Error('API error');
            }
        } catch (error) {
            // Fallback: open Telegram with pre-filled message
            const telegramUrl = `https://t.me/adntgv?text=${encodeURIComponent(telegramMessage)}`;
            window.open(telegramUrl, '_blank');
            showSuccess('Открыли Telegram. Отправьте сообщение для связи.');
        }
    });
}

function getServiceName(value) {
    const services = {
        'whatsapp': 'WhatsApp Business',
        '2gis': 'Парсер 2GIS',
        'telegram': 'Telegram Бот',
        'browser': 'Браузерная Автоматизация',
        'openclaw': 'OpenClaw "Под Ключ"',
        'content': 'Контент-Автоматизация',
        'custom': 'Кастомное Решение'
    };
    return services[value] || value;
}

function showSuccess(message) {
    // Create success notification
    const notification = document.createElement('div');
    notification.className = 'notification success';
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">✓</span>
            <span class="notification-message">${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Scroll-based animations (optional - reveal on scroll)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe service cards, case cards, pricing cards
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.service-card, .case-card, .pricing-card, .audience-card, .trust-item, .faq-item');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });
});

// Add active state to navigation based on scroll position
let scrollTicking = false;
window.addEventListener('scroll', () => {
    if (!scrollTicking) {
        window.requestAnimationFrame(() => {
            const sections = document.querySelectorAll('section[id]');
            const scrollY = window.pageYOffset;

            sections.forEach(section => {
                const sectionHeight = section.offsetHeight;
                const sectionTop = section.offsetTop - 100;
                const sectionId = section.getAttribute('id');
                const navLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);

                if (navLink) {
                    if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                        navLink.classList.add('active');
                    } else {
                        navLink.classList.remove('active');
                    }
                }
            });
            scrollTicking = false;
        });
        scrollTicking = true;
    }
});

