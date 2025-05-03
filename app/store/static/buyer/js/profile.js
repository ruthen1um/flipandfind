// Активные кнопки в профиле покупателя
function goToAddress() {
    alert('Переход к адресу...');
}

function goToPurchases() {
    alert('Переход к покупкам...');
}

function rateProduct(element, ratingValue) {
    // Find the parent .bracelet element
    const braceletDiv = element.closest('.bracelet');

    // Check if the braceletDiv exists
    if (braceletDiv) {
        // Add a class to hide the bracelet card
        braceletDiv.style.opacity = '0'; // Start fading out
        setTimeout(() => {
            braceletDiv.style.display = 'none'; // Then hide
        }, 300); // Match the transition duration (0.3s)
    }
}
