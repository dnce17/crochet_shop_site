function main() {
    toggleNav();
}

function toggleNav() {
    const navToggle = document.querySelector(".nav__toggle");
    const nav = document.querySelector(".nav");

    navToggle.addEventListener("click", () => {
        // console.log("test");
        nav.classList.toggle("visible");
    })
}

main();