document.getElementById('registerForm').addEventListener('submit', function(e) {
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirm_password').value.trim();

    if (password.length < 6) {
        alert("Password must be at least 6 characters.");
        e.preventDefault();
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        e.preventDefault();
        return;
    }
});
