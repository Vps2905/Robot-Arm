# Robot Arm + Conveyor Simulation (ROS 2 + Gazebo)

This repository contains a complete ROS 2 package to run:
- A **4-DOF robot arm** using `ros2_control`
- A **conveyor table** in Gazebo
- Moving boxes driven by a custom Gazebo world plugin (`conveyor_plugin`)

---

## 1) System requirements

Recommended OS: **Ubuntu 22.04** with **ROS 2 Humble** and **Gazebo Classic 11**.

Install dependencies:

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-xacro \
  python3-colcon-common-extensions \
  build-essential cmake git
```

Source ROS:

```bash
source /opt/ros/humble/setup.bash
```

---

## 2) Build workspace

If you cloned this repository into `/workspace/Robot-Arm`:

```bash
cd /workspace/Robot-Arm
mkdir -p ../robot_arm_ws/src
cp -r . ../robot_arm_ws/src/Robot-Arm
cd ../robot_arm_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```

---

## 3) Run simulation

In terminal 1:

```bash
cd /workspace/robot_arm_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:/workspace/robot_arm_ws/install/robot_arm_simulation/lib
ros2 launch robot_arm_simulation sim.launch.py
```

You should see:
- Gazebo world with a conveyor table
- Robot arm spawned near the conveyor
- Controllers loaded by `controller_manager/spawner`
- Boxes (`box_0`, `box_1`) moving along +X conveyor direction

---

## 4) Command robot arm joints

In terminal 2:

```bash
cd /workspace/robot_arm_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 topic pub /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: [joint1, joint2, joint3, joint4],
  points: [
    {positions: [0.0, -0.8, 1.0, 0.3], time_from_start: {sec: 2}},
    {positions: [0.6, -0.4, 0.8, -0.2], time_from_start: {sec: 4}},
    {positions: [0.0, -0.8, 1.0, 0.3], time_from_start: {sec: 6}}
  ]
}" -1
```

---

## 5) Push to your GitHub repo

From this repo directory:

```bash
git add .
git commit -m "Improve robot arm + conveyor Gazebo simulation setup"
git push origin <your-branch>
```

If remote is not set yet:

```bash
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin <your-branch>
```

---

## 6) Important files

- `robot_arm_simulation/launch/sim.launch.py`:
  Launches Gazebo, robot state publisher, robot spawn, controller spawners, and sample boxes.
- `robot_arm_simulation/urdf/robot_arm.urdf.xacro`:
  Robot structure + `gazebo_ros2_control` setup with launch-provided controller YAML path.
- `robot_arm_simulation/config/ros2_controllers.yaml`:
  Joint state broadcaster + trajectory controller setup.
- `robot_arm_simulation/worlds/conveyor_world.world`:
  Conveyor geometry + world plugin configuration.
- `robot_arm_simulation/src/conveyor_plugin.cpp`:
  Moves box models inside conveyor region at configured velocity.

---

## 7) Troubleshooting

If controllers fail to load:

```bash
ros2 control list_controllers
ros2 run controller_manager spawner joint_state_broadcaster --controller-manager /controller_manager
ros2 run controller_manager spawner arm_controller --controller-manager /controller_manager
```

If conveyor plugin does not load, confirm plugin path:

```bash
echo $GAZEBO_PLUGIN_PATH
ls /workspace/robot_arm_ws/install/robot_arm_simulation/lib
```

If Gazebo cannot find package resources:

```bash
source /workspace/robot_arm_ws/install/setup.bash
```
