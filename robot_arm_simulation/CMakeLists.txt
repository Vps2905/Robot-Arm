cmake_minimum_required(VERSION 3.8)
project(robot_arm_simulation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(gazebo_dev REQUIRED)

include_directories(
  include
  ${GAZEBO_INCLUDE_DIRS}
)
link_directories(${GAZEBO_LIBRARY_DIRS})

add_library(conveyor_plugin SHARED src/conveyor_plugin.cpp)
ament_target_dependencies(conveyor_plugin rclcpp gazebo_ros)
target_link_libraries(conveyor_plugin ${GAZEBO_LIBRARIES})

install(
  TARGETS conveyor_plugin
  LIBRARY DESTINATION lib
)

install(
  DIRECTORY launch urdf worlds config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
