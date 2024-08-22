const navLinks = document.querySelectorAll('.nav_link');

let path = location.pathname; /* Gets URL of current page, stores in path */
let linkID;


if (path == "/") {
    linkID = "home"
} else if (path == "/clubs") {
    linkID = "clubs"
} else if (path == "/teach_access") {
    linkID = "teacher"
} else if (path == "/admin_access") {
    linkID = "admin"
}

document.getElementById(linkID).style.fontWeight = "bold ";

function toggleButtons() {
    const buttons = document.querySelectorAll('.defualt_use');
    buttons.forEach(button => {
        button.classList.toggle('show');
    });
    }


function toggleButtons() {
    const img = document.querySelector('.default_si');
    const buttons = document.querySelectorAll('.defualt_use');

    img.classList.toggle('active'); // Toggle the active class to apply the border
    buttons.forEach(button => button.classList.toggle('show')); // Show/hide the buttons
}

