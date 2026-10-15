from flask import Flask, render_template, request, jsonify, Response
import csv
import io
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
        return jsonify({
            "error": "No search data received. Please try again."
        }), 400
    search_term = data.get("search_term")
    algorithm_name = data.get("algorithm")
    data_type = data.get("data_type", "integer")
    values = uploaded_data.copy()
    if search_term is None or not algorithm_name:
        return jsonify({
            "error": "Please provide a search term and select an algorithm."
        }), 400
    if not values:
        return jsonify({
            "error": "No data has been uploaded. Please upload a CSV file first."
        }), 400
    if data_type == "integer":
        try:
            values = [int(value) for value in values]
            search_term = int(search_term)
        except (ValueError, TypeError):
            return jsonify({
                "error": (
                    "Numbers mode requires whole numbers in your CSV "
                    "and search term. Select Text mode for words, "
                    "or upload a CSV containing only whole numbers."
                )
            }), 400
    elif data_type == "string":
        values = [str(value).strip() for value in values]
        search_term = str(search_term).strip()
    else:
        return jsonify({
            "error": "Invalid data type. Please select Numbers or Text."
        }), 400
    if algorithm_name not in ("linear", "binary"):
        return jsonify({
            "error": "Unknown search algorithm. Please select Linear or Binary Search."
        }), 400
    if algorithm_name == "binary" and values != sorted(values):
        if data_type == "integer":
            return jsonify({
                "error": (
                    "Binary Search needs numbers sorted from smallest "
                    "to largest. Please sort your numbers and upload "
                    "the CSV again, or choose Linear Search."
                )
            }), 400
        else:
            return jsonify({
                "error": (
                    "Binary Search needs text sorted alphabetically "
                    "(A to Z). Please sort your text and upload the "
                    "CSV again, or choose Linear Search."
                )
            }), 400
    if algorithm_name == "linear":
        index = linear_search(values, search_term)
    else:
        index = binary_search(values, search_term)
    return jsonify({"index": index})

@app.route("/sort", methods=["POST"])
def sort_request():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No sorting data received."}), 400
    algorithm_name = data.get("algorithm")
    data_type = data.get("data_type", "integer")
    values = uploaded_data.copy()
    if not values:
        return jsonify({
            "error": "Please upload a CSV file before sorting."
        }), 400
    if data_type == "integer":
        try:
            values = [int(value) for value in values]
        except (ValueError, TypeError):
            return jsonify({
                "error": "Numbers mode requires whole numbers in your CSV. Select Text mode or upload numeric data."
            }), 400
    elif data_type == "string":
        values = [str(value).strip() for value in values]
    else:
        return jsonify({"error": "Please select Numbers or Text."}), 400
    sort_functions = {
        "bubble": bubble_sort,
        "insertion": insertion_sort,
        "merge": merge_sort,
        "quick": quick_sort
    }
    sort_function = sort_functions.get(algorithm_name)
    if sort_function is None:
        return jsonify({"error": "Unknown sorting algorithm."}), 400
    sorted_values = sort_function(values.copy())
    if sorted_values is None:
        sorted_values = values
    return jsonify({"sorted_values": sorted_values})

@app.route("/export-sorted", methods=["POST"])
def export_sorted():
    data = request.get_json()
    if not data or not isinstance(data.get("values"), list):
        return jsonify({"error": "No sorted data to export."}), 400
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(data["values"])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=sorted_data.csv"
        }
    )

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