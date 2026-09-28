const pageState = {
    url: window.location.href,
    title: document.title,
    text: document.body.innerText.substring(0, 5000)
};

console.log("Captured page state:", pageState);

fetch("http://127.0.0.1:8000/page-state", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(pageState)
})
.then(response => response.json())
.then(data => {
    console.log("Backend response:", data);
})
.catch(error => {
    console.error("Error sending page state:", error);
});