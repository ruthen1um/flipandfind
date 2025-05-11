let currentPage = 1;
let loading = false;

function loadProducts(page) {
    if (loading) return;
    loading = true;

    fetch(`/api/catalog/?page=${page}`)
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementsByClassName('products__grid')[1];
            if (!grid) return;

            data.products.forEach(product => {
                const card = document.createElement('div');
                card.className = 'product-card';

                card.innerHTML = `
                    <a href="${product.url}">
                        <img class="product-card__image" src="${product.primary_photo_url}" alt="${product.name}">
                    </a>
                    <p class="product-card__info">${product.seller_username}/${product.name}</p>
                    <p class="product-card__price">${product.price} p</p>
                    <p class="product-card__rating">${product.average_rating} ⭐ ${product.reviews_count} отзывов</p>
                `;

                grid.appendChild(card);
            });

            currentPage = page;

            if (!data.has_next) {
                window.removeEventListener('scroll', handleScroll);
            }

            loading = false;
        })
        .catch(err => {
            console.error("Failed to load products", err);
            loading = false;
        });
}

function handleScroll() {
    const scrollPosition = window.scrollY + window.innerHeight;
    const threshold = document.body.scrollHeight - 500;

    if (scrollPosition > threshold && !loading) {
        loadProducts(currentPage + 1);
    }
}

// Load initial page
loadProducts(1);

// Attach scroll handler
window.addEventListener('scroll', handleScroll);
