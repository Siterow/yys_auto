import os
import cv2
import numpy as np
import pyautogui
from typing import Tuple, Optional


class ImageLocator:
    def __init__(self, images_dir: str = "resources/images"):
        """
        初始化图像定位器
        
        :param images_dir: 图片资源目录的相对路径
        """
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.base_path, images_dir)
        
    def locate_on_screen(self, image_name: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        在屏幕上定位指定图片的位置
        
        :param image_name: 图片文件名（需要包含在resources/images目录中）
        :param confidence: 匹配置信度阈值（0-1之间）
        :return: 返回找到的位置坐标(x, y)，如果未找到则返回None
        """
        image_path = os.path.join(self.images_dir, image_name)
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                return location.x, location.y
        except Exception as e:
            print(f"定位图片时出错: {e}")
        return None
    
    def click_image(self, image_name: str, confidence: float = 0.8, delay: float = 1.0) -> bool:
        """
        点击屏幕上匹配的图片位置
        
        :param image_name: 图片文件名
        :param confidence: 匹配置信度阈值
        :param delay: 点击前的延迟时间（秒）
        :return: 是否成功点击
        """
        location = self.locate_on_screen(image_name, confidence)
        if location:
            x, y = location
            pyautogui.sleep(delay)
            print(f"点击图片 {image_name} 在位置：({x}, {y})")
            pyautogui.click(x, y)
            return True
        print(f"未找到图片: {image_name}")
        return False
    
    def wait_and_click_image(self, image_name: str, timeout: int = 10, confidence: float = 0.8) -> bool:
        """
        等待图片出现并点击
        
        :param image_name: 图片文件名
        :param timeout: 超时时间（秒）
        :param confidence: 匹配置信度阈值
        :return: 是否成功点击
        """
        start_time = pyautogui.time.time()
        while pyautogui.time.time() - start_time < timeout:
            if self.click_image(image_name, confidence):
                return True
            pyautogui.sleep(1)
        return False 