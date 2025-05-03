document.addEventListener('DOMContentLoaded', () => {
    // Load More functionality
    const loadMoreBtn = document.querySelector('.load-more-btn');
    const hiddenProducts = document.querySelectorAll('.products-section.hidden');

    if(loadMoreBtn) {
        loadMoreBtn.addEventListener('click', (e) => {
            e.preventDefault();
            hiddenProducts.forEach(section => {
                section.classList.remove('hidden');
            });
            loadMoreBtn.style.display = 'none';
        });
    }

    // Mobile Menu Toggle (добавьте иконку меню в HTML)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const categoryMenu = document.querySelector('.category-menu');

    if(mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            categoryMenu.classList.toggle('active');
        });
    }
});
