/**
 * Financial Fraud Detection System - Homepage JavaScript
 */

// ===== NAVBAR SCROLL EFFECT =====
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ===== INTERSECTION OBSERVER FOR ANIMATIONS =====
document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.feature-card, .step-card, .testimonial-card, .stat-card').forEach(el => {
        observer.observe(el);
    });
});

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== DASHBOARD TAB SWITCHING =====
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        this.classList.add('active');
    });
});

// ===== COUNTER ANIMATION =====
function animateCounters() {
    document.querySelectorAll('.countup').forEach(counter => {
        const target = parseInt(counter.dataset.target);
        if (isNaN(target)) return;

        let current = 0;
        const increment = Math.ceil(target / 60);
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = current.toLocaleString();
        }, 30);
    });
}

// Run counters when page loads
document.addEventListener('DOMContentLoaded', animateCounters);

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', function(e) {
    // ESC to close popup
    if (e.key === 'Escape') {
        closeAuth();
    }

    // Ctrl+K to open auth
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        openAuthPopup();
    }
});

// ===== ACTIVE NAV LINK =====
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', function() {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.scrollY >= sectionTop) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-links a:not(.login-btn)').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// ===== TOOLTIP FOR STATS =====
document.querySelectorAll('.stat-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transition = 'transform 0.3s ease';
    });
});

// ===== LOGGING =====
console.log('🛡️ Fraud Detection System loaded successfully!');
console.log('📊 Tracking real-time fraud analytics...');