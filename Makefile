CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -Iinclude

TARGET = cpu_scheduler
SOURCES = src/main.cpp src/scheduler.cpp

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(SOURCES) -o $(TARGET)

test:
	$(CXX) $(CXXFLAGS) tests/test_scheduler.cpp src/scheduler.cpp -o scheduler_tests
	./scheduler_tests

clean:
	rm -f $(TARGET) scheduler_tests

.PHONY: all test clean
