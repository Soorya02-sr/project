document.addEventListener("DOMContentLoaded", function() {
    const quadrants = ["quadrant_1_tooth", "quadrant_2_tooth", "quadrant_3_tooth", "quadrant_4_tooth"];

    quadrants.forEach(quadrant => {
        let container = document.getElementById(`id_${quadrant}`);
        container.style.display = "none"; // Hide original input

        let gridContainer = document.createElement("div");
        gridContainer.className = "tooth-grid";
        
        for (let i = 1; i <= 8; i++) {
            let button = document.createElement("button");
            button.innerText = i;
            button.className = "tooth-button";
            button.onclick = function(e) {
                e.preventDefault();
                document.getElementById(`id_${quadrant}`).value = i; // Set selected tooth number
                gridContainer.querySelectorAll(".tooth-button").forEach(btn => btn.classList.remove("selected"));
                button.classList.add("selected"); // Highlight selected button
            };
            gridContainer.appendChild(button);
        }

        container.parentElement.appendChild(gridContainer);
    });
});
