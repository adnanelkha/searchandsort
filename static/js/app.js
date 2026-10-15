console.log("JS is connected");

const dropZone = document.getElementById("drag-and-drop");
const output = document.getElementById("myText");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("site-search");
const searchResult = document.getElementById("search-result");
const algorithmSelect = document.getElementById("algorithm");
const fileInput = document.getElementById("file-input");
let searchableData = [];

if (dropZone && output && fileInput) {
    dropZone.addEventListener("click", () => {
        fileInput.click();
    });

    dropZone.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            fileInput.click();
        }
    });

    fileInput.addEventListener("change", async () => {
        await handleFile(fileInput.files[0]);
    });

    dropZone.addEventListener("dragover", (event) => {
        event.preventDefault();
        dropZone.classList.add("drag-over");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("drag-over");
    });

    dropZone.addEventListener("drop", async (event) => {
        event.preventDefault();
        dropZone.classList.remove("drag-over");
        await handleFile(event.dataTransfer.files[0]);
    });

    async function handleFile(file) {
        if (!file) return;

        if (!file.name.toLowerCase().endsWith(".csv")) {
            output.textContent = "Please select a CSV file.";
            fileInput.value = "";
            return;
        }

        try {
            output.textContent = "Reading file...";

            const contents = await file.text();

            searchableData = contents
                .replace(/^\uFEFF/, "")
                .split(/\r?\n/)
                .flatMap(row => row.split(","))
                .map(value => value.trim())
                .filter(value => value.length > 0);

            if (searchableData.length === 0) {
                output.textContent = "The CSV file is empty.";
                return;
            }

            const response = await fetch("/upload-data", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    values: searchableData
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Upload failed.");
            }

            output.textContent = file.name;
            console.log("Uploaded data:", result);
        } catch (error) {
            output.textContent = error.message || "Could not read the file.";
            console.error("File error:", error);
        }
    }
}

window.addEventListener("dragover", (event) => {
    event.preventDefault();
});

window.addEventListener("drop", (event) => {
    if (!dropZone || !dropZone.contains(event.target)) {
        event.preventDefault();
    }
});

if (searchForm && searchInput && searchResult) {
    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const searchTerm = searchInput.value.trim();
        const selectedAlgorithm = algorithmSelect?.value;

        if (!searchTerm) {
            searchResult.textContent = "Please enter something to search for.";
            return;
        }

        if (!selectedAlgorithm || !["binary", "linear"].includes(selectedAlgorithm)) {
            searchResult.textContent = "Please select a search algorithm.";
            return;
        }

        if (searchableData.length === 0) {
            searchResult.textContent = "Please upload a CSV file first.";
            return;
        }

        searchResult.textContent = "Searching...";

        try {
            const response = await fetch("/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    search_term: searchTerm,
                    algorithm: selectedAlgorithm
                })
            });

            const result = await response.json();

            if (!response.ok) {
                searchResult.textContent = result.error || "Search failed.";
                return;
            }

            if (result.index === -1) {
                searchResult.textContent = "Item not found.";
            } else {
                searchResult.textContent = `Item found at index ${result.index}.`;
            }
        } catch (error) {
            searchResult.textContent = "Could not connect to the server.";
            console.error("Search error:", error);
        }
    });
}