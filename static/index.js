function initPage() {
    toggleNav();
    closeMsg();
    socket.emit("display cart item count");
}

function toggleNav() {
    const navToggle = document.querySelector(".nav__toggle");
    const nav = document.querySelector(".nav");

    navToggle.addEventListener("click", () => {
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

function createLabel(clsArr, labelFor, text) {
    let label = createEleWithCls("label", clsArr);
    label.htmlFor = labelFor;
    label.innerText = text;

    return label;
}

function createInput(inputType, inputName, clsArr) {
    let input = createEleWithCls("input", clsArr);
    input.setAttribute("type", inputType);
    input.name = inputName;
    input.id = inputName

    return input;
}

function createTextArea(textAreaName, rowCount, clsArr) {
    let textArea = createEleWithCls("textarea", clsArr);
    textArea.name = textAreaName;
    textArea.id = textAreaName;
    textArea.rows = rowCount;

    return textArea;
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


initPage();