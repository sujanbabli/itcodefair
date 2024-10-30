// script.js
document.addEventListener("DOMContentLoaded", () => {
    // Retrieve the selected doctor's name from localStorage
    const doctorName = localStorage.getItem("selectedDoctorName");

    // Check if a doctor name exists in localStorage
    if (doctorName) {
        // Update the title and doctor name fields with the selected doctor’s name
        document.getElementById("selected-doctor-name").textContent = `Selected Doctor: ${doctorName}`;
        document.getElementById("doctor-name").textContent = doctorName;
    }
});


document.addEventListener("DOMContentLoaded", () => {
    // Select the form's submit button (Next button)
    const nextButton = document.querySelector(".next-button");

    // Add click event listener to the Next button
    nextButton.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent the form from submitting
        window.location.href = "appointment-date.html"; // Redirect to the next page
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // Initialize Flatpickr on the date input
    const dateInput = document.getElementById("appointment-date");
    flatpickr(dateInput, {
        altInput: true,
        altFormat: "F j, Y",
        dateFormat: "Y-m-d",
        minDate: "today"
    });

    // Next button functionality
    document.getElementById("next-button").addEventListener("click", () => {
        const selectedDate = dateInput.value;
        const selectedTime = document.getElementById("time").value;

        if (selectedDate) {
            sessionStorage.setItem("appointmentDate", selectedDate);
            sessionStorage.setItem("appointmentTime", selectedTime);

            window.location.href = "appointment-confirmation.html";
        } else {
            alert("Please select a date before proceeding.");
        }
    });
});
document.addEventListener("DOMContentLoaded", () => {
    // Retrieve the selected date and time from sessionStorage
    const selectedDate = sessionStorage.getItem("appointmentDate");
    const selectedTime = sessionStorage.getItem("appointmentTime");

    // Check if date and time exist in sessionStorage
    if (selectedDate && selectedTime) {
        document.getElementById("appointment-date").textContent = selectedDate;
        document.getElementById("appointment-time").textContent = selectedTime;
    } else {
        document.getElementById("appointment-date").textContent = "No date selected";
        document.getElementById("appointment-time").textContent = "No time selected";
    }
});




