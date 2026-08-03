import os
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

def crop_and_recognize_smart():
    original_image_path = os.path.join(os.getcwd(), "windows_screen.png")
    cropped_image_path = os.path.join(os.getcwd(), "keyboard_area.png")
    
    if not os.path.exists(original_image_path):
        print("❌ 找不到原截图，请先运行物理截屏脚本！")
        return

    print("✂️ 正在进行区域提取...")
    img = Image.open(original_image_path)
    width, height = img.size
    
    # 切割出右下角的包含键盘的区域
    crop_left = int(width * 0.6)
    crop_top = int(height * 0.3)
    crop_right = width
    crop_bottom = height
    
    img.crop((crop_left, crop_top, crop_right, crop_bottom)).save(cropped_image_path)
    
    print("🔍 启动 OCR 智能防粘连解析...")
    engine = RapidOCR()
    result, _ = engine(cropped_image_path)
    
    if not result:
        print("❌ 局部画面未识别到任何文本。")
        return

    # === 调试区块：打印 AI 眼里的真实世界 ===
    print("=" * 50)
    print("【OCR 原始识别视野透视】")
    for item in result:
        print(f"原始文本: '{item[1]}' | 坐标框: {item[0]}")
    print("=" * 50)

    keyboard_dict = {}
    captcha_candidate = None
    
    for item in result:
        box, text, score = item
        text = text.strip()
        
        # 计算这一整块文本的局部 Y 轴中心
        local_cy = int((box[0][1] + box[2][1]) / 2)
        absolute_cy = local_cy + crop_top
        
        # 🎯 寻找验证码
        if len(text) == 4 and text.isdigit():
            local_cx = int((box[0][0] + box[2][0]) / 2)
            captcha_candidate = (text, local_cx + crop_left, absolute_cy)
            continue
            
        # 🎯 破解 AI “粘连”：提取这段文本里所有的数字
        digits_in_text = [char for char in text if char.isdigit()]
        
        # 如果包含了 1 到 3 个数字，说明这极大概率是键盘的一排按键（例如 "9 2 8"）或者落单的按键
        if digits_in_text and len(digits_in_text) <= 3:
            box_left = box[0][0]
            box_right = box[1][0]
            box_width = box_right - box_left
            
            # 核心数学逻辑：将整个长框按数字的个数进行物理平分
            step = box_width / len(digits_in_text)
            
            for index, digit in enumerate(digits_in_text):
                # 计算该数字在自身等分网格里的 X 轴中心点
                local_cx = int(box_left + (index + 0.5) * step)
                
                # 补全裁剪掉的边距，还原为物理屏幕绝对坐标
                absolute_cx = local_cx + crop_left
                
                # 存入字典
                keyboard_dict[digit] = (absolute_cx, absolute_cy)

    print("-" * 50)
    print("【最终提取汇总】")
    if len(keyboard_dict) == 10:
        print("🎉 完美！0-9 十个乱序键盘数字物理坐标已全部集齐！")
        for num in "0123456789":
            print(f"数字 [{num}] 坐标 -> {keyboard_dict[num]}")
    else:
        print(f"⚠️ 键盘数字提取了 {len(keyboard_dict)} 个: {list(keyboard_dict.keys())}")
        
    if captcha_candidate:
        print(f"🎉 验证码提取成功！结果: [{captcha_candidate[0]}]，绝对坐标: ({captcha_candidate[1]}, {captcha_candidate[2]})")

if __name__ == "__main__":
    crop_and_recognize_smart()