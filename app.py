from flask import Flask, render_template, request
from python.search.linear import linear_search

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
    for i in range (0,len(algorithm_name)):
        if algorithm_name[i] == " ":
            if algorithm_name[i+2] == "e":
                return render_template(
                    "search_algorithm.html",
                    algorithm_name=algorithm_name
                )
            else:
                return render_template(
                    "sort_algorithm.html",
                    algorithm_name=algorithm_name
                )
        else:
            pass

if __name__ == "__main__":
    app.run(debug=True)