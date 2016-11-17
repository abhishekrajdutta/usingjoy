#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/String.h>
#include <std_msgs/Float64.h>
#include <string>
#include <gazebo_msgs/ModelState.h>
#include <tf/transform_broadcaster.h>


bool action1,action2,action3,action4,action5,action6,action7,action8,action9,action10,action11,action12,action13,action14,action15,action16,action17,action18,action19,action20;
float speedfactor=1.0;
class TeleopTurtle
{
public:
  TeleopTurtle();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);
  
  ros::NodeHandle nh_;

  int linear_, angular_,count1=0,count2=0,count3=0,count4=0;
  //std_msgs::int8 count = 1;
  double l_scale_, a_scale_;
  double init_x=3,init_y=1.5,initYaw=(180+55)*3.14/180;
  //std_msgs::Float64 deg;
  std_msgs::Float64 deg;
  ros::Publisher vel_pub_;
  ros::Publisher rot_pub_;
  ros::Subscriber joy_sub_;
  ros::Publisher chatter_pub;
  ros::Publisher gazebo_state_reset_pub;
  ros::Publisher ptam_com_pub;
  std_msgs::String msg,resetString,spaceString;
  std::stringstream ss;
  gazebo_msgs::ModelState initState;

  
};


TeleopTurtle::TeleopTurtle():
  linear_(1),
  angular_(2)
{

  nh_.param("axis_linear", linear_, linear_);
  nh_.param("axis_angular", angular_, angular_);
  nh_.param("scale_angular", a_scale_, a_scale_);
  nh_.param("scale_linear", l_scale_, l_scale_);


  vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/ron/cmd_vel", 1);
  //rot_pub_ = nh_.advertise<std_msgs::String>("/ron/joint1_position_controller/command", 1000);
  //vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/cmd_vel_mux/input/teleop", 1);

  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 10, &TeleopTurtle::joyCallback, this);  
  
    
  //chatter_pub = nh_.advertise<std_msgs::Float64>("/ron/joint1_position_controller/command", 1000);

  gazebo_state_reset_pub = nh_.advertise<gazebo_msgs::ModelState>("/gazebo/set_model_state",1);

  ptam_com_pub = nh_.advertise<std_msgs::String>("/vslam/key_pressed",1);

  //rostopic pub -1 /ron/joint1_position_controller/command std_msgs/Float64 "data: 1.5"

}

void TeleopTurtle::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  geometry_msgs::Twist twist;
  twist.angular.z = a_scale_*joy->axes[angular_];
  twist.linear.x = l_scale_*joy->axes[linear_];
  vel_pub_.publish(twist);

  //chatter_pub.publish(deg);
  
  //********start button initialises ptam**********
  if(joy->buttons[7]==1)
  {
    resetString.data = "r";
  spaceString.data = "Space";
  ptam_com_pub.publish(resetString);
  ptam_com_pub.publish(resetString);
  ptam_com_pub.publish(resetString);
  ptam_com_pub.publish(resetString);
  
  initState.model_name = "ron";
  //initState.model_name = "mobile_base";
  initState.reference_frame = "world";
  initState.pose.position.z = 0;
  initState.pose.position.x = init_x;
  initState.pose.position.y = init_y;
  initState.pose.orientation = tf::createQuaternionMsgFromRollPitchYaw(0.0, 0.0, initYaw);

  gazebo_state_reset_pub.publish(initState);
  ptam_com_pub.publish(spaceString);

  twist.linear.x=-0.2;
  clock_t t = clock();
  ros::Rate r(10);
  while(((float) (clock() - t))/CLOCKS_PER_SEC < 0.2) 
  {
    vel_pub_.publish(twist);
    
  
    r.sleep();
  }
  ros::Rate(1).sleep();
  ptam_com_pub.publish(spaceString);

  }


  //**********************home button moves robot along trajectory planned beforehand
 /* if(joy->buttons[1]==1)
  {
    

  twist.linear.x=0;
  twist.angular.z=0;
  clock_t t = clock();
  ros::Rate r(10);
  for(int i=0;i<34;i++) 
  {
    vel_pub_.publish(twist);  
    r.sleep();
  }
  ros::Rate(1).sleep();
    

  }  
*/

  if(joy->buttons[8]==1) //homescan
  {
    

  twist.linear.x=0.95;
  twist.angular.z=+0.6;
  clock_t t = clock();
  ros::Rate r(80); 	
  for(int i=0;i<10;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action1=0;  
  
  }

  if(joy->buttons[3]==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<113;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action1=1;  
  
  }


 if(action1==1)  //right turn
  {
    
  twist.linear.x=0.75;
  twist.angular.z=-0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<515;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action1=0;
  action2=1;  
  ROS_INFO("%d",count1);

  if(action2==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<113;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action3=1;  
  
  }

  }

  if(action3==1)  //left turn
  {
    
  twist.linear.x=0.75;
  twist.angular.z=0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<500;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action3=0;
  action4=1;  
  ROS_INFO("%d",count1);

  }

  if(action4==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<113;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action4=0; 
  action5=1; 
  
  }

//*********************first long straight**************************

  if(action5==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<113;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action5=0;
  action6=1;  
  
  }

  if(action6==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<113;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action6=0;  
  action7=1;
  }
  
  if(action7==1)  //left turn
  {
    
  twist.linear.x=0.8;
  twist.angular.z=0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<205;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action7=0;
  action8=1;  
  ROS_INFO("%d",count1);

  }

  if(action8==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<235;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action8=0;  
  action9=1;
  }

  if(action9==1)  //right turn at wall
  {
    
  twist.linear.x=0.8;
  twist.angular.z=-0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<205;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action9=0;
  action10=1;  
  ROS_INFO("%d",count1);

  }

  if(action10==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<200;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action10=0;  
  action11=1;
  }


  if(action11==1)  //left turn
  {
    
  twist.linear.x=0.75;
  twist.angular.z=0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<500;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action11=0;
  action12=1;  
  ROS_INFO("%d",count1);

  }

  if(action12==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<160;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action12=0;  
  action13=1;
  }

  if(action13==1)  //right turn after wall u turn
  {
    
  twist.linear.x=0.8;
  twist.angular.z=-0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<205;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action13=0;
  action14=1;  
  ROS_INFO("%d",count1);

  }

  if(action14==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<100;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action14=0;  
  action15=1;
  }

  if(action15==1)  //left turn
  {
    
  twist.linear.x=0.8;
  twist.angular.z=0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<195;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action15=0;
  action16=1;  
  ROS_INFO("%d",count1);

  }


  if(action16==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<600;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action16=0;  
  action17=1;
  }

  if(action17==1)  //left turn
  {
    
  twist.linear.x=0.8;
  twist.angular.z=0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<200;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action17=0;
  action18=1;  
  ROS_INFO("%d",count1);

  }

  if(action18==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<350;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action18=0;  
  action19=1;
  }
  
  if(action19==1)  //left turn
  {
    
  twist.linear.x=0.8;
  twist.angular.z=0.53;
  
  
  clock_t t = clock();
  ros::Rate r(100);
  for(int i=0;i<180;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count1++;
  }

  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action19=0;
  action20=1;  
  ROS_INFO("%d",count1);

  }

  if(action20==1)
  {
    

  twist.linear.x=0.85;
  
  clock_t t = clock();
  ros::Rate r(80);
  for(int i=0;i<250;i++)
  {
    vel_pub_.publish(twist);  
    r.sleep();
    
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action2=0;
  action20=0;  
  
  }




  /*if(action3==1)
  {
    

  twist.linear.x=+0.5;
  twist.angular.z=-0.35;
  clock_t t = clock();
  ros::Rate r(10);
  for(int i=0;i<41;i++)
  {
    vel_pub_.publish(twist);
    r.sleep();
    count3++;
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action3=0;
  action4=1;
  ROS_INFO("%d",count3);  

  }*/

  if(action4==1)
  {
    

  twist.linear.x=+0.5;//a smaller value makes the bot go slower
  
  clock_t t = clock();
  ros::Rate r(10);
  for(int i=0;i<70;i++) //this value continues the number of times the loop runs 
  {
    vel_pub_.publish(twist);
    r.sleep();
    count4++;
  }
  ros::Rate(1).sleep();
  twist.linear.x=0;
  twist.angular.z=0;
  action4=0;
  ROS_INFO("%d",count4);

  }

  

  


    //ROS_INFO("%s    \n", msg.data.c_str());
   // chatter_pub.publish(msg);
   // ++count;

}




int main(int argc, char** argv)
{
  speedfactor=1.0;
  action1=0;action2=0;action3=0,action4=0;
  ros::init(argc, argv, "teleop_turtle");
  TeleopTurtle teleop_turtle;


 
  
  ros::spin();
}

