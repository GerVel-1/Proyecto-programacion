#pragma once
#include <string>
#include <map>
#include "Result.hpp"

using Params = std::map<std::string, std::string>;

class IModule {
public:
    virtual ~IModule() = default;
    virtual std::string name() const = 0;
    virtual Result run(const Params& params) = 0;
};
