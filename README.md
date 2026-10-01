# CPU Scheduling Simulator

A console-based CPU Scheduling Simulator written in C++ for Operating Systems coursework.

The simulator accepts process information and runs four CPU scheduling algorithms on the same process set:

- First Come First Serve (FCFS)
- Shortest Job First (SJF) — Non-Preemptive
- Priority Scheduling — Preemptive
- Round Robin (RR)

For every algorithm, it displays a Gantt chart and calculates:

- Completion Time (CT)
- Turnaround Time (TAT)
- Waiting Time (WT)
- Average Turnaround Time
- Average Waiting Time

## Project Structure

```text
cpu-scheduling-simulator/
├── include/
│   └── scheduler.h
├── src/
│   ├── main.cpp
│   └── scheduler.cpp
├── data/
│   └── sample_input.txt
├── docs/
│   └── OS_PROJECT.pdf
├── tests/
│   └── test_scheduler.cpp
├── .gitignore
├── CMakeLists.txt
├── Makefile
├── LICENSE
└── README.md
```

## Requirements

- C++17 or later
- GCC, MinGW, Clang, or another C++17-compatible compiler
- CMake is optional

## Run with g++

### Linux / macOS

```bash
g++ -std=c++17 -Wall -Wextra -O2 src/main.cpp src/scheduler.cpp -Iinclude -o cpu_scheduler
./cpu_scheduler
```

### Windows MinGW

```bash
g++ -std=c++17 -Wall -Wextra -O2 src/main.cpp src/scheduler.cpp -Iinclude -o cpu_scheduler.exe
cpu_scheduler.exe
```

## Run with Make

```bash
make
./cpu_scheduler
```

On Windows with MinGW:

```bash
mingw32-make
cpu_scheduler.exe
```

## Run with CMake

```bash
mkdir build
cd build
cmake ..
cmake --build .
```

Then run the generated executable from the build directory.

## Input Format

The program first asks for the number of processes. For every process, enter:

1. Arrival time
2. Burst time
3. Priority

For Priority Scheduling, a larger priority number means a higher priority.

Round Robin additionally asks for a time quantum.

Example:

```text
Number of processes: 4

P1: arrival=0 burst=2 priority=10
P2: arrival=1 burst=2 priority=20
P3: arrival=5 burst=3 priority=30
P4: arrival=6 burst=4 priority=40
```

For Round Robin, use:

```text
Time quantum: 2
```

## Scheduling Algorithms

### FCFS

The process with the earliest arrival time runs first. It is non-preemptive.

### SJF

Among the processes that have already arrived, the process with the smallest burst time is selected. This implementation is non-preemptive.

### Preemptive Priority

At each CPU time unit, the available process with the highest priority is selected. A newly arrived higher-priority process can preempt the current process.

### Round Robin

Each ready process receives a fixed time quantum. An unfinished process goes to the back of the ready queue.

## Formulas

```text
Turnaround Time = Completion Time - Arrival Time

Waiting Time = Turnaround Time - Burst Time

Average Waiting Time = Total Waiting Time / Number of Processes

Average Turnaround Time = Total Turnaround Time / Number of Processes
```

## Sample Results

Using the sample process set from the project report and a Round Robin quantum of 2, the report records:

| Algorithm | Average Waiting Time | Average Turnaround Time |
|---|---:|---:|
| FCFS | 0.75 | 3.50 |
| SJF (Non-Preemptive) | 0.75 | 3.50 |
| Round Robin (q=2) | 1.25 | 4.00 |
| Priority (Preemptive) | 1.50 | 4.25 |

These values are reproduced from the submitted project report.

## Project Report

The original project report is included in `docs/OS_PROJECT.pdf`.

## Future Enhancements

Possible extensions:

- Graphical user interface
- Shortest Remaining Time First (SRTF)
- Export results to TXT/PDF
- Input validation and better error handling
- Algorithm comparison charts
- CPU utilization and throughput metrics
