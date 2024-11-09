// static/js/script.js

function toggleTextBox() {
    const checkBox = document.getElementById("otherCheckbox");
    const textBox = document.getElementById("otherTextBox");
    textBox.style.display = checkBox.checked ? "block" : "none";
}

function toggleFeelingTextBox() {
    const checkBox = document.getElementById("otherFeelingCheckbox");
    const textBox = document.getElementById("otherFeelingTextBox");
    textBox.style.display = checkBox.checked ? "block" : "none";
}