import random
import threading
import time
import tkinter as tk
import random

# This code simulates a gym where random people (brawny) train with different equipment.
# Each brawny has a unique ID and a list of equipment they will use for training.
# Up to 3 brawny can train at the same time with the same equipment.
# The code uses threading to simulate concurrent training sessions.


EQUIPMENT_NUM = 60
MAX_BRAWNY = EQUIPMENT_NUM * 3

#List of colors for brawny
BRAWNY_COLORS = [
    "red", "blue", "green", "yellow", "purple", "orange", "pink", "brown",
    "gray", "cyan", "magenta"
]

# To limit the number of brawny that can train at the same time with the same equipment
class Equipment:
    def __init__(self, id: int):
        self.id = id # Equipment ID
        self.training_num = 0
        self.training_num_lock = threading.Semaphore(1)

    def __str__(self):
        return f"Equipment #{self.id}"

# Simulate the gym

# List of equipment in the gym
equipment_list = []
for i in range(EQUIPMENT_NUM):
   equipment_list.append(Equipment(i))

# Number of brawny in the gym counter, including a lock
brawnyInGym = 0
brawnyInGymLock = threading.Semaphore(1)

# Brawny class
# Each brawny has an ID, a training number, and a list of equipment they will use for training
# The training number indicates how many exercises the brawny will do
# The training equipment list is generated randomly, representing the equipment the brawny will use
# The brawny will enter the gym, train with the equipment, and leave the gym
# The brawny will wait if the gym is full
# The brawny will also check if the equipment is available (not in use by 3 or more brawny)
# The brawny will leave the gym if all the equipment is full and he has already done 5 exercises
class Brawny(threading.Thread):
    def __init__(self, id: int, gym_gui):
        super().__init__()
        self.id = id
        self.gym_gui = gym_gui
        self.training_num = random.randint(6,10)
        self.training_num_original = self.training_num # Original number of training exercises
        self.training_equipment = [] # Training routine list
        self.color = random.choice(BRAWNY_COLORS)

        # Generate a random list of equipment for training
        while len(self.training_equipment) < self.training_num:
            equipment = random.randint(0, EQUIPMENT_NUM-1)
            if equipment not in self.training_equipment:
                self.training_equipment.append(equipment)
        # Sort the equipment list to ensure consistent order and avoid deadlocks
        sorted(self.training_equipment)

    def __str__(self):
        return f"Brawny {self.id}"

    def run(self):
        while True:
            global brawnyInGym
            global brawnyInGymLock

            #Try to enter the gym until the brawny can enter and train
            while True:
                # Check if the gym is full
                brawnyInGymLock.acquire()
                if brawnyInGym < MAX_BRAWNY:
                    # Enter the gym, increment the counter of brawny in the gym
                    brawnyInGym += 1
                    brawnyInGymLock.release()

                    # Enter the gym and training
                    # Draw the brawny in the gym
                    self.gym_gui.create_brawny(self.id, 50, 100, self.color)
                    print(f"{self} has entered the gym")
                    self.train()


                    # Leave the gym, decrement the counter of brawny in the gym
                    brawnyInGymLock.acquire()
                    brawnyInGym -= 1
                    brawnyInGymLock.release()
                    print(f"{self} has left the gym")
                    break
                else:
                    brawnyInGymLock.release()
                    # Wait for a while before checking again
                    print(f"{self} is returning later")
                    time.sleep(random.randint(1, 3))

    def train(self):
        global equipment_list

        # If the brawny is in the gym, start training until all exercises are done
        while self.training_num > 0:
            # Get the position of the gym
            width = self.gym_gui.canvas.winfo_width()
            height = self.gym_gui.canvas.winfo_height()
            x_center = width // 2
            y_center = height // 2
            cols = 10
            rows = 6
            rect_width = 100
            rect_height = 100
            padding = 50
            tn = self.training_num
            #Move the brawny to the gym in the top left corner
            square_x1 = x_center - (cols * (rect_width + padding) // 2) - (padding // 2)
            square_y1 = y_center - (rows * (rect_height + padding) // 2) - (padding // 2)

            #Calculate the path to the first equipment
            path_points = []
            path_points.append([50, 100])
            path_points.append([square_x1, square_y1])
            self.gym_gui.move_brawny(self.id, path_points)

            # Search for the equipment
            for equipment in self.training_equipment:
                # Check if the equipment is available (not in use by 3 or more brawnies)
                equipment_list[equipment].training_num_lock.acquire()
                if equipment_list[equipment].training_num < 3:
                    equipment_list[equipment].training_num += 1
                    equipment_list[equipment].training_num_lock.release()

                    # Simulate training time
                    print(f"{self} is using {equipment_list[equipment]}")
                    time.sleep(1)

                    # Release the equipment after training
                    equipment_list[equipment].training_num_lock.acquire()
                    equipment_list[equipment].training_num -= 1
                    equipment_list[equipment].training_num_lock.release()

                    # Decrease the number of exercises left
                    self.training_num -= 1
                    self.training_equipment.remove(equipment)
                else:
                    # If the equipment is full, release the lock and try next equipment
                    equipment_list[equipment].training_num_lock.release()
                    print(f"{self} cannot use {equipment_list[equipment]} because it is full")

            # Check if all the equipment are full
            if tn == self.training_num:
                # If the brawny has done 5 exercises, he can leave the gym
                if self.training_num_original - self.training_num > 5:
                    break

        if self.training_num == 0:
            print(f"{self} has finished training")
        else:
            print(f"{self} has left the gym without finishing training")

class GymGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Simulator")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack(fill=tk.X, pady=5)
        self.status_label = tk.Label(self.control_panel, text="Status: Waiting for brawny to enter the gym", font=("Courier", 14))
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.brawny_count = 0
        self.brawny_count_label = tk.Label(self.control_panel, text="Brawny in gym: 0", font=("Courier", 14))
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.canvas.bind("<Configure>", self.draw_gym)
        self.brawny_objects = {}

    def draw_gym(self, event=None):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.x_center = width // 2
        self.y_center = height // 2
        self.equipment_num = EQUIPMENT_NUM
        # Draw the gym

        # Draw rectangles representing the equipment
        rect_width = 100
        rect_height = 100
        rows = 6
        cols = 10
        padding = 50
        # Draw the gym square outline
        square_x1 = self.x_center - (cols * (rect_width + padding) // 2) - 50
        square_y1 = self.y_center - (rows * (rect_height + padding) // 2) - 30
        square_x2 = self.x_center + (cols * (rect_height + padding) // 2)
        square_y2 = self.y_center + (rows * (rect_height + padding) // 2)
        self.canvas.create_rectangle(square_x1, square_y1, square_x2, square_y2, outline="black", width=4)
        for r in range(rows):
            for c in range(cols):
                x1 = self.x_center - (cols * (rect_width + padding) // 2) + c * (rect_width + padding)
                y1 = self.y_center - (rows * (rect_height + padding) // 2) + r * (rect_height + padding)
                x2 = x1 + rect_width
                y2 = y1 + rect_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray", outline="black", width=2)
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"Equipment\n{r * cols + c}", font=("Courier", 12), anchor="center", justify="center")

        # entrance tourniquet
        # Draw entrance tourniquet on the left of the canvas
        tourniquet_width = 100
        tourniquet_height = 125
        x1 = 10
        y1 = 30
        x2 = x1 + tourniquet_width
        y2 = y1 + tourniquet_height
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black", width=2)
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Entrance", font=("Courier", 12), anchor="center", justify="center", fill="white")

        #lidsol
        lidsol_width = 100
        lidsol_width = 125
        y1 = height - 80 - lidsol_width
        x2 = 110
        y2 = y1 + lidsol_width
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black", width=2)
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="LIDSoL", font=("Courier", 12), anchor="center", justify="center", fill="white")

    def get_equipment_position(self, equipment_id):
        pos = []
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        x_center = width // 2
        y_center = height // 2
        rect_width = 100
        rect_height = 100
        rows = 6
        cols = 10
        padding = 50
        x_top = x_center - (cols * (rect_width + padding) // 2) + rect_width // 2
        y_top = y_center - (rows * (rect_height + padding) // 2) + rect_height // 2

        # Calculate the position of the equipment with the given ID
        row = equipment_id // cols
        col = equipment_id % cols

        pos.append(x_top + col * (rect_width + padding))
        pos.append(y_top + row * (rect_height + padding))

        return pos

    def create_brawny(self, brawny_id, x, y, color):
        radius = 20
        brawny = self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline="black"
        )
        label = self.canvas.create_text(
            x, y,
            text=str(brawny_id),
            font=("Courier", 10, "bold"),
            fill="white"
        )
        self.brawny_objects[brawny_id] = {"brawny": brawny, "label": label, "x_pos": x, "y_pos": y}

        # Update the brawny count label
        self.brawny_count += 1
        self.brawny_count_label.config(text=f"Brawny in gym: {self.brawny_count}")
        return brawny

    def calculate_brawny_path(self, brawny_id, origin_equipment_id, destination_equipment_id):
        rect_width = 100
        rect_height = 100
        padding = 50
        # Calculate the actual brawny position (origin) based on the equipment ID
        path_points = []
        origin = self.get_equipment_position(origin_equipment_id)
        path_points.append(origin)

        # Calculate the path points
        # Get to bottom left corner of the rectangle in hallway crossing
        path_points.append([origin[0] - (rect_width // 2) - (padding // 2), origin[1] - (rect_height // 2) - (padding // 2)])
        # If it is going left or right
        if origin[0] > destination[0]:
            # Going left
            path_points.append([destination[0] + (rect_width // 2) + (padding // 2), origin[1] - (rect_height // 2) - (padding // 2)])
            # If it is going up or down
            path_points.append([destination[0] + (rect_width // 2) + (padding // 2), destination[1]])
        else:
            # Going right
            path_points.append([destination[0] - (rect_width // 2) - (padding // 2), origin[1] - (rect_height // 2) - (padding // 2)])
            # If it is going up or down
            path_points.append([destination[0] - (rect_width // 2) - (padding // 2), destination[1]])
        # Get to the center of the rectangle
        destination = self.get_equipment_position(destination_equipment_id)
        path_points.append(destination)

        return path_points

    def move_brawny(self, brawny_id, path_points, speed=100, on_exit=None):
        # Move the brawny along the path points

        # Verify if the brawny exists
        if brawny_id not in self.brawny_objects:
            return

        brawny_obj = self.brawny_objects[brawny_id]
        # Get the brawny object and label
        brawny = brawny_obj["brawny"]
        label = brawny_obj["label"]

        #Animation
        def animate_paths(points, idx=0):
            #If we reached the end of the path remove the car
            if idx < len(points) - 1:
                if on_exit:
                    on_exit()
                self.canvas.delete(brawny)
                self.canvas.delete(label)
                del self.brawny_objects[brawny_id]
                #Update the brawny count label
                self.brawny_count -= 1
                self.brawny_count_label.config(text=f"Brawny in gym: {self.brawny_count}")
                return

            #Get path distance
            start_x, start_y = points[idx]
            end_x, end_y = points[idx + 1]
            distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
            steps = 30
            dx = (end_x - start_x) / steps
            dy = (end_y - start_y) / steps

            def move_step(step):
                if step >= steps:
                    # Move to the next point
                    brawny_obj["x_pos"] = end_x
                    brawny_obj["y_pos"] = end_y
                    self.root.after(10, lambda: animate_paths(points, idx + 1))
                    return
                self.canvas.move(brawny, dx, dy)
                self.canvas.move(label, dx, dy)
                self.root.after(10, lambda: move_step(step + 1))

            move_step()

        animate_paths(path_points)

# Function to spawn and start a brawny thread
def spawn_brawnies(gym_gui, num_brawny=10):
    brawnies_count = 0

    def spawn_brawny():
        nonlocal brawnies_count
        if brawnies_count < num_brawny:
            brawny = Brawny(brawnies_count, gym_gui)
            brawny.start()
            brawnies_count += 1
            # Schedule the next spawn
            gym_gui.root.after(random.randint(1000, 3000), spawn_brawny)

    gym_gui.root.after(1000, spawn_brawny)

def main():
    print("Starting the gym simulation")
    root = tk.Tk()
    gym_gui = GymGUI(root)
    gym_gui.draw_gym()  # Draw the gym after the canvas is ready

    # Start the brawny threads
    spawn_brawnies(gym_gui, num_brawny=10)
    root.mainloop()

if __name__ == "__main__":
    main()