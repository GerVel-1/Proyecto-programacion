#pragma once
#include <string>
#include <map>

struct Result {
    std::string module;
    std::string output_json;
    double elapsed_ms = 0.0;
    std::map<std::string, long long> metrics;
};
