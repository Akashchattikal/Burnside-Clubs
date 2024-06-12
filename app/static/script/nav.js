const navLinks = document.querySelectorAll('.nav_link');

let path = location.pathname; /* Gets URL of current page, stores in path */
let linkID;


if (path == "/") {
    linkID = "home"
} else if (path == "#") {
    linkID = "clubs"
} else if (path == "#") {
    linkID = "teacher"
} else if (path == "#") {
    linkID = "admin"
}

document.getElementById(linkID).style.fontWeight = "bold ";

