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
    const closeBtn = document.querySelector(".remove-btn");

    if (closeBtn != null) {
        closeBtn.addEventListener("click", function() {
            msgCtnr.classList.toggle("d-none");
        });
    }
}

socket.on("display cart item count", function(cartCount) {
    let amt = document.querySelector(".cart-amt");
    amt.innerText = cartCount;
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