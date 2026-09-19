// ============================================================
// SUCCESS PAGE - JAVASCRIPT
// ============================================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('✅ Registration Success Page Loaded');

    // Show current date
    updateRegDate();

    // Create confetti
    createConfetti();

    // Start countdown
    startCountdown();
});

// ============================================================
// UPDATE REGISTRATION DATE
// ============================================================
function updateRegDate() {
    const dateEl = document.getElementById('regDate');
    if (dateEl) {
        const now = new Date();
        dateEl.textContent = now.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// ============================================================
// CREATE CONFETTI ANIMATION
// ============================================================
function createConfetti() {
    const container = document.getElementById('confetti');
    if (!container) return;

    const colors = ['#6C3CE1', '#00D4AA', '#FFB432', '#FF6B6B', '#8B6FE8'];
    const piecesCount = 60;

    for (let i = 0; i < piecesCount; i++) {
        const piece = document.createElement('div');
        piece.className = 'confetti-piece';

        const color = colors[Math.floor(Math.random() * colors.length)];
        const left = Math.random() * 100;
        const delay = Math.random() * 1.5;
        const duration = 2 + Math.random() * 2;
        const size = 6 + Math.random() * 6;

        piece.style.background = color;
        piece.style.left = left + '%';
        piece.style.width = size + 'px';
        piece.style.height = size + 'px';
        piece.style.animationDelay = delay + 's';
        piece.style.animationDuration = duration + 's';
        piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';

        container.appendChild(piece);
    }

    // Remove confetti after animation
    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

// ============================================================
// COUNTDOWN & AUTO REDIRECT
// ============================================================
function startCountdown() {
    const countdownEl = document.getElementById('countdown');
    const progressEl = document.getElementById('progressFill');

    if (!countdownEl || !progressEl) return;

    let seconds = 5;
    const totalSeconds = 5;
    const loginUrl = getLoginUrl();

    // Update every second
    const interval = setInterval(() => {
        seconds--;
        countdownEl.textContent = seconds;

        // Update progress
        const progress = ((totalSeconds - seconds) / totalSeconds) * 100;
        progressEl.style.width = progress + '%';

        if (seconds <= 0) {
            clearInterval(interval);
            window.location.href = loginUrl;
        }
    }, 1000);
}

// ============================================================
// GET LOGIN URL
// ============================================================
function getLoginUrl() {
    // Check for data attribute or default
    const el = document.querySelector('[data-login-url]');
    if (el) return el.dataset.loginUrl;
    return '/login/';
}

// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================
document.addEventListener('keydown', function (e) {
    // Press Enter to go to login
    if (e.key === 'Enter') {
        window.location.href = getLoginUrl();
    }

    // Press Escape to go to home
    if (e.key === 'Escape') {
        window.location.href = '/';
    }
});