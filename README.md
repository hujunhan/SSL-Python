# 注意事项
## 数据规定
* 地图大小/数据单位
  * 在*Athena*界面中显示为 `1200 x 900` ,单位为$cm$ 
  * 通过*Vision_Detection*得到的大小为 `12000 x 9000` ,单位为$mm$
  * 通过*grSim_Replacement*控制的大小为 `12 x 9 ` ,单位为$m$

* 控制信号
  * 线速度单位不明，小于$m/s$,即设置速度为1时，实际速度小于$1m/s$
  * 角速度约等于 $0.5rad/s$,即设置角速度为1时，转一圈大约需要$6.28$秒

## 自定义类与函数
* Robot类
  * 变量
    * color
    * id
  * 方法
    * setSpeed
    * setReplacement
    * getSpeedCommand