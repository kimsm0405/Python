import tkinter as tk
from tkinter import messagebox
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.frames = []
        self.total_score = 0

    def play_game(self):
        for i in range(10):
            first = random.randint(0, 10)
            if first == 10:
                second = 0
            else:
                second = random.randint(0, 10 - first)
            self.frames.append([first, second])

        if self.frames[9][0] == 10 or sum(self.frames[9]) == 10:
            bonus = random.randint(0, 10)
            self.frames[9].append(bonus)
        else:
            self.frames[9].append(0)

    def calculate_score(self):
        score = 0
        for i in range(10):
            frame = self.frames[i]
            if frame[0] == 10:
                if i < 9:
                    next_frame = self.frames[i + 1]
                    score += 10 + next_frame[0] + (next_frame[1] if next_frame[0] != 10 else self.frames[i + 2][0] if i + 2 < 10 else 0)
                else:
                    score += 10 + frame[2]
            elif sum(frame[:2]) == 10:
                if i < 9:
                    score += 10 + self.frames[i + 1][0]
                else:
                    score += 10 + frame[2]
            else:
                score += sum(frame[:2])
        self.total_score = score

class BowlingGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("볼링 게임")
        self.players = []

        self.labels = []
        self.entries = []

        # 이름 입력창
        for i in range(3):
            label = tk.Label(root, text=f"플레이어 {i+1} 이름:")
            label.grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(root)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.labels.append(label)
            self.entries.append(entry)

        # 게임 시작 버튼
        self.start_button = tk.Button(root, text="게임 시작", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        # 결과 출력
        self.result_text = tk.Text(root, width=50, height=20)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def start_game(self):
        self.players = []
        for entry in self.entries:
            name = entry.get().strip()
            if not name:
                messagebox.showerror("오류", "모든 플레이어의 이름을 입력하세요!")
                return
            player = Player(name)
            self.players.append(player)

        for player in self.players:
            player.play_game()
            player.calculate_score()

        self.show_results()

    def show_results(self):
        self.result_text.delete('1.0', tk.END)

        for player in self.players:
            self.result_text.insert(tk.END, f"{player.name}의 점수:\n")
            for i, frame in enumerate(player.frames):
                frame_str = f"프레임 {i+1}: {frame[:2]}"
                if i == 9 and frame[2] > 0:
                    frame_str += f" + 보너스: {frame[2]}"
                self.result_text.insert(tk.END, frame_str + "\n")
            self.result_text.insert(tk.END, f">>> 총점: {player.total_score}\n\n")

        winner = max(self.players, key=lambda p: p.total_score)
        self.result_text.insert(tk.END, f" 최종 우승자: {winner.name} (총점: {winner.total_score}) \n")

# 메인 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = BowlingGameGUI(root)
    root.mainloop()

    
 
