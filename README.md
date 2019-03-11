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
## 机器人操作
* 控制机器人
  ``` python
  # 1.新建一个机器人
  test_robot = Robot("yellow", 1)
  # 2.设置速度或者瞬移位置
  test_robot.setSpeed(1, 1, 1)
  test_robot.setReplacement(1, 1, 2)
  # 3.发送命令
  control_socket.sendto(test_robot.getSpeedCommand(), control_addr)
  ```
* 对同一个机器人进行不同操作时要注意：两个操作(setSpeed、setReplacement)之间要清空一下message，即调用机器人的clearCommand()命令
* 读取机器人信息
  ``` python
  getXYA("blue", 0, read_socket)
  # or
  getPos("blue", 0, read_socket)
  ```
## 自定义类与函数
* Robot类
  * 变量
    * color
    * id
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

* 函数
  * getPos (获取机器人全部信息)
  * getXYA (只返回x,y坐标和方向orientation)