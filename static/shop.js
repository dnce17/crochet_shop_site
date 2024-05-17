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

function showOutcome(ctnrCls, outcomeCls, msg, index) {
    let ctnr = document.querySelector(`.${ctnrCls}`);

    outcomeBg = createEleWithCls("div", ["outcome-bg"]);
    outcomeMsgCtnr = createEleWithCls("div", ["msg-ctnr", "outcome-msg-ctnr", outcomeCls]);
    outcomeMsg = createEleWithCls("p", ["msg"]);
    closeBtn = createEleWithCls("button", ["remove-btn", "close-btn"]);

    outcomeMsg.innerText = msg;
    closeBtn.innerText = "Close";
    closeBtn.addEventListener("click", function() {
        outcomeBg.remove();
    });

    outcomeMsgCtnr.appendChild(outcomeMsg);
    outcomeMsgCtnr.appendChild(closeBtn);
    outcomeBg.appendChild(outcomeMsgCtnr);

    ctnr.insertBefore(outcomeBg, ctnr.children[index]);
}


socket.on("successfully added to cart", function() {
    showOutcome("shop", "outcome-msg-ctnr--success", "SUCCESS: Item has been added to cart.", 0);
});

socket.on("not enough stock", function() {
    showOutcome("shop", "outcome-msg-ctnr--no-stock", "Amount currently in your cart is the max stock available");
});

addToCart();