from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare('robot_arm_simulation')
    gazebo_ros_share = FindPackageShare('gazebo_ros')

    world = PathJoinSubstitution([pkg_share, 'worlds', 'conveyor_world.world'])
    robot_description = ParameterValue(
        Command(['xacro ', PathJoinSubstitution([pkg_share, 'urdf', 'robot_arm.urdf.xacro'])]),
        value_type=str,
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([gazebo_ros_share, 'launch', 'gazebo.launch.py'])
        ),
        launch_arguments={'world': world}.items(),
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
        output='screen',
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot_arm', '-topic', 'robot_description', '-x', '0.0', '-y', '-1.0', '-z', '0.2'],
        output='screen',
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen',
    )

    load_arm_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_controller'],
        output='screen',
    )

    spawn_boxes = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'box_0', '-file', PathJoinSubstitution([pkg_share, 'worlds', 'box.sdf']), '-x', '-1.5', '-y', '0.0', '-z', '1.0'],
        output='screen',
    )

    spawn_boxes_2 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'box_1', '-file', PathJoinSubstitution([pkg_share, 'worlds', 'box.sdf']), '-x', '-2.0', '-y', '0.05', '-z', '1.0'],
        output='screen',
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn_robot,
        RegisterEventHandler(
            OnProcessExit(target_action=spawn_robot, on_exit=[load_joint_state_broadcaster])
        ),
        RegisterEventHandler(
            OnProcessExit(target_action=load_joint_state_broadcaster, on_exit=[load_arm_controller])
        ),
        spawn_boxes,
        spawn_boxes_2,
    ])
