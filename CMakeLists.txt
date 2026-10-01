cmake_minimum_required(VERSION 3.15)

project(CPUSchedulingSimulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(cpu_scheduler
    src/main.cpp
    src/scheduler.cpp
)

target_include_directories(cpu_scheduler PRIVATE include)

if (MSVC)
    target_compile_options(cpu_scheduler PRIVATE /W4)
else()
    target_compile_options(cpu_scheduler PRIVATE -Wall -Wextra -Wpedantic)
endif()

add_executable(scheduler_tests
    tests/test_scheduler.cpp
    src/scheduler.cpp
)

target_include_directories(scheduler_tests PRIVATE include)
