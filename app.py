from flask import Flask, render_template, request, jsonify
from python.search.linear import linear_search
from python.search.binary import binary_search
from python.sort.bubble import bubble_sort
from python.sort.insertion import insertion_sort
from python.sort.merge import merge_sort
from python.sort.quick import quick_sort, _quick_sort, partition

algorithm_types = {
    "linear": "search",
    "binary": "search",
    "bubble": "sort",
    "insertion": "sort",
    "quick": "sort",
    "merge": "sort"
}

algorithm_names = {
    "linear": "Linear Search",
    "binary": "Binary Search",
    "bubble": "Bubble Sort",
    "insertion": "Insertion Sort",
    "quick": "Quick Sort",
    "merge": "Merge Sort"
}

app = Flask(__name__)

uploaded_data = []

@app.route("/upload-data", methods=["POST"])
def upload_data():
    data = request.get_json()
    if not data or "values" not in data:
        return jsonify({"error": "No data received"}), 400
    values = data["values"]
    uploaded_data.clear()
    uploaded_data.extend(values)
    return jsonify({
        "message": "Data received successfully",
        "count": len(values)
    })

@app.route("/search", methods=["POST"])
def search_request():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No search data received"}), 400
    search_term = data.get("search_term")
    algorithm_name = data.get("algorithm")
    data_type = data.get("data_type", "integer")
    values = uploaded_data.copy()
    if search_term is None or not algorithm_name:
        return jsonify({"error": "Missing search term or algorithm"}), 400
    if data_type == "integer":
        try:
            values = [int(value) for value in values]
            search_term = int(search_term)
        except (ValueError, TypeError):
            return jsonify({
                "error": "Numbers mode requires whole numbers in your CSV and search term."
            }), 400
    elif data_type != "string":
        return jsonify({"error": "Invalid data type selected"}), 400
    if algorithm_name == "linear":
        index = linear_search(values, search_term)
    elif algorithm_name == "binary":
        if values != sorted(values):
            return jsonify({
                "error": "Binary Search requires sorted data. Please sort your CSV data and upload it again."
            }), 400
        index = binary_search(values, search_term)
    else:
        return jsonify({"error": "Search algorithm not found"}), 400
    return jsonify({"index": index})


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/algorithm")
def algorithm ():
    algorithm_name = request.args.get("algorithm")
    algorithm_type = algorithm_types.get(algorithm_name)
    display_name=algorithm_names.get(algorithm_name)
    if algorithm_type == "search":
        return render_template("search_algorithm.html",display_name=display_name,algorithm_name=algorithm_name)
    elif algorithm_type == "sort":
        return render_template("sort_algorithm.html",display_name=display_name,algorithm_name=algorithm_name)
    else:
        return "Unknown algorithm"

if __name__ == "__main__":
    app.run(debug=True)