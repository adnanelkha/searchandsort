console.log("JavaScript is connected!");

const dropZone = document.getElementById("drag-and-drop");
const output = document.getElementById("myText");

if (!dropZone || !output) {
    console.error("Could not find the drop zone or file display.");
} else {
    console.log("Drop zone found!");
    dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    dropZone.addEventListener("drop", (event) => {
        event.preventDefault();
        const files = Array.from(event.dataTransfer.files);
        if (files.length === 0) {
            output.textContent = "No files detected.";
            return;
        }
        output.textContent = files.map(file => file.name).join(", ");
        console.log("Files dropped:", files);
    });

    window.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    window.addEventListener("drop", (event) => {
        event.preventDefault();
    });
}
