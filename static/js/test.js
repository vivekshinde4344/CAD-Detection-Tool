document.getElementById("testForm").addEventListener("submit", function(e) {
    const inputs = document.querySelectorAll("#testForm input");
    for (const input of inputs) {
        if (input.value.trim() === "") {
            alert("All fields must be filled.");
            e.preventDefault();
            return;
        }
    }
});
