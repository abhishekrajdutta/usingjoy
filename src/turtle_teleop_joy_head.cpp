#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
#include <string>
#include <gazebo_msgs/ModelState.h>
#include <tf/transform_broadcaster.h>



class TeleopTurtle
{
public:
  TeleopTurtle();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);
  
  ros::NodeHandle nh_;

  int linear_, angular_;
  //std_msgs::int8 count = 1;
  double l_scale_, a_scale_;
  
  //std_msgs::Float64 deg;
  std_msgs::Float64 deg;
  //ros::Publisher vel_pub_;
  //ros::Publisher rot_pub_;
  ros::Subscriber joy_sub_;
  ros::Publisher chatter_pub;
  //ros::Publisher gazebo_state_reset_pub;
  //ros::Publisher ptam_com_pub;
  //std_msgs::String msg,resetString,spaceString;
  //std::stringstream ss;
  //gazebo_msgs::ModelState initState;

  
};


TeleopTurtle::TeleopTurtle():
  linear_(1),
  angular_(2)
{

  nh_.param("axis_linear", linear_, linear_);
  nh_.param("axis_angular", angular_, angular_);
  nh_.param("scale_angular", a_scale_, a_scale_);
  nh_.param("scale_linear", l_scale_, l_scale_);


  //vel_pub_ = nh_.advertise<geometry_msgs::Twist>("ron/cmd_vel", 1);
  //rot_pub_ = nh_.advertise<std_msgs::String>("/ron/joint1_position_controller/command", 1000);
  //vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/teleop", 1);

  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 10, &TeleopTurtle::joyCallback, this);  
  
    
  chatter_pub = nh_.advertise<std_msgs::Float64>("/ron/joint1_position_controller/command", 1000);

  //gazebo_state_reset_pub = nh_.advertise<gazebo_msgs::ModelState>("/gazebo/set_model_state",1);

  //ptam_com_pub = nh_.advertise<std_msgs::String>("/vslam/key_pressed",1);

  //rostopic pub -1 /ron/joint1_position_controller/command std_msgs/Float64 "data: 1.5"

}

void TeleopTurtle::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  /*geometry_msgs::Twist twist;
  twist.angular.z = a_scale_*joy->axes[angular_];
  twist.linear.x = l_scale_*joy->axes[linear_];
  vel_pub_.publish(twist);*/
  deg.data = joy->axes[3];  
  
  chatter_pub.publish(deg);

  


    //ROS_INFO("%s    \n", msg.data.c_str());
   // chatter_pub.publish(msg);
   // ++count;

}




int main(int argc, char** argv)
{
  ros::init(argc, argv, "teleop_turtle");
  TeleopTurtle teleop_turtle;
 
  
  ros::spin();
}
