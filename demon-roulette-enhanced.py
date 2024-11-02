import tkinter as tk
from tkinter import messagebox
import random
import math


class DemonRouletteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("恶魔轮盘")
        self.root.geometry("800x800")

        # 设置轮盘区域
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(pady=20)

        # 游戏数据
        self.player_hp = 100
        self.player_gold = 100
        self.is_spinning = False
        self.current_angle = 0  # 记录轮盘当前角度
        self.segments = [
            ("奖励 100 金币", "green"),
            ("惩罚 50 金币", "red"),
            ("神秘事件", "blue"),
            ("奖励 50 金币", "yellow"),
            ("惩罚 100 金币", "orange"),
            ("双倍奖励", "purple"),
        ]

        # 初始化轮盘和按钮
        self.create_roulette()
        self.spin_button = tk.Button(root, text="转动轮盘", command=self.start_spin)
        self.spin_button.pack(pady=20)

        # 显示玩家状态
        self.status_label = tk.Label(root, text=f"生命值: {self.player_hp} | 金币: {self.player_gold}")
        self.status_label.pack(pady=10)

    def create_roulette(self):
        """绘制轮盘的不同扇形区域"""
        start_angle = 0
        angle_per_segment = 360 / len(self.segments)

        for segment, color in self.segments:
            end_angle = start_angle + angle_per_segment
            self.canvas.create_arc(
                50, 50, 550, 550, start=start_angle, extent=angle_per_segment,
                fill=color, outline="black"
            )
            start_angle = end_angle

    def start_spin(self):
        """开始轮盘旋转"""
        if not self.is_spinning:
            self.is_spinning = True
            self.spin_speed = 20  # 初始速度
            self.animate_spin()

    def animate_spin(self):
        """轮盘旋转的动画效果"""
        if self.spin_speed > 0:
            self.current_angle = (self.current_angle + self.spin_speed) % 360
            self.canvas.delete("pointer")  # 删除旧的指针
            self.canvas.create_line(300, 300, 300 + 250 * math.cos(math.radians(self.current_angle)),
                                    300 - 250 * math.sin(math.radians(self.current_angle)),
                                    fill="black", width=3, tags="pointer")

            # 随机减少速度，模拟减速效果
            self.spin_speed -= random.uniform(0.1, 0.5)
            self.root.after(20, self.animate_spin)
        else:
            self.is_spinning = False
            self.finalize_spin()

    def finalize_spin(self):
        """计算轮盘最终结果并更新状态"""
        # 计算当前指针指向的区域
        angle_per_segment = 360 / len(self.segments)
        selected_segment = int((self.current_angle % 360) / angle_per_segment)
        result, color = self.segments[selected_segment]

        # 根据结果更新玩家状态，添加检查以防止 IndexError
        if "奖励" in result:
            try:
                reward = int(result.split()[1])
                self.player_gold += reward
                messagebox.showinfo("结果", f"你获得了 {reward} 金币！")
            except (IndexError, ValueError):
                messagebox.showinfo("结果", "解析奖励出现问题，未能获得奖励。")

        elif "惩罚" in result:
            try:
                penalty = int(result.split()[1])
                self.player_gold -= penalty
                messagebox.showinfo("结果", f"你损失了 {penalty} 金币！")
            except (IndexError, ValueError):
                messagebox.showinfo("结果", "解析惩罚出现问题，未能扣除金币。")

        elif "神秘事件" in result:
            mystery_reward = random.randint(-100, 100)
            self.player_gold += mystery_reward
            if mystery_reward > 0:
                messagebox.showinfo("结果", f"神秘奖励！你获得了 {mystery_reward} 金币！")
            else:
                messagebox.showinfo("结果", f"神秘惩罚！你损失了 {abs(mystery_reward)} 金币！")

        elif "双倍奖励" in result:
            reward = random.choice([50, 100])
            self.player_gold += 2 * reward
            messagebox.showinfo("结果", f"双倍奖励！你获得了 {2 * reward} 金币！")

        # 更新状态显示
        self.update_status()

    def update_status(self):
        """更新状态标签"""
        self.status_label.config(text=f"生命值: {self.player_hp} | 金币: {self.player_gold}")


# 运行游戏
if __name__ == "__main__":
    root = tk.Tk()
    app = DemonRouletteGUI(root)
    root.mainloop()
