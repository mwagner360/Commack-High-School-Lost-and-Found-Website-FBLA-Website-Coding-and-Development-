var menuBtn = document.querySelector(".menuToggle");
var nav = document.querySelector(".mainNav");

if (menuBtn) {
    menuBtn.addEventListener("click", function() {
        var isOpen = nav.classList.toggle("open");
        menuBtn.setAttribute("aria-expanded", isOpen);
    });
}

// let users of the website close flash messages
document.querySelectorAll(".flashClose").forEach(function(btn) {
    btn.addEventListener("click", function() {
        this.parentElement.remove();
    });
});
