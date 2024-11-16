document.addEventListener("DOMContentLoaded", function() {
    const dateField = document.getElementById("id_date");
    const timeSlotsContainer = document.getElementById("time-slots");

    // Función para actualizar las horas disponibles
    function updateAvailableTimes(date) {
        const serviceId = document.getElementById("id_service").value;

        // Solicitar las horas disponibles y reservadas desde el servidor
        fetch(`/get-available-times-ajax/?date=${date}&service_id=${serviceId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                const reservedTimes = data.reserved_times;
                const availableTimes = data.available_times;

                // Limpiar las opciones anteriores
                timeSlotsContainer.innerHTML = '';

                // Obtener la hora actual
                const now = new Date();
                const currentHour = now.getHours();
                const currentMinutes = now.getMinutes();

                // Crear las opciones de hora
                availableTimes.forEach(time => {
                    const timeLabel = document.createElement("label");
                    const timeRadio = document.createElement("input");
                    timeRadio.type = "radio";
                    timeRadio.name = "time";
                    timeRadio.value = time;
                    timeRadio.classList.add("form-check-input");

                    timeLabel.classList.add("form-check-label");
                    timeLabel.textContent = time;

                    const colDiv = document.createElement("div");
                    colDiv.classList.add("col-md-2");

                    const checkDiv = document.createElement("div");
                    checkDiv.classList.add("form-check");

                    checkDiv.appendChild(timeRadio);
                    checkDiv.appendChild(timeLabel);

                    colDiv.appendChild(checkDiv);
                    timeSlotsContainer.appendChild(colDiv);

                    // Desactivar y ocultar horas pasadas
                    const timeParts = time.split(":");
                    const hour = parseInt(timeParts[0]);
                    const minutes = parseInt(timeParts[1]);

                    if (hour < currentHour || (hour === currentHour && minutes <= currentMinutes)) {
                        timeRadio.disabled = true;
                        // Ocultar la hora pasada
                        timeRadio.parentElement.style.display = "none";
                    }

                    // Desactivar y ocultar horas ya reservadas
                    if (reservedTimes.includes(time)) {
                        timeRadio.disabled = true;
                        // Ocultar la hora reservada
                        timeRadio.parentElement.style.display = "none";
                    }
                });

                // Si no hay horas disponibles, mostrar un mensaje
                if (timeSlotsContainer.innerHTML === '') {
                    const noTimesMessage = document.createElement("p");
                    noTimesMessage.textContent = "No hay horas disponibles para esta fecha.";
                    timeSlotsContainer.appendChild(noTimesMessage);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Detectar cambio en la fecha seleccionada
    dateField.addEventListener("change", function() {
        const selectedDate = dateField.value;
        if (selectedDate) {
            updateAvailableTimes(selectedDate);
        }
    });
});
