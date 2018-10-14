cmake_minimum_required(VERSION 2.8.3)
project(face_node)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(DEPENDS)

catkin_python_setup()

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
##install(PROGRAMS
##   nodes/ros_faceselect.py
##  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
##)

##install(DIRECTORY launch
##  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
##)

##install(DIRECTORY nodes
##  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
##)
