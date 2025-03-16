document.addEventListener("DOMContentLoaded", function () {
    let dayOffset = 0; // 0 = today, -1 = yesterday, and so on

    const previousArrow = document.getElementById("prev-day-btn");
    const nextArrow = document.getElementById("next-day-btn");

    document.querySelectorAll('[data-bs-slide-to]').forEach(button => {
        button.addEventListener('click', function () {
            dayOffset = parseInt(this.getAttribute('data-bs-slide-to')) || 0;
            console.log(`Button clicked! Loading offset: ${dayOffset}`);
            getTopEntry();
        });
    });

    function getTopEntry() {
        const url = '/top-entry/?offset=${encodeURIComponent(dayOffset)}';
        console.log(`Fetching: ${url}`);

        fetch(url)
            .then(response => response.json())
            .then(data => {
                updateCarousel(data);
                updateCarouselIndicator();
                updateArrowStates();
            })
            .catch(error => console.error("Error getting top entry: ", error ));
    }

    function updateCarousel(data) {
        document.getElementById("carousel_prompt").textContent = data.prompt_text || "No prompt yet";
        document.getElementById("top_entry").textContent = data.entry_text || "No entries available yet"
        document.getElementById("entry_likes").textContent = data.entry_likes || "0";
        document.getElementById("total_entries").textContent = data.total_entries || "0";
    }

    previousArrow.addEventListener("click", function () {
        if (dayOffset > 0) {
            dayOffset -= 1; // Move forward one day (closer to today)
            console.log(`Next button clicked! New offset: ${dayOffset}`);
            getTopEntry();
        }
    });

    nextArrow.addEventListener("click", function () {
        dayOffset += 1; // Go back one day
        console.log(`Previous button clicked! New offset: ${dayOffset}`);
        getTopEntry();
    });

    function updateCarouselIndicator() {
        document.querySelectorAll("[data-bs-slide-to]").forEach((el, index) => {
            el.classList.toggle("active", index === dayOffset);
        });
    }

    function updateArrowStates() {
        previousArrow.disabled = dayOffset < 1;
        nextArrow.disabled = dayOffset >= 6;
    }

    getTopEntry();

});