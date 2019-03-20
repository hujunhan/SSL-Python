# 注意事项
## 数据规定
* 地图大小/数据单位
  * 原点为(0,0),在地图中心
  * 在*Athena*界面中显示为 `1200 x 900` ,单位为cm 
  * 通过*Vision_Detection*得到的大小为 `12000 x 9000` ,单位为mm
  * 通过*grSim_Replacement*控制的大小为 `12 x 9 ` ,单位为m

* 控制信号
  * 线速度单位不明，小于m/s,即设置速度为1时，实际速度小于1m/s
  * 角速度单位约等于 0.5rad/s,即设置角速度为1时，转一圈大约需要6.28秒
  * 最大速度 500cm/s
  * 最大加速度 500cm/s^2
## 机器人操作
* 控制机器人
  ``` python
  # 1.新建一个机器人,要依次给出颜色、id、半径、地址端口信息
  test_robot = Robot("yellow", 1,0.15,control_addr)
  # 2.设置速度或者瞬移位置，这条命令会自动发出控制命令
  test_robot.setSpeed(1, 1, 1)
  test_robot.setReplacement(1, 1, 2)
  ```
* 读取机器人信息
  ``` python
  #1.新建一个camera实例，要传入读取地址端口
  camera=Camera(read_addr)
  #2.读取信息，现在Camera类中有
  x,y,ori=camera.getRobotPos()#读取全部机器人的位置信息（数组），顺序是蓝0-7，黄0-7
  vx,vy,vori=camera.getRobotVel()#读取全部机器人的速度信息（数组），顺序是蓝0-7，黄0-7
  blue_robot,yellow_robot=camera.getRobotDict()#读取全部机器人的全部信息（字典），通过id号来索引。
  #3.获取想要的信息
  xb0=x[0]#蓝色0号机器人的位置
  vb2=vx[2]#蓝色2号机器人的x方向速度
  oy3=yellow_robot[3].orientation#黄色3号机器人的转向
  ```
## 自定义类与函数
* Robot类
  * 变量
    * color
    * id
    * radius
  * 方法
    * setSpeed
    * setReplacement
    * getSpeedCommand

* Camera类
  * 变量
    * read_addr
    * read_socket
  * 方法
    * update_state
    * getRobotPos
    * getRobotVel
    * getRobotDict

* utils工具函数库
  * cal_angle(start,goal),通过getRobotDict获取的机器人输入函数，获取`start的方向`与`start到goal的方向`之间的夹角，范围\[-pi,pi]