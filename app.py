from flask import Flask, render_template, request
from python.search.linear import linear_search

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


@app.route("/")
def index():
    return render_template("index.html")

 #look at these next few lines if you are having problems with url
@app.route("/test/<int:target>")
def test(target):
    result = linear_search([1, 2, 3, 4, 5], target)
    return str(result)

@app.route("/algorithm")
def algorithm ():
    algorithm_name = request.args.get("algorithm")
    algorithm_type = algorithm_types.get(algorithm_name)
    display_name=algorithm_names.get(algorithm_name)
    if algorithm_type == "search":
        return render_template("search_algorithm.html",algorithm_name=display_name)
    elif algorithm_type == "sort":
        return render_template("sort_algorithm.html",algorithm_name=display_name)
    else:
        return "Unknown algorithm"

if __name__ == "__main__":
    app.run(debug=True)