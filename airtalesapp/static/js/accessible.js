document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const toggleAccessibility = document.getElementById("access-button");

    // Check localStorage and apply accessibility mode
    const isAccessible = localStorage.getItem("accessible") === "true";
    if(isAccessible){
        body.classList.add("accessible");
        toggleAccessibility.textContent = "Disable accessiblity";
    } else {
        toggleAccessibility.textContent = "Enable accessiblity";
    }

    toggleAccessibility.addEventListener("click", () => {
        body.classList.toggle("accessible");
        
        const isCurrentlyAccessible = body.classList.contains("accessible");
        localStorage.setItem("accessible", isCurrentlyAccessible);

        if(isCurrentlyAccessible){
            toggleAccessibility.textContent = "Disable accessibility";
        } else {
            toggleAccessibility.textContent = "Enable accessibility";
        }

    });
});
