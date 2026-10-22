#include <cassert>
#include "core/Timer.hpp"

int main() {
    Timer t;
    assert(t.elapsed_ms() >= 0.0);
    return 0;
}
