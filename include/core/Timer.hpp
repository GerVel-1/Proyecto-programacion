#pragma once
#include <chrono>

class Timer {
    std::chrono::steady_clock::time_point start_;
public:
    Timer() : start_(std::chrono::steady_clock::now()) {}
    double elapsed_ms() const {
        using namespace std::chrono;
        return duration<double, std::milli>(steady_clock::now() - start_).count();
    }
};
