function main() {
    toggleNav();
    previewImg()
}

function toggleNav() {
    const navToggle = document.querySelector(".nav__toggle");
    const nav = document.querySelector(".nav");

    navToggle.addEventListener("click", () => {
        // console.log("test");
        nav.classList.toggle("visible");
    });
}

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
        // imgPreview.src = `/static/img/shop${}`
    });
}

main();