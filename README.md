# 注意事项
## 数据规定
* 地图大小/数据单位
  * 原点为(0,0),在地图中心
  * 在*Athena*界面中显示为 `1200 x 900` ,单位为$cm$ 
  * 通过*Vision_Detection*得到的大小为 `12000 x 9000` ,单位为$mm$
  * 通过*grSim_Replacement*控制的大小为 `12 x 9 ` ,单位为$m$

* 控制信号
  * 线速度单位不明，小于$m/s$,即设置速度为$1$时，实际速度小于$1m/s$
  * 角速度单位约等于 $0.5rad/s$,即设置角速度为$1$时，转一圈大约需要$6.28$秒

* 机器人参数
  * 读取位置信号时，得到的数据单位是mm，12000*9000 
  * 读取角度信号时，得到的数据是按照弧度制
  * 角度信号0°时向右，随角度增加，顺时针旋转(-180,180)
## 机器人操作
* 对同一个机器人进行不同操作时要注意：两个操作(setSpeed、setReplacement)之间要清空一下message，即调用机器人的clearCommand()命令
## 自定义类与函数
* Robot类
  * 变量
    * color
    * id
  * 方法
    * setSpeed
    * setReplacement
    * getSpeedCommand

* 函数
  * getPos (获取机器人全部信息)
  * getXYA (只返回x,y坐标和方向orientation)