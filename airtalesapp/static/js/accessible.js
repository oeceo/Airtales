document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;

    // Select both accessibility buttons (text button and icon)
    const toggleAccessibility = document.querySelectorAll(".access-button");

    // Check localStorage and apply accessibility mode
    const isAccessible = localStorage.getItem("accessible") === "true";
    
    if(isAccessible){
        body.classList.add("accessible");
        toggleAccessibility.forEach(button => {
            if (button.classList.contains("nav-text")) {
                button.textContent = "Disable A11Y+"; // Update button text
            }
        }); 
    } else {
        toggleAccessibility.forEach(button => {
            if (button.classList.contains("nav-text")) {
                button.textContent = "Enable A11Y+";
            }
        });
    }

    // Add event listener for each of the two accessibility buttons
    toggleAccessibility.forEach(button => {
        button.addEventListener("click", () => {
            body.classList.toggle("accessible");
        
        const isCurrentlyAccessible = body.classList.contains("accessible");
        localStorage.setItem("accessible", isCurrentlyAccessible); // Store the button state

        toggleAccessibility.forEach(btn => {
            if (btn.classList.contains("nav-text")) {
                if (isCurrentlyAccessible) {
                    btn.textContent = "Disable A11Y+";
                } else {
                    btn.textContent = "Enable A11Y+";
                }
            }
        });
    });
});
})
