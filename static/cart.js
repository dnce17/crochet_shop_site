function currencyToNum(value) {
    return parseFloat(value.replace("$", ""));
}

function deleteCartItem() {
    const deleteBtns = document.querySelectorAll(".cart__item-delete-btn");
    const cartItemNames = document.querySelectorAll(".cart__item-name");
    
    for (let i = 0; i < deleteBtns.length; i++) {
        deleteBtns[i].addEventListener("click", function() {
            socket.emit("delete cart item", {
                "name": cartItemNames[i].innerText,
                "index": i
            });
        });
    }
}

function deleteChild(ele) {
    ele.classList.toggle("deleted");
    // Gets rid of children by replacing content with #text node
    ele.textContent = "";
}

function updateSubtotal(pricesList) {
    let newSubtotal = 0;
    for (let i = 0; i < pricesList.length; i++) {
        newSubtotal = newSubtotal + currencyToNum(pricesList[i].innerText);
    }

    return "$" + newSubtotal.toFixed(2);
}

// Sockets
socket.on("delete cart item", function(index) {
    let cartItems = document.querySelectorAll(".cart__item");
    let subtotal = document.querySelector(".cart__subtotal-amt");

    deleteChild(cartItems[index])

    // Get prices AFTER undesired item is deleted
    let cartPrices = document.querySelectorAll(".cart__item-price");
    subtotal.innerText = updateSubtotal(cartPrices)

    // Reload the page once the cart reaches 0 items
    if (subtotal.innerText == "$0.00") {
        location.reload();
    }
});

deleteCartItem();