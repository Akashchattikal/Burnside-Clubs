// Handle opening and closing of the photo popup
document.getElementById("myButton").addEventListener("click", function () {
    document.getElementById("myPopup").classList.add("show");
});

document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("myPopup").classList.remove("show");
});

window.addEventListener("click", function (event) {
    if (event.target === document.getElementById("myPopup")) {
        document.getElementById("myPopup").classList.remove("show");
    }
});

// Smooth scrolling to different sections of the page
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    const yOffset = -60; // Adjust this value based on your needs
    const y = section.getBoundingClientRect().top + window.pageYOffset + yOffset;

    window.scrollTo({
        top: y,
        behavior: 'smooth'
    });
}

// Toggle the visibility of forms for editing club details
function toggleEdit(formId) {
    var form = document.getElementById(formId);
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}

// Toggle the visibility of the fixed menu
function toggleMenu() {
    const menu = document.querySelector('.fix_menu');
    menu.classList.toggle('hidden');
}

// Handle delete functionality for notices and events
document.addEventListener("DOMContentLoaded", function () {
    // Attach event listeners to all delete buttons
    const deleteButtons = document.querySelectorAll(".delete_button");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent the default form submission

            const form = this.closest('form'); // Find the closest form element
            if (confirm("Are You Sure You Want To Delete This Item?")) {
                form.submit(); // Submit the form to delete the item
            }
        });
    });
});
