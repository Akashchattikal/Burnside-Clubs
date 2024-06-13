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

