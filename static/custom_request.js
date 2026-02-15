function addRadioChangeEvt() {
    let radios = document.querySelectorAll(".form__radio-option");

    for (let i = 0; i < radios.length; i++) {
        radios[i].addEventListener("change", function() {
            // Validate that user did not alter values in developer tool
            socket.emit("validate radios", {
                "value": radios[i].value,
                "index": i
            });
        });
    }
}


socket.on("undisable correct request form element", function(index) {
    let radioIdentifers = document.querySelectorAll(".radio-identifer");

    for (let i = 0; i < radioIdentifers.length; i++) {
        if (i == index) {
            radioIdentifers[i].classList.remove("form__item--disabled");
            radioIdentifers[i].lastElementChild.disabled = false;
        }
        else {
            radioIdentifers[i].classList.add("form__item--disabled");
            radioIdentifers[i].lastElementChild.disabled = true;
        }

    }
})


addRadioChangeEvt();