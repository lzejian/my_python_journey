import pyautogui
import os

def test_windows_screenshot():
    print("📸 正在调用 Windows 底层物理截屏...")
    # 直接截取你整个显示器的画面
    img = pyautogui.screenshot()
    
    image_path = os.path.join(os.getcwd(), "windows_screen.png")
    img.save(image_path)
    print(f"✅ 截屏成功！图片已保存至: {image_path}")

if __name__ == "__main__":
    test_windows_screenshot()