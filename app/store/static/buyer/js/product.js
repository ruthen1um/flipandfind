// Переключение изображений
function changeImage(element) {
    const mainImage = document.getElementById('mainImage');
    mainImage.src = element.src;

    document.querySelectorAll('.product-gallery__thumbnail')
        .forEach(img => img.classList.remove('product-gallery__thumbnail--active'));

    element.classList.add('product-gallery__thumbnail--active');
}

// Табы
function openTab(tabName) {
    const tabcontent = document.querySelectorAll('.product-tabs__content');
    const tablinks = document.querySelectorAll('.product-tabs__tab');

    tabcontent.forEach(content => content.classList.remove('product-tabs__content--active'));
    tablinks.forEach(link => link.classList.remove('product-tabs__tab--active'));

    document.getElementById(tabName).classList.add('product-tabs__content--active');
    event.currentTarget.classList.add('product-tabs__tab--active');
}

// Корзина: добавление товара
document.addEventListener('DOMContentLoaded', () => {
    const cartButton = document.querySelector('.product-info__cart-btn');
    const cartCounters = document.querySelectorAll('.user-nav__cart-counter');

    if (!cartButton) return;

    const productId = cartButton.dataset.productId;

    cartButton.addEventListener('click', (event) => {
        // If already "Перейти в корзину", just redirect
        if (cartButton.textContent.trim() === 'Перейти в корзину') {
            window.location.href = '/cart';
            return;
        }

        // Prevent double clicks
        if (cartButton.classList.contains('adding')) return;
        cartButton.classList.add('adding');

        fetch(`/api/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                // Update cart counters
                cartCounters.forEach(counter => {
                    let count = parseInt(counter.textContent || '0');
                    counter.textContent = count + 1;
                    counter.classList.add('bounce');
                    setTimeout(() => counter.classList.remove('bounce'), 300);
                });

                // Change button text
                cartButton.textContent = 'Перейти в корзину';
            } else {
                alert('Не удалось добавить товар в корзину.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при добавлении товара в корзину.');
        })
        .finally(() => {
            cartButton.classList.remove('adding');
        });
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
