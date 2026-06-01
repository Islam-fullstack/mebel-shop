// Page Loader
window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById('page-loader')?.classList.add('hidden');
    }, 800);
});

// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 20);
});

// Mobile menu
const navToggle = document.getElementById('nav-toggle');
const mobileMenu = document.getElementById('mobile-menu');
navToggle?.addEventListener('click', () => {
    mobileMenu?.classList.toggle('open');
});

// Auto-dismiss toasts
const toasts = document.querySelectorAll('.toast');
toasts.forEach(toast => {
    setTimeout(() => {
        toast.style.animation = 'slide-out-right 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
});

// CSRF token helper
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
           document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || '';
}

// Add to cart AJAX
document.querySelectorAll('[data-add-cart]').forEach(btn => {
    btn.addEventListener('click', async function(e) {
        e.preventDefault();
        const productId = this.dataset.addCart;
        const qty = document.querySelector(`[data-qty="${productId}"]`)?.value || 1;
        const originalContent = this.innerHTML;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        this.disabled = true;

        try {
            const res = await fetch(`/savat/qoshish/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `quantity=${qty}`,
            });
            const data = await res.json();
            if (data.success) {
                showToast(data.message, 'success');
                updateCartBadge(data.cart_count);
                this.innerHTML = '<i class="fas fa-check"></i> Qo\'shildi';
                setTimeout(() => { this.innerHTML = originalContent; this.disabled = false; }, 2000);
            }
        } catch (err) {
            this.innerHTML = originalContent;
            this.disabled = false;
            showToast('Xatolik yuz berdi', 'error');
        }
    });
});

// Update cart AJAX
document.querySelectorAll('[data-cart-action]').forEach(btn => {
    btn.addEventListener('click', async function() {
        const itemId = this.dataset.itemId;
        const action = this.dataset.cartAction;
        try {
            const res = await fetch(`/savat/yangilash/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `action=${action}`,
            });
            const data = await res.json();
            if (data.success) {
                updateCartBadge(data.cart_count);
                location.reload();
            }
        } catch (err) {
            showToast('Xatolik yuz berdi', 'error');
        }
    });
});

function updateCartBadge(count) {
    let badge = document.getElementById('cart-badge');
    if (count > 0) {
        if (!badge) {
            const btn = document.querySelector('.cart-btn');
            if (btn) {
                badge = document.createElement('span');
                badge.id = 'cart-badge';
                badge.className = 'cart-badge';
                btn.appendChild(badge);
            }
        }
        if (badge) badge.textContent = count;
    } else if (badge) {
        badge.remove();
    }
}

function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    toast.innerHTML = `<i class="fas ${icon}"></i><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 4000);
}

// Quantity controls
document.querySelectorAll('.qty-increase').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.target;
        const input = document.getElementById(target) || document.querySelector(`[data-qty-field="${target}"]`);
        if (input) input.value = parseInt(input.value || 1) + 1;
    });
});
document.querySelectorAll('.qty-decrease').forEach(btn => {
    btn.addEventListener('click', () => {
        const target = btn.dataset.target;
        const input = document.getElementById(target) || document.querySelector(`[data-qty-field="${target}"]`);
        if (input && parseInt(input.value) > 1) input.value = parseInt(input.value) - 1;
    });
});

// Scroll reveal
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Star rating
document.querySelectorAll('.star-rating-input').forEach(container => {
    const stars = container.querySelectorAll('.star-input');
    const input = container.querySelector('input[name="rating"]');
    stars.forEach((star, i) => {
        star.addEventListener('mouseover', () => {
            stars.forEach((s, j) => s.classList.toggle('active', j <= i));
        });
        star.addEventListener('click', () => {
            if (input) input.value = i + 1;
            stars.forEach((s, j) => s.classList.toggle('selected', j <= i));
        });
    });
    container.addEventListener('mouseleave', () => {
        const val = parseInt(input?.value || 0);
        stars.forEach((s, j) => s.classList.toggle('active', j < val));
    });
});

// Number formatting
document.querySelectorAll('.format-price').forEach(el => {
    const num = parseFloat(el.textContent.replace(/\s/g, ''));
    if (!isNaN(num)) el.textContent = num.toLocaleString('uz-UZ') + ' so\'m';
});
