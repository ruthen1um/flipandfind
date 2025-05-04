let currentPage = 1;
let loading = false;

function loadProducts(page) {
    if (loading) return;
    loading = true;

    fetch(`/api/catalog/?page=${page}`)
        .then(response => response.text())
        .then(html => {
            const grid = document.getElementsByClassName('products__grid')[1];
            grid.innerHTML += html;
            loading = false;
        });
}

function handleScroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const windowHeight = window.innerHeight;
    const bodyHeight = document.body.scrollHeight;

    if (scrollTop + windowHeight >= bodyHeight - 500) {
        loadProducts(currentPage + 1);
    }
}

loadProducts(1);
window.addEventListener('scroll', handleScroll);
