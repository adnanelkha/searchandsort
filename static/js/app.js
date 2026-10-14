console.log("JS is connected");

const dropZone = document.getElementById("drag-and-drop");
const output = document.getElementById("myText");

let searchableData = [];

if (!dropZone || !output) {
    console.error("Could not find the drop zone or file display");
} else {
    console.log("Drop zone found");
    dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    dropZone.addEventListener("drop", async (event) => {
        event.preventDefault();
        const files = Array.from(event.dataTransfer.files);
        if (files.length === 0) {
            output.textContent = "No files detected";
            return;
        }

        const file = files[0];
        if (!file.name.toLowerCase().endsWith(".csv")) {
            output.textContent = "Please drop a CSV file";
            return;
        }

        try {
            const contents = await file.text();
            searchableData = contents
                .split(/\r?\n/) //split into rows
                .flatMap(row => row.split(",")) //splits rows at commas, combines into one array
                .map(value => value.trim()) //removes spaces around values
                .filter(value => value.length > 0); //removes empty values
            output.textContent = file.name;
            console.log("Searchable data:", searchableData);
            const response = await fetch("/upload-data", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    values: searchableData
                })
            });
            const result = await response.json();
            console.log("Flask response:", result);
        } catch (error) {
            output.textContent = "Could not read the file";
            console.error("File reading error:", error);
        }
    });

    window.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    window.addEventListener("drop", (event) => {
        event.preventDefault();
    });
}