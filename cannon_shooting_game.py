import tkinter as tk
import random

WIDTH, HEIGHT = 600, 400
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
TARGET_WIDTH, TARGET_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
PLAYER_SPEED = 10
BULLET_SPEED = 15
TARGET_SPEED = 5

class ShooterGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Shooter Game for Kids")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(
            WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10,
            WIDTH // 2 + PLAYER_WIDTH // 2, HEIGHT - 10,
            fill="blue"
        )

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot_bullet)

        self.bullets = []
        self.targets = []

        self.spawn_target()

    def move_left(self, event):
        x1, _, _, _ = self.canvas.coords(self.player)
        if x1 > 0:
            self.canvas.move(self.player, -PLAYER_SPEED, 0)

    def move_right(self, event):
        _, _, x2, _ = self.canvas.coords(self.player)
        if x2 < WIDTH:
            self.canvas.move(self.player, PLAYER_SPEED, 0)

    def shoot_bullet(self, event):
        x1, _, x2, _ = self.canvas.coords(self.player)
        bullet = self.canvas.create_rectangle(
            x1 + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 20,
            x1 + PLAYER_WIDTH // 2 + BULLET_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 20 - BULLET_HEIGHT,
            fill="red"
        )
        self.bullets.append(bullet)
        self.move_bullets()

    def move_bullets(self):
        for bullet in self.bullets[:]:
            self.canvas.move(bullet, 0, -BULLET_SPEED)
            if self.canvas.coords(bullet)[1] < 0:
                self.bullets.remove(bullet)
            else:
                self.check_collision(bullet)

        self.root.after(50, self.move_bullets)

    def spawn_target(self):
        x = random.randint(0, WIDTH - TARGET_WIDTH)
        target = self.canvas.create_rectangle(
            x, 0,
            x + TARGET_WIDTH, TARGET_HEIGHT,
            fill="green"
        )
        self.targets.append(target)
        self.move_targets()

    def move_targets(self):
        for target in self.targets[:]:
            self.canvas.move(target, 0, TARGET_SPEED)
            if self.canvas.coords(target)[1] > HEIGHT:
                self.targets.remove(target)

        if self.targets:
            self.root.after(50, self.move_targets)
        else:
            self.spawn_target()

    def check_collision(self, bullet):
        bullet_coords = self.canvas.coords(bullet)
        for target in self.targets[:]:
            target_coords = self.canvas.coords(target)
            if (bullet_coords[0] < target_coords[2] and bullet_coords[2] > target_coords[0] and
                    bullet_coords[1] < target_coords[3] and bullet_coords[3] > target_coords[1]):
                self.canvas.delete(target)
                self.targets.remove(target)
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                break

def main():
    root = tk.Tk()
    game = ShooterGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
