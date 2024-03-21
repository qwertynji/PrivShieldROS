import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import os
import threading
import time
import cv2
from cv_bridge import CvBridge
import random

# 全局变量，用于计数新文件
new_file_count = 0
# 创建 CvBridge 实例
bridge = CvBridge()

def folder_monitor(folder_path):
    global new_file_count
    file_list = os.listdir(folder_path)

    while rclpy.ok():
        current_file_list = os.listdir(folder_path)
        new_files = [f for f in current_file_list if f not in file_list]
        if new_files:
            new_file_count += len(new_files)
            print("New files found: {} (Total: {})".format(new_files, new_file_count))
        file_list = current_file_list
        time.sleep(1)

def save_data(data_msg, folder_path, file_extension):
    # 将ROS图像消息转换为OpenCV图像
    cv_image = bridge.imgmsg_to_cv2(data_msg, "bgr8")
    # 使用 random.randint 生成一个随机数ID
    random_id = random.randint(10000, 99999)
    # 构建文件名
    filename = "{}.{}".format(random_id, file_extension)
    file_path = os.path.join(folder_path, filename)
    # 保存图像
    cv2.imwrite(file_path, cv_image)
    print("The data is saved as a file: ", file_path)

class MediaListener(Node):
    def __init__(self, image_topic, folder_path):
        super().__init__('media_listener')
        # 确保文件夹已存在，不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.get_logger().info('A folder has been created: ' + folder_path)
        self.folder_path = folder_path
        self.subscription_image = self.create_subscription(Image, image_topic, self.image_callback, 10)
        self.get_logger().info(f"Start listening for an image topic: {image_topic}")
    def image_callback(self, image_msg):
        """图像话题的回调函数"""
        self.get_logger().info("Image data received") 
        save_data(image_msg, self.folder_path, 'jpg')

def main(args=None):
    rclpy.init(args=args)
    folder_path = input("Please enter the path to the folder where you want to save the file:")
    image_topic = input("Please enter the name of the image topic you want to listen to:")
    media_listener = MediaListener(image_topic, folder_path)
    # 创建并启动文件夹监控线程
    monitor_thread = threading.Thread(target=folder_monitor, args=(folder_path,))
    monitor_thread.start()
    rclpy.spin(media_listener)
    # 关闭节点
    media_listener.destroy_node()
    rclpy.shutdown()
    # 等待文件夹监控线程结束
    monitor_thread.join()

if __name__ == '__main__':
    main()

