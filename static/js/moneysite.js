var closes = document.getElementsByClassName("close");

for (let i = 0; i < closes.length; i++) {
    closes[i].addEventListener("click", function (e) {
        if (this.parentNode.classList.contains("messages")) {
            this.parentNode.parentNode.style.display = "none";
        }
        else {
            this.parentNode.style.display = "none";
        }
    });

}