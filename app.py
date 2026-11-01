from flask import Flask, render_template, request, jsonify
from scheduler import CPUScheduler
import threading
import webbrowser

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/schedule", methods=["POST"])
def schedule():
    try:
        data = request.get_json(silent=True) or {}

        processes = data.get("processes", [])
        algorithm = data.get("algorithm", "fcfs")
        time_quantum = int(data.get("time_quantum", 2))

        if not processes:
            return jsonify({
                "error": "Please add at least one process"
            }), 400

        scheduler = CPUScheduler(processes)

        if algorithm == "fcfs":
            result = scheduler.fcfs()

        elif algorithm == "sjf":
            result = scheduler.sjf()

        elif algorithm == "priority":
            result = scheduler.priority_scheduling()

        elif algorithm == "round_robin":
            result = scheduler.round_robin(time_quantum)

        else:
            return jsonify({
                "error": "Invalid algorithm"
            }), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/compare", methods=["POST"])
def compare():
    try:
        data = request.get_json(silent=True) or {}

        processes = data.get("processes", [])
        time_quantum = int(data.get("time_quantum", 2))

        if not processes:
            return jsonify({
                "error": "Please add at least one process"
            }), 400

        results = {}

        for algorithm in [
            "fcfs",
            "sjf",
            "priority",
            "round_robin"
        ]:
            scheduler = CPUScheduler(processes)

            if algorithm == "fcfs":
                results[algorithm] = scheduler.fcfs()

            elif algorithm == "sjf":
                results[algorithm] = scheduler.sjf()

            elif algorithm == "priority":
                results[algorithm] = scheduler.priority_scheduling()

            elif algorithm == "round_robin":
                results[algorithm] = scheduler.round_robin(
                    time_quantum
                )

        return jsonify(results)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


def open_browser():
    url = "http://127.0.0.1:5000/"

    try:
        webbrowser.open_new(url)
    except Exception:
        pass

    print(f"\nCPU Scheduler is running at: {url}\n")


if __name__ == "__main__":
    threading.Timer(
        1.0,
        open_browser
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )