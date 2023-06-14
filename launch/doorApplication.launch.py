import os
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    rviz_config_file = PathJoinSubstitution(
            [FindPackageShare("door_tof_sensor"), "rviz", "door_model.rviz"]
    )

    # Specify the name of the package and path to xacro file within the package
    #pkg_name = 'urdf_example'  
    #file_subpath = 'description/example_robot.urdf.xacro'
    pkg_name = 'launch_package'  
    file_subpath = 'description/door.urdf.xacro'

    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    ld = LaunchDescription()

    motor_driver_node = Node(
        package="door_tof_sensor",
        executable="machine_ControlNode",
        name = "pic24_motor_driver_node"    #Rename node with this assigned name
    )

    door_dynamic_tf2_node = Node(
        package="door_tof_sensor",
        executable="door_dynamic_tf2_transform",
        name = "imu_dynamic_tf2_transform"                  #Rename node with this assigned name
    )

    vl53l8cx_publisher_node_1 = Node(
        package="vl53l8cx",
        executable="vl53l8cx_tof_Node",
        name = "vl53l8cx_tof_sensor_1",        #Rename node with this assigned name
        arguments = ['1', 'pcl_data1','vl53l8cx_frame']     
        #arguments = ['1', 'pcl_data1','world']                
    )

    vl53l8cx_publisher_node_2 = Node(
        package="vl53l8cx",
        executable="vl53l8cx_tof_Node",
        name = "vl53l8cx_tof_sensor_2",        #Rename node with this assigned name
        arguments = ['2', 'pcl_data2', 'world']                 
    )

    imu_filter_node_for_orientation = Node(
        package="imu_complementary_filter",
        executable="complementary_filter_node",
        name = "complementary_filter_node"                  #Rename node with this assigned name
    )

    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw}] # add other parameters here if required
    )

    # Configure the node
    node_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        #output="log",
        arguments=["-d", rviz_config_file],
    )

    ld.add_action(motor_driver_node)
    ld.add_action(door_dynamic_tf2_node)
    ld.add_action(vl53l8cx_publisher_node_1)   
    ld.add_action(vl53l8cx_publisher_node_2)        
    #ld.add_action(imu_filter_node_for_orientation)
    ld.add_action(node_robot_state_publisher)
    ld.add_action(node_rviz)

    return ld