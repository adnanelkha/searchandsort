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
    uploaded_data.append(values)
    return jsonify({
        "message": "Data received successfully!",
        "count": len(values)
    })


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