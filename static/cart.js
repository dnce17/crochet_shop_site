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

function changeQty() {
    // Changes subtotal after changing qty
    let qtySelect = document.querySelectorAll(".qty");
    let cartItemNames = document.querySelectorAll(".cart__item-name");

    for (let i = 0; i < qtySelect.length; i++) {
        qtySelect[i].addEventListener("change", function(e) {
            newQty = e.target.value;
            socket.emit("update desired qty", {
                "name": cartItemNames[i].innerText, 
                "newQty": newQty
            });
        });
    }
}

function updateCartTotalItem() {
    let qtys = document.querySelectorAll(".desired-qty");
    let totalItem = document.querySelector(".cart__total-items");
        
    let itemCount = 0;
    for (let i = 0; i < qtys.length; i++) {
        itemCount += parseInt(qtys[i].innerText);
    }

    totalItem.innerText = `(${itemCount} items)`;
}

function updateCartSubtotal() {
    let cartPrices = document.querySelectorAll(".cart__item-price");
    let qtys = document.querySelectorAll(".desired-qty");

    let newSubtotal = 0;
    for (let i = 0; i < cartPrices.length; i++) {
        newSubtotal = updateSubtotal(newSubtotal, currencyToNum(cartPrices[i].innerText), parseInt(qtys[i].innerText))
    }

    return "$" + newSubtotal.toFixed(2);
}

function updateSubtotal(currentSubtotal, price, qty, operation="+") {
    if (operation == "+") {
        return currentSubtotal + (parseInt(price) * parseInt(qty));
    }
    else if (operation == "-") {
        return currentSubtotal - (parseInt(price) * parseInt(qty));
    }
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
    
    subtotal.innerText = updateCartSubtotal();
    updateCartTotalItem();

    // Reload the page once the cart reaches 0 items
    if (subtotal.innerText == "$0.00") {
        location.reload();
    }
});

socket.on("refresh pg", function() {
    location.reload();
})

deleteCartItem();
changeQty();