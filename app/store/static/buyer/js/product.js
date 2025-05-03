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

// Размеры товара
document.addEventListener('DOMContentLoaded', () => {
    const baseLength = 21;
    const baseWidth = 6.5;
    const lengthElem = document.getElementById('length-value');
    const widthElem = document.getElementById('width-value');

    document.querySelectorAll('.product-info__size').forEach(item => {
        item.addEventListener('click', () => {
            document.querySelectorAll('.product-info__size')
                .forEach(i => i.classList.remove('product-info__size--active'));

            item.classList.add('product-info__size--active');

            const selectedSize = parseFloat(item.dataset.size);
            const scale = selectedSize / baseLength;

            lengthElem.textContent = (baseLength * scale).toFixed(1);
            widthElem.textContent = (baseWidth * scale).toFixed(1);
        });
    });
});

// Корзина
document.addEventListener('DOMContentLoaded', () => {
    const cartButton = document.querySelector('.product-page__cart-btn');
    const cartCounters = document.querySelectorAll('.user-nav__cart-counter');

    let cartCount = 0;

    cartButton.addEventListener('click', () => {
        if (cartButton.textContent.trim() === 'В корзину') {
            cartCount++;
            cartCounters.forEach(counter => {
                counter.textContent = cartCount;
                counter.classList.add('bounce');
                setTimeout(() => counter.classList.remove('bounce'), 300);
            });
            cartButton.textContent = 'Перейти в корзину';
        } else {
            window.location.href = '/cart';
        }
    });
});

