import tkinter as tk
import random
import heapq

class UserSnake:
    def __init__(self, master, score_frame):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("820x450")  # Adjusted width for two side-by-side canvases
        self.master.resizable(False, False)

        # Left canvas for User Operated Snake
        self.canvas1 = tk.Canvas(self.master, bg="black", width=400, height=400, borderwidth=2, highlightthickness=0)
        self.canvas1.pack(side=tk.LEFT)
        #self.canvas1.create_rectangle(0, 0, 400, 400, outline="white")

        self.score_label1 = tk.Label(score_frame, text="User Snake Length: 3", font=("Helvetica", 12), fg="white", bg="black")
        self.score_label1.pack(side=tk.LEFT)

        self.snake1 = [(100, 100), (90, 100), (80, 100)]
        self.direction1 = "Right"

        self.food1 = self.create_food(self.canvas1)

        self.master.bind("<KeyPress>", self.change_direction)

        self.update()

    def create_food(self, canvas):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            food_coords = (x, y, x + 20, y + 20)
            food = canvas.create_rectangle(*food_coords, fill="red", tags="food")
            if all(canvas.itemcget(s, 'fill') != 'green' for s in canvas.find_overlapping(x, y, x + 20, y + 20)):
                break
            canvas.delete(food)
        return food

    def move_snake(self):
        head = self.snake1[0]
        if self.direction1 == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction1 == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction1 == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction1 == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake1.insert(0, new_head)
        self.snake1.pop()

    def update(self):
        self.move_snake()

        head = self.snake1[0]
        self.canvas1.delete("snake")
        for segment in self.snake1:
            self.canvas1.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green",
                                         tags="snake")

        food_coords = self.canvas1.coords(self.food1)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake1.append((0, 0))  # Just to increase the length
            self.canvas1.delete("food")
            self.food1 = self.create_food(self.canvas1)
            self.update_score()

        # Check for boundaries and self-collisions
        if head[0] < 0 or head[0] > 380 or head[1] < 0 or head[1] > 380 or head in self.snake1[1:]:
            self.game_over()

        self.master.after(200, self.update)

    def game_over(self):
        self.canvas1.create_text(200, 210, text="Game Over", font=("Helvetica", 20), fill="red")
        self.master.unbind("<KeyPress>")
        self.display_result()

    def display_result(self):
        length_user = len(self.snake1)
        length_ai = len(game2.snake2)
        result = "It's a tie!" if length_user == length_ai else \
                 "User Snake wins!" if length_user > length_ai else "AI Snake wins!"

        result_text = f"User Snake Length: {length_user}\nAI Snake Length: {length_ai}\n{result}"

        result_label = tk.Label(self.master, text=result_text, font=("Helvetica", 16), fg="white", bg="black")
        result_label.place(relx=0.5, rely=0.5, anchor="center")

    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction1 == "Left":
            self.direction1 = "Right"
        elif event.keysym == "Left" and not self.direction1 == "Right":
            self.direction1 = "Left"
        elif event.keysym == "Up" and not self.direction1 == "Down":
            self.direction1 = "Up"
        elif event.keysym == "Down" and not self.direction1 == "Up":
            self.direction1 = "Down"

    def update_score(self):
        length = len(self.snake1)
        self.score_label1.config(text=f"User Snake Length: {length}")


class AISnake:
    def __init__(self, master, score_frame):
        self.master = master
        self.master.title("AI Operated Snake (Snake Game)")

        # Right canvas for AI Operated Snake
        self.canvas2 = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas2.pack(side=tk.LEFT)

        self.score_label2 = tk.Label(score_frame, text="AI Snake Length: 3", font=("Helvetica", 12), fg="white", bg="black")
        self.score_label2.pack(side=tk.LEFT)

        self.snake2 = [(100, 100), (90, 100), (80, 100)]
        self.direction2 = "Right"

        self.food2 = self.create_food(self.canvas2)

        self.update()

    def create_food(self, canvas):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            food_coords = (x, y, x + 20, y + 20)
            food = canvas.create_rectangle(*food_coords, fill="red", tags="food")
            if all(canvas.itemcget(s, 'fill') != 'green' for s in canvas.find_overlapping(x, y, x + 20, y + 20)):
                break
            canvas.delete(food)
        return food

    def move_snake(self, target):
        head = self.snake2[0]
        path = self.astar_search(head, target)
        if len(path) > 1:
            new_head = path[1]
            if new_head not in self.snake2 or head[0] > 0 or head[0] < 360 or head[1] > 0 or head[1] < 360:  # Check for self-collision
                self.snake2.insert(0, new_head)
                self.snake2.pop()

    def get_neighbors(self, node):
        x, y = node
        neighbors = [(x + 20, y), (x - 20, y), (x, y + 20), (x, y - 20)]
        # Filter the neighbors to stay within the boundaries and avoid the snake itself
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < 400 and 0 <= ny < 400 and (nx, ny) not in self.snake2]

    def update(self):
        head = self.snake2[0]

        self.canvas2.delete("snake")
        for segment in self.snake2:
            self.canvas2.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake")

        food_coords = self.canvas2.coords(self.food2)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake2.append((0, 0))  # Just to increase the length
            self.canvas2.delete("food")
            self.food2 = self.create_food(self.canvas2)
            self.update_score()

        target = (food_coords[0], food_coords[1])
        self.move_snake(target)

        self.master.after(200, self.update)

    def display_result(self):
        length_user = len(game1.snake1)
        length_ai = len(self.snake2)
        result = "It's a tie!" if length_user == length_ai else \
                 "User Snake wins!" if length_user > length_ai else "AI Snake wins!"

        result_text = f"User Snake Length: {length_user}\nAI Snake Length: {length_ai}\n{result}"

        result_label = tk.Label(self.master, text=result_text, font=("Helvetica", 16), fg="white", bg="black")
        result_label.place(relx=0.5, rely=0.5, anchor="center")

    def astar_search(self, start, goal):
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                path = []
                while current_node is not None:
                    path.insert(0, current_node)
                    current_node = came_from[current_node]
                return path

            for next_node in self.get_neighbors(current_node):
                new_cost = cost_so_far[current_node] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current_node

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def update_score(self):
        length = len(self.snake2)
        self.score_label2.config(text=f"AI Snake Length: {length}")

if __name__ == "__main__":
    root = tk.Tk()
    score_frame = tk.Frame(root, highlightbackground="white", highlightthickness=2)
    score_frame.pack(side="bottom", fill="x")

    game1 = UserSnake(root, score_frame)
    game2 = AISnake(root, score_frame)

    # Set a time limit of 60 seconds
    root.after(60000, game1.display_result)
    root.after(60000, game2.display_result)

    root.mainloop()