// Script for interactivity
document.getElementById("button1").addEventListener("click", () => {
    document.getElementById("outputArea").textContent = "Button 1 clicked!";
});

document.getElementById("button2").addEventListener("click", () => {
    document.getElementById("outputArea").textContent = "Button 2 clicked!";
});

document.getElementById("button3").addEventListener("click", () => {
    const userInput = document.getElementById("textInput").value;
    document.getElementById("outputArea").textContent = `You entered: ${userInput}`;
});

document.getElementById("button4").addEventListener("click", () => {
    document.getElementById("outputArea").textContent = "Button 4 clicked!";
});
