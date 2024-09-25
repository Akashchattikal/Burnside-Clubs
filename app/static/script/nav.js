// Highlight the correct navigation link based on the current path
const navLinks = document.querySelectorAll('.nav_link');
let path = location.pathname; // Gets URL of current page, stores in path
let linkID;

// Set the appropriate linkID based on the path
if (path == "/") {
    linkID = "home";
} else if (path == "/clubs") {
    linkID = "clubs";
} else if (path == "/teach/{{ current_user.get_teacher_id() }}") {
    linkID = "teach";
} else if (path == "{{ url_for('user', id=current_user.id) }}") {
    linkID = "dashboard";
} else if (path == "/admin_access") {
    linkID = "admin";
}

// Bold the current active link
if (linkID) {
    document.getElementById(linkID).style.fontWeight = "bold";
}

// Toggle buttons in the dropdown menu
function toggleButtons() {
    const buttons = document.querySelectorAll('.defualt_use');
    buttons.forEach(button => {
        button.classList.toggle('show');
    });
}

// Toggle the menu and arrow next to the profile image
function toggleProfileMenu() {
    const img = document.querySelector('.default_si');
    const menu = document.querySelector('.dropdown_menu');
    const arrow = document.getElementById('menu-arrow');

    img.classList.toggle('active');
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';

    // Toggle between down (▼) and up (▲) arrow
    if (menu.style.display === 'block') {
        arrow.textContent = '▲'; // Up arrow when menu is open
    } else {
        arrow.textContent = '▼'; // Down arrow when menu is closed
    }
}

// Flash message slide-out and fade-out animation
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
