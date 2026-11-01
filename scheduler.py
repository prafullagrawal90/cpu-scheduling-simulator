class CPUScheduler:
    def __init__(self, processes):
        self.processes = [p.copy() for p in processes]
        self.gantt_chart = []
        self.metrics = {}

    def _reset(self):
        for p in self.processes:
            p.pop("completion_time", None)
            p.pop("start_time", None)
            p.pop("waiting_time", None)
            p.pop("turnaround_time", None)
        self.gantt_chart = []
        self.metrics = {}

    def _calculate_metrics(self):
        total_wait = 0
        total_turnaround = 0

        for p in self.processes:
            ct = p["completion_time"]
            tat = ct - p["arrival_time"]
            wt = tat - p["burst_time"]
            p["turnaround_time"] = tat
            p["waiting_time"] = max(0, wt)
            total_wait += p["waiting_time"]
            total_turnaround += tat

        n = len(self.processes)
        total_time = max(p["completion_time"] for p in self.processes) if n else 0
        burst_total = sum(p["burst_time"] for p in self.processes)

        self.metrics = {
            "avg_waiting_time": round(total_wait / n, 2) if n else 0,
            "avg_turnaround_time": round(total_turnaround / n, 2) if n else 0,
            "total_time": total_time,
            "cpu_utilization": round((burst_total / total_time) * 100, 2) if total_time else 0
        }

    def fcfs(self):
        self._reset()
        self.processes.sort(key=lambda p: (p["arrival_time"], p["pid"]))
        current = 0

        for p in self.processes:
            current = max(current, p["arrival_time"])
            start = current
            current += p["burst_time"]

            p["start_time"] = start
            p["completion_time"] = current

            self.gantt_chart.append({
                "pid": p["pid"],
                "start": start,
                "end": current,
                "burst_time": p["burst_time"]
            })

        self._calculate_metrics()
        return self._format_result("FCFS")

    def sjf(self):
        self._reset()
        remaining = [p.copy() for p in self.processes]
        current = 0

        while remaining:
            available = [
                p for p in remaining
                if p["arrival_time"] <= current
            ]

            if not available:
                current = min(
                    p["arrival_time"]
                    for p in remaining
                )
                continue

            p = min(
                available,
                key=lambda x: (
                    x["burst_time"],
                    x["arrival_time"],
                    x["pid"]
                )
            )

            remaining.remove(p)

            start = current
            current += p["burst_time"]

            p["start_time"] = start
            p["completion_time"] = current

            self.gantt_chart.append({
                "pid": p["pid"],
                "start": start,
                "end": current,
                "burst_time": p["burst_time"]
            })

        self._copy_results_from_gantt()
        self._calculate_metrics()

        return self._format_result(
            "Shortest Job First (SJF)"
        )

    def priority_scheduling(self):
        self._reset()

        processes = [
            p.copy()
            for p in self.processes
        ]

        processes.sort(
            key=lambda p: (
                p["arrival_time"],
                p["pid"]
            )
        )

        remaining = {
            p["pid"]: p["burst_time"]
            for p in processes
        }

        current = 0
        completed = set()

        while len(completed) < len(processes):

            available = [
                p for p in processes
                if p["arrival_time"] <= current
                and p["pid"] not in completed
                and remaining[p["pid"]] > 0
            ]

            if not available:
                next_arrival = min(
                    p["arrival_time"]
                    for p in processes
                    if p["pid"] not in completed
                    and remaining[p["pid"]] > 0
                )

                current = max(current, next_arrival)
                continue

            p = min(
                available,
                key=lambda x: (
                    x.get("priority", 0),
                    x["arrival_time"],
                    x["pid"]
                )
            )

            pid = p["pid"]

            if "start_time" not in p:
                p["start_time"] = current

            start = current

            current += 1
            remaining[pid] -= 1

            if (
                self.gantt_chart
                and self.gantt_chart[-1]["pid"] == pid
                and self.gantt_chart[-1]["end"] == start
            ):
                self.gantt_chart[-1]["end"] = current
                self.gantt_chart[-1]["burst_time"] += 1
            else:
                self.gantt_chart.append({
                    "pid": pid,
                    "start": start,
                    "end": current,
                    "burst_time": 1,
                    "priority": p.get("priority", 0)
                })

            if remaining[pid] == 0:
                p["completion_time"] = current
                completed.add(pid)

        result_map = {
            p["pid"]: p
            for p in processes
        }

        for p in self.processes:
            result = result_map[p["pid"]]

            p["start_time"] = result.get(
                "start_time",
                0
            )

            p["completion_time"] = result.get(
                "completion_time",
                0
            )

        self._calculate_metrics()

        return self._format_result(
            "Preemptive Priority Scheduling"
        )

    def round_robin(self, time_quantum=2):
        self._reset()

        time_quantum = max(
            1,
            int(time_quantum)
        )

        processes = sorted(
            [p.copy() for p in self.processes],
            key=lambda p: (
                p["arrival_time"],
                p["pid"]
            )
        )

        remaining = {
            p["pid"]: p["burst_time"]
            for p in processes
        }

        queue = []
        added = set()
        current = 0
        completed = set()
        index = 0

        while len(completed) < len(processes):

            while (
                index < len(processes)
                and processes[index]["arrival_time"] <= current
            ):
                pid = processes[index]["pid"]

                if pid not in added:
                    queue.append(pid)
                    added.add(pid)

                index += 1

            if not queue:
                if index < len(processes):
                    current = max(
                        current,
                        processes[index]["arrival_time"]
                    )
                    continue
                break

            pid = queue.pop(0)

            p = next(
                x for x in processes
                if x["pid"] == pid
            )

            if "start_time" not in p:
                p["start_time"] = current

            run = min(
                time_quantum,
                remaining[pid]
            )

            start = current
            current += run
            remaining[pid] -= run

            self.gantt_chart.append({
                "pid": pid,
                "start": start,
                "end": current,
                "burst_time": run
            })

            while (
                index < len(processes)
                and processes[index]["arrival_time"] <= current
            ):
                new_pid = processes[index]["pid"]

                if new_pid not in added:
                    queue.append(new_pid)
                    added.add(new_pid)

                index += 1

            if remaining[pid] > 0:
                queue.append(pid)
            else:
                p["completion_time"] = current
                completed.add(pid)

        result_map = {
            p["pid"]: p
            for p in processes
        }

        for p in self.processes:
            rp = result_map[p["pid"]]

            p["start_time"] = rp.get(
                "start_time",
                0
            )

            p["completion_time"] = rp.get(
                "completion_time",
                0
            )

        self._calculate_metrics()

        return self._format_result(
            "Round Robin"
        )

    def _copy_results_from_gantt(self):
        result = {}

        for item in self.gantt_chart:
            pid = item["pid"]

            if pid not in result:
                result[pid] = {
                    "start": item["start"],
                    "end": item["end"]
                }
            else:
                result[pid]["end"] = item["end"]

        for p in self.processes:
            item = result[p["pid"]]

            p["start_time"] = item["start"]
            p["completion_time"] = item["end"]

    def _format_result(self, algorithm_name):
        return {
            "algorithm": algorithm_name,
            "gantt_chart": self.gantt_chart,
            "processes": [
                {
                    "pid": p["pid"],
                    "arrival_time": p["arrival_time"],
                    "burst_time": p["burst_time"],
                    "priority": p.get("priority", "-"),
                    "start_time": p.get(
                        "start_time",
                        0
                    ),
                    "completion_time": p.get(
                        "completion_time",
                        0
                    ),
                    "waiting_time": p.get(
                        "waiting_time",
                        0
                    ),
                    "turnaround_time": p.get(
                        "turnaround_time",
                        0
                    )
                }
                for p in sorted(
                    self.processes,
                    key=lambda x: x["pid"]
                )
            ],
            "metrics": self.metrics
        }