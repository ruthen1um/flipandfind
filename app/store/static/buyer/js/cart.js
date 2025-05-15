document.addEventListener("DOMContentLoaded", function () {
    const summaryTotal = document.getElementById("summary-total");
    const summaryCount = document.getElementById("summary-product-count");

    document.querySelectorAll(".cart__quantity-button").forEach(button => {
        button.addEventListener("click", function () {
            const productDiv = this.closest(".cart__item");
            const productId = productDiv.dataset.productId;
            const quantitySpan = productDiv.querySelector(".cart__quantity");
            let quantity = parseInt(quantitySpan.textContent);

            if (this.classList.contains("cart__quantity-button--plus")) {
                quantity++;
            } else if (this.classList.contains("cart__quantity-button--minus") && quantity > 1) {
                quantity--;
            }

            fetch(`/api/cart/update/${productId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: `quantity=${quantity}`
            }).then(response => response.json())
              .then(data => {
                  if (data.status === "ok") {
                      quantitySpan.textContent = data.quantity;
                      productDiv.querySelector(".cart__price").textContent = `${data.line_total}₽`;
                      updateTotals();
                  } else if (data.status === "deleted") {
                      productDiv.remove();
                      updateTotals();
                  }
              });
        });
    });

    function updateTotals() {
        let total = 0;
        let count = 0;

        document.querySelectorAll(".cart__item").forEach(item => {
            const priceText = item.querySelector(".cart__price").textContent.replace("₽", "");
            total += parseInt(priceText);
            count += parseInt(item.querySelector(".cart__quantity").textContent);
        });

        summaryTotal.textContent = total;
        summaryCount.textContent = count;
    }
});

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
