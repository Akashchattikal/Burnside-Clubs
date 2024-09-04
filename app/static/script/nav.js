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

    img.classList.toggle('active'); 
    buttons.forEach(button => button.classList.toggle('show')); 
}

document.querySelectorAll('.custom-flash-message').forEach(function(msg) {
    setTimeout(function() {
        msg.style.transition = 'transform 0.5s ease-out, opacity 0.5s ease-out'; 
        msg.style.transform = 'translateX(-100%)'; // Slide out to the left
        msg.style.opacity = '0'; // Fade out
        setTimeout(function() {
            msg.style.display = 'none'; // Hide the element after the transition
        }, 500); // Match this time with the CSS transition duration
    }, 3000); // Wait 3 seconds before starting the slide-out
});

