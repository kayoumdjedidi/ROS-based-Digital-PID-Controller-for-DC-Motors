## README for Motor Control Project

### Overview
### NB: please view the dev branch for the latest updates

This project focuses on developing a comprehensive motor control system using a Raspberry Pi and ROS (Robot Operating System). The system integrates PID control strategies for accurate motor speed and position regulation, vital for applications in robotics and automation. By leveraging ROS's capabilities, this system is designed to be modular, scalable, and easily integrated into larger robotics projects.

### Project Structure
The project is structured into several core areas:
1. **Motor Controller Development**
2. **Interface Design and Implementation**
3. **ROS Package and Node Development**
4. **PID Control Integration and Testing**
5. **Documentation and Training**

### Resources
- [Simple ROS PID GitHub Repository](https://github.com/jellevos/simple-ros-pid)
- [ROS Wiki on PID](http://wiki.ros.org/pid)
- [Autonomous Robotics: PID Controllers - JMU](https://w3.cs.jmu.edu/spragunr/CS354_S14/labs/pid_lab/pid_lab.shtml)

### Installation and Setup
1. **Environment Setup:**
   - Install ROS on Ubuntu (Recommended due to better support).
   - Set up a ROS workspace using the `catkin` build system.
2. **Dependencies:**
   - Ensure Python and necessary libraries (e.g., `numpy`, `matplotlib`) are installed.
   - Install ROS dependencies such as `rospy` and `std_msgs`.

### Core Functionalities
1. **Motor Speed and Position Control:**
   - Utilize PID controllers to adjust motor parameters in response to dynamic conditions.
   - Implement controllers both in open-loop and closed-loop configurations for testing and real-world application.

2. **ROS Integration:**
   - Develop ROS nodes for motor control signaling and encoder feedback.
   - Implement service-based architecture for setting motor parameters and control modes.

3. **Interface Design:**
   - Develop user interfaces using PyQt or web-based technologies for real-time control and monitoring.
   - Implement dynamic data visualization for motor performance using ROS tools like `rqt_plot` and `rviz`.

### Running the Project
1. **Basic Commands:**
   - Use `roslaunch` to start the motor control nodes.
   - Monitor motor encoder via ROS topics to adjust control strategies dynamically.
2. **Configuration:**
   - Adjust PID parameters through ROS services or dynamic reconfiguration tools.

### Task Breakdown
- **Completed Tasks:**
  - Measurement of motor specifications.
  - Creation of mathematical models for motor dynamics.
  - Basic motor control through direct GPIO manipulation and PWM adjustment.
- **Pending Tasks:**
  - Advanced PID tuning using Ziegler-Nichols method.
  - Integration of control settings in the ROS environment.
  - Extensive testing of the control system under simulated disturbances.

### Testing and Validation
- Use unit tests for individual components (controllers, ROS nodes).
- Perform integrated tests with the actual motor to validate the entire control system.

### Documentation and Training
- Maintain comprehensive documentation on system setup, usage, and troubleshooting.
- Conduct training sessions for team members to familiarize them with the ROS environment and custom packages.

### Future Work
- Enhance the PID control algorithms by integrating machine learning techniques for adaptive control.
- Expand the ROS node capabilities to include more advanced features such as actionlib for feedback and diagnostics for system monitoring.

### Contribution
- Contributions are welcome, especially in the areas of PID optimization, ROS node efficiency, and user interface enhancement.
- Please refer to the GitHub repository for current issues and guidelines on contributing to the project.

### License
- The project is released under a suitable open-source license, allowing for widespread use and collaboration.
