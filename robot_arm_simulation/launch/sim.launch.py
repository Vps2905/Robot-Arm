from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
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
    controllers_file = PathJoinSubstitution([pkg_share, 'config', 'ros2_controllers.yaml'])

    robot_description = ParameterValue(
        Command([
            'xacro ',
            PathJoinSubstitution([pkg_share, 'urdf', 'robot_arm.urdf.xacro']),
            ' controllers_file:=',
            controllers_file,
        ]),
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

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen',
    )

    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller', '--controller-manager', '/controller_manager'],
        output='screen',
    )

    spawn_box_0 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'box_0', '-file', PathJoinSubstitution([pkg_share, 'worlds', 'box.sdf']), '-x', '-1.5', '-y', '0.0', '-z', '1.0'],
        output='screen',
    )

    spawn_box_1 = Node(
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
            OnProcessExit(target_action=spawn_robot, on_exit=[joint_state_broadcaster_spawner])
        ),
        RegisterEventHandler(
            OnProcessExit(target_action=joint_state_broadcaster_spawner, on_exit=[arm_controller_spawner])
        ),
        spawn_box_0,
        spawn_box_1,
    ])
