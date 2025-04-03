/*[TARGET]*/

let arrEqual = (a, b) => a.length === b.length && a.every((value, index) => value === b[index]);

let init = () => {
    const form = document.getElementById("login_form");
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const status = document.getElementById("status");
        const password = form.querySelector("input[type=password]");

        const encoder = new TextEncoder();
        const input_bytes = encoder.encode(password.value.substring(0, 32));
        const digest = megahash(input_bytes);

        if(arrEqual(digest, TARGET)) {
            status.innerText = "Password correct! Access granted!";
        } else {
            status.innerText = "Password incorrect!";
        }
    });
}

window.addEventListener('DOMContentLoaded', (event) => {
    init();
});