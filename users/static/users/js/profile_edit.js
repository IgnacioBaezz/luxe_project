document.addEventListener("DOMContentLoaded", function () {
    function enableField(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.removeAttribute("disabled");
        }
    }

    const editIcons = document.querySelectorAll(".edit-icon");
    editIcons.forEach(icon => {
        const fieldId = icon.nextElementSibling.querySelector("input, textarea").id;

        icon.addEventListener("click", function () {
            enableField(fieldId);
        });
    });

    const successMessage = document.getElementById("success-message");
    if (successMessage) {
        Swal.fire({
            icon: "success",
            title: "¡Perfil actualizado!",
            text: successMessage.dataset.message,
            timer: 2000,
            showConfirmButton: false
        });
    }
});
