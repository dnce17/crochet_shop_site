function previewImg() {
    let imgUpload = document.querySelector(".img-upload");
    let imgPreview = document.querySelector(".img-preview");

    imgUpload.addEventListener("change", () => {
        let file = imgUpload.files[0];
        if (file) {
            imgPreview.src = URL.createObjectURL(file);
            if (imgPreview.classList.contains("hidden")) {
                imgPreview.classList.remove("hidden");
            }
        }
    });
}

previewImg();