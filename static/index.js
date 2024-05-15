function main() {
    toggleNav();
    closeMsg();
    socket.emit("display cart item count");

    // MOVE FUNC to a add-stock.js
    previewImg()
}

function toggleNav() {
    const navToggle = document.querySelector(".nav__toggle");
    const nav = document.querySelector(".nav");

    navToggle.addEventListener("click", () => {
        // console.log("test");
        nav.classList.toggle("d-none");
    });
}

function closeMsg() {
    const msgCtnr = document.querySelector(".msg-ctnr");
    const closeBtn = document.querySelector(".close-btn");

    if (closeBtn != null) {
        closeBtn.addEventListener("click", function() {
            msgCtnr.classList.toggle("d-none");
        });
    }
}

function createEleWithCls(ele, clsArr) {
    let element = document.createElement(ele);

    for (let item of clsArr) {
        element.classList.add(item);
    }

    return element
}


socket.on("display cart item count", function(cartCount) {
    let amt = document.querySelector(".cart-amt");
    amt.innerText = cartCount;
});

socket.on("error", function(data) {
    let ctnr = document.querySelector(data["ctnr_name"]);
    let errMsgCtnr = document.querySelector(".error-msg-ctnr");

    if (errMsgCtnr == null) {   
        errMsgCtnr = createEleWithCls("div", ["msg-ctnr", "error-msg-ctnr"]);
        let errMsg = createEleWithCls("p", ["msg"]);

        errMsg.innerText = "ERROR: An issue has occurred. Please refresh the page and try again.";
        errMsgCtnr.appendChild(errMsg);

        ctnr.insertBefore(errMsgCtnr, ctnr.children[data["index"]]);
    };

    // Scroll back to top of page to see err msg
    window.scroll(0, 0);
});

// MOVE FUNC to a add-stock.js
function previewImg() {
    let imgUpload = document.querySelector(".img-upload");
    let imgPreview = document.querySelector(".img-preview")

    imgUpload.addEventListener("change", () => {
        let file = imgUpload.files[0]
        if (file) {
            imgPreview.src = URL.createObjectURL(file);
            if (imgPreview.classList.contains("hidden")) {
                imgPreview.classList.remove("hidden")
            }
        }
    });
}

main();