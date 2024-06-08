function addRadioChangeEvt() {
    let radios = document.querySelectorAll(".form__radio-option");

    // radios.forEach((radio) => {
    //     radio.addEventListener("change", function() {
    //         // Validate that user did not alter values in developer tool
    //         socket.emit("validate radios", radio.value);
    //     });
    // });

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
    let disabledItems = document.querySelectorAll(".form__item--disabled");
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

// Idea 1 - Have the correct request form appear and the other one disappear
// socket.on("add correct request form element", function(data) {
//     // For existing pattern and own idea
//     let requestForm = document.querySelector(".request");
//     let radioQ = document.querySelector(".form__radio-question");
//     let ctnr = createEleWithCls("div", ["form__item"]);
//     let label;
//     let formEle;

//     if (data == "existing pattern") {
//         label = createLabel(["request__label"], "pattern-link", "Link for an Existing Pattern");
//         formEle = createInput("text", "pattern-link", ["input", "request__input"]);
//     }
//     else if (data == "own idea") {
//         label = createLabel(["request__label"], "idea-detail", "Details for Own Idea");
//         formEle = createTextArea("idea-detail", 10, ["input", "request__input"])
//     }

//     ctnr.appendChild(label);
//     ctnr.appendChild(formEle);
    
//     // Remove input/textarea box parent corresponding to radios, if present
//     let requestType = radioQ.nextElementSibling;
//     if (requestType.children[0].htmlFor == "pattern-link" || requestType.children[0].htmlFor == "idea-detail") {
//         requestType.remove();
//     }
    
//     // nextElementSibling so item always inserts AFTER radio question
//     // CAUTION: can't put requestType in 2nd parameter as requestType might get removed
//     requestForm.insertBefore(ctnr, radioQ.nextElementSibling);
// });

addRadioChangeEvt();