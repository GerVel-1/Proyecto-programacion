cmake_minimum_required(VERSION 3.16)
project(UrbanOS CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

include_directories(include)

file(GLOB_RECURSE SRC_FILES src/*.cpp)
add_executable(urbanos ${SRC_FILES})

enable_testing()
add_subdirectory(tests)
