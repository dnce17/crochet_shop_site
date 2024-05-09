function currencyToNum(value) {
    return parseFloat(value.replace("$", ""));
}

function deleteCartItem() {
    let deleteBtns = document.querySelectorAll(".cart__item-delete-btn");
    let cartItemNames = document.querySelectorAll(".cart__item-name");
    
    for (let i = 0; i < deleteBtns.length; i++) {
        deleteBtns[i].addEventListener("click", function() {
            socket.emit("delete cart item", {
                "name": cartItemNames[i].innerText,
                "index": i
            });
        });
    }
}

function updateTotalItem() {
    let qtys = document.querySelectorAll(".desired-qty");
    let totalItem = document.querySelector(".cart__total-items");
        
    let itemCount = 0;
    for (let i = 0; i < qtys.length; i++) {
        itemCount += parseInt(qtys[i].innerText);
    }

    totalItem.innerText = `(${itemCount} items)`;
}

function updateSubtotal(pricesList, qtysList) {
    let cartItemNames = document.querySelectorAll(".cart__item-name");
    let newSubtotal = 0;
    for (let i = 0; i < pricesList.length; i++) {
        console.log(i);
        console.log(cartItemNames[i]);
        console.log(qtysList);
        console.log(qtysList[i]);
        newSubtotal = newSubtotal + (currencyToNum(pricesList[i].innerText) * parseInt(qtysList[i].innerText));
    }

    return "$" + newSubtotal.toFixed(2);
}

function deleteChild(ele) {
    ele.classList.toggle("deleted");
    // Gets rid of children by replacing content with #text node
    ele.textContent = "";
}


// Sockets
socket.on("delete cart item", function(index) {
    let cartItems = document.querySelectorAll(".cart__item");
    let subtotal = document.querySelector(".cart__subtotal-amt");

    deleteChild(cartItems[index]);

    // Get prices AFTER undesired item is deleted
    let cartPrices = document.querySelectorAll(".cart__item-price");
    let qtys = document.querySelectorAll(".desired-qty");
    subtotal.innerText = updateSubtotal(cartPrices, qtys)

    // Update total item count
    updateTotalItem();

    // Reload the page once the cart reaches 0 items
    if (subtotal.innerText == "$0.00") {
        location.reload();
    }
});

deleteCartItem();