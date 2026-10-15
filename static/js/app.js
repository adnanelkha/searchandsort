console.log("JS is connected");

const dropZone = document.getElementById("drag-and-drop");
const output = document.getElementById("myText");

let searchableData = [];

if (!dropZone || !output) {
    console.error("Could not find the drop zone or file display", {
        dropZoneFound: !!dropZone,
        outputFound: !!output
    });
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


document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("search-form");
    console.log("Search form found:", searchForm);

    const searchInput = document.getElementById("site-search");
    const searchResult = document.getElementById("search-result");
    const dataTypeInput = document.getElementById("data-type");

    if (searchForm && searchInput && searchResult) {
        searchForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const searchTerm = searchInput.value.trim();

            if (searchTerm === "") {
                searchResult.textContent = "Please enter something to search for.";
                return;
            }

            try {
                const response = await fetch("/search", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        search_term: searchTerm,
                        algorithm: selectedAlgorithm,
                        data_type: dataTypeInput.value
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
    } else {
        console.error("Search form or its elements could not be found.");
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const sortButton = document.getElementById("sort-button");
    const dataTypeInput = document.getElementById("sort-data-type");
    const sortStatus = document.getElementById("sort-status");
    const sortedResults = document.getElementById("sorted-results");
    const exportButton = document.getElementById("export-sorted");
    if (
        !sortButton ||
        !dataTypeInput ||
        !sortStatus ||
        !sortedResults ||
        !exportButton
    ) {
        return;
    }
    let sortedValues = null;
    sortButton.addEventListener("click", async () => {
        sortStatus.textContent = "Sorting your data...";
        sortedResults.replaceChildren();
        exportButton.disabled = true;
        sortedValues = null;
        try {
            const response = await fetch("/sort", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    algorithm: selectedAlgorithm,
                    data_type: dataTypeInput.value
                })
            });
            const result = await response.json();
            if (!response.ok) {
                sortStatus.textContent =
                    result.error || "Could not sort the data.";
                return;
            }
            sortedValues = result.sorted_values;
            const list = document.createElement("ol");
            sortedValues.forEach((value) => {
                const item = document.createElement("li");
                item.textContent = value;
                list.appendChild(item);
            });
            sortedResults.appendChild(list);
            sortStatus.textContent =
                `Sorting complete! ${sortedValues.length} items sorted.`;
            exportButton.disabled = false;
        } catch (error) {
            sortStatus.textContent =
                "Could not connect to the server. Please try again.";
            console.error("Sorting error:", error);
        }
    });
    exportButton.addEventListener("click", async () => {
        if (sortedValues === null) {
            sortStatus.textContent = "Please sort your data first.";
            return;
        }
        try {
            const response = await fetch("/export-sorted", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    values: sortedValues
                })
            });
            if (!response.ok) {
                const result = await response.json();
                sortStatus.textContent =
                    result.error || "Could not export the CSV file.";
                return;
            }
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.href = url;
            link.download = "sorted_data.csv";
            document.body.appendChild(link);
            link.click();
            link.remove();
            URL.revokeObjectURL(url);
            sortStatus.textContent = "Your sorted CSV has been downloaded.";
        } catch (error) {
            sortStatus.textContent =
                "Could not export the CSV file. Please try again.";
            console.error("CSV export error:", error);
        }
    });
});