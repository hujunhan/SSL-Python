1. 安装SDK

2. 安装Python-**3.6**

3. 从C盘的C:\Program Files (x86)\Intel RealSense SDK 2.0\bin\x64目录下复制

   * .pyd文件共4个
   * .dll文件共2个

   到你电脑上Python的site-packages文件夹下（一般在\$your_python_path$\Lib\ 目录下）

4. 运行例程

   ```python
   # First import the library
   import pyrealsense2 as rs
   
   pipeline = rs.pipeline()
   pipeline.start()
   
   while True:
   	# Create a pipeline object. This object configures the streaming camera and owns it's handle
   	frames = pipeline.wait_for_frames()
   	depth = frames.get_depth_frame()
   	if not depth: continue
   
   	# Print a simple text-based representation of the image, by breaking it into 10x20 pixel regions and approximating the coverage of pixels within one meter
   	coverage = [0] * 64
   	for y in range(480):
   		for x in range(640):
   			dist = depth.get_distance(x, y)
   			if 0 < dist and dist < 1:
   				coverage[int(x / 10)] += 1
   
   		if y % 20 is 19:
   			line = ""
   			for c in coverage:
   				line += " .:nhBXWW"[int(c / 25)]
   			coverage = [0] * 64
   			print(line)
   
   ```

5. 应该可以看到命令行输出字符形式的图像