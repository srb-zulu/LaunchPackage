from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    static_sensor_tf_node = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            #Pass the parameters       
            arguments = ['1', '1', '0', '0', '0', '0', 'world', 'vl53l8cx_sensor']
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
        arguments = ['2', 'pcl_data2', 'vl53l8cx_frame']  
        #arguments = ['2', 'pcl_data2', 'door_module']                
    )

    #ld.add_action(static_sensor_tf_node)
    ld.add_action(vl53l8cx_publisher_node_1)
    #ld.add_action(vl53l8cx_publisher_node_2)
    return ld