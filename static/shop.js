function addToCart() {
    const cartBtns = document.querySelectorAll(".shop__cart-btn");
    const items = document.querySelectorAll(".shop__img-title");
    
    for (let i = 0; i < cartBtns.length; i++) {
        cartBtns[i].addEventListener("click", function() {
            // console.log(items[i].innerText);
            socket.emit("add to cart", items[i].innerText)
        });
    }
}

addToCart();