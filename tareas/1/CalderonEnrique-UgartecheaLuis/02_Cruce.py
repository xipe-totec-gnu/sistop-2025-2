# Road cross problem implementation with Python threads
# Authors: Enrique Calderón y Luis Ugartechea

# Transit could come from any of the 4 directions and go to any of the 4 directions (north, east, south, west)
# The intersection is a 4-way intersection, composed of 4 sections
# Transit can come from any direction at any time.
# There can not be two cars in the same section of the intersection at the same time.
# A car can not overtake another
# Cars can not invade other lanes
# There should not be starvation. Even if there is constant traffic in one direction, a car coming from another direction should be able to cross.
# The intersection can not be blocked completely.
# Car turns should be modeled
# Avoid deadlock

import threading
import random
import tkinter as tk
import math

# We keep 4 mutexes for the 4 intersection quadrants.
mutexIntersection = [threading.Semaphore(1) for _ in range(4)]

CAR_COLORS = ["red", "blue", "green", "orange", "purple", "pink", "cyan", "magenta", "yellow"]
CAR_EMOJIS = ["🚗", "🚙", "🚕", "🚒", "🚜", "🚌", "🛻", "🏎️", "🏍️"]

# Mutex that uses a queue to have a FIFO behavior
class fifoMutex:
    def __init__(self):
        self.queue = []
        self.lock = threading.Semaphore(1)
        # Condition is used to signal between threads
        self.condition = threading.Condition()

    def acquire(self, id):
        with self.condition:
            self.queue.append(id)
            # We use while instead of if to avoid waking up threads that are not the next
            while self.queue[0] != id:
                # Wait until the condition is notified
                self.condition.wait()
        self.lock.acquire()

    def release(self):
        with self.condition:
            self.queue.pop(0)
            self.lock.release()
            # Notify all threads, if the thread is the next, it will acquire the lock, else it will go to sleep again
            self.condition.notify_all()

# Mutex to control the order of the cars from the same direction
mutexDirection = [fifoMutex() for _ in range(4)]

class IntersectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intersection Simulation with Two Roads per Direction")
        self.root.geometry("1200x1200")
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.control_panel = tk.Frame(root)
        self.control_panel.pack(fill=tk.X, pady=5)
        self.status_label = tk.Label(self.control_panel, text="Simulation Status: Running", font=("Courier", 14))
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.car_count_label = tk.Label(self.control_panel, text="Cars: 0", font=("Courier", 14))
        self.car_count_label.pack(side=tk.RIGHT, padx=10)
        self.canvas.bind("<Configure>", self.draw_intersection)
        self.car_objects = {}
        self.car_count = 0

    def draw_intersection(self, event=None):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.center_x = width // 2
        self.center_y = height // 2

        # Define lane_width so that each road (with two lanes) is wider now
        lane_width = min(width, height) // 12
        self.lane_width = lane_width

        # Draw roads (each direction gets two lanes)
        # Exiting lane north
        self.canvas.create_rectangle(
            self.center_x, 0,
            self.center_x - lane_width, self.center_y - lane_width,
            fill="gray", outline="black"
        )
        # Incoming lane north
        self.canvas.create_rectangle(
            self.center_x + lane_width, 0,
            self.center_x, self.center_y - lane_width,
            fill="gray", outline="black"
        )

        # Exiting lane east
        self.canvas.create_rectangle(
            self.center_x + lane_width, self.center_y,
            width, self.center_y + lane_width,
            fill="gray", outline="black"
        )
        # Incoming lane east
        self.canvas.create_rectangle(
            self.center_x + lane_width, self.center_y - lane_width,
            width, self.center_y,
            fill="gray", outline="black"
        )

        # Exiting lane south
        self.canvas.create_rectangle(
            self.center_x - lane_width, self.center_y + lane_width,
            self.center_x, height,
            fill="gray", outline="black"
        )
        # Incoming lane south
        self.canvas.create_rectangle(
            self.center_x, self.center_y + lane_width,
            self.center_x + lane_width, height,
            fill="gray", outline="black"
        )

        # Exiting lane west
        self.canvas.create_rectangle(
            0, self.center_y - lane_width,
            self.center_x - lane_width, self.center_y,
            fill="gray", outline="black"
        )
        # Incoming lane west
        self.canvas.create_rectangle(
            0, self.center_y,
            self.center_x - lane_width, self.center_y + lane_width,
            fill="gray", outline="black"
        )

        # Draw the intersection square (size = 2 * lane_width)
        # And its quadrants (NW, NE, SE, SW)
        self.intersection_left = self.center_x - lane_width
        self.intersection_top = self.center_y - lane_width
        self.intersection_right = self.center_x + lane_width
        self.intersection_bottom = self.center_y + lane_width

        # Quadrants:
        self.q0 = self.canvas.create_rectangle(
            self.center_x - lane_width, self.center_y - lane_width,
            self.center_x, self.center_y,
            fill="lightgray", outline="white", width=2, tags="q0"
        )
        self.q1 = self.canvas.create_rectangle(
            self.center_x, self.center_y - lane_width,
            self.center_x + lane_width, self.center_y,
            fill="lightgray", outline="white", width=2, tags="q1"
        )
        self.q2 = self.canvas.create_rectangle(
            self.center_x, self.center_y,
            self.center_x + lane_width, self.center_y + lane_width,
            fill="lightgray", outline="white", width=2, tags="q2"
        )
        self.q3 = self.canvas.create_rectangle(
            self.center_x - lane_width, self.center_y,
            self.center_x, self.center_y + lane_width,
            fill="lightgray", outline="white", width=2, tags="q3"
        )

        # Label the roads/directions with larger fonts
        self.canvas.create_text(self.center_x, 30, text="North", font=("Courier", 16, "bold"))
        self.canvas.create_text(width - 60, self.center_y, text="East", font=("Courier", 16, "bold"))
        self.canvas.create_text(self.center_x, height - 30, text="South", font=("Courier", 16, "bold"))
        self.canvas.create_text(60, self.center_y, text="West", font=("Courier", 16, "bold"))

        # Label quadrants with larger font
        self.canvas.create_text(self.center_x - lane_width/2, self.center_y - lane_width/2, text="0", font=("Courier", 14, "bold"))
        self.canvas.create_text(self.center_x + lane_width/2, self.center_y - lane_width/2, text="1", font=("Courier", 14, "bold"))
        self.canvas.create_text(self.center_x + lane_width/2, self.center_y + lane_width/2, text="2", font=("Courier", 14, "bold"))
        self.canvas.create_text(self.center_x - lane_width/2, self.center_y + lane_width/2, text="3", font=("Courier", 14, "bold"))

    # Create a car graphic at the incoming lane of the specified direction.
    def create_car(self, car_id, origin, color, emoji=None):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        lane_width = min(width, height) // 12
        self.lane_width = lane_width

        start_positions = {
            0: (self.center_x - lane_width/2, 50),                              # North incoming (left lane)
            1: (self.canvas.winfo_width() - 50, self.center_y - lane_width/2),  # East incoming (top lane)
            2: (self.center_x + lane_width/2, self.canvas.winfo_height() - 50), # South incoming (right lane)
            3: (50, self.center_y + lane_width/2)                               # West incoming (bottom lane)
        }
        x, y = start_positions[origin]
        car_size = lane_width // 1.7
        car = self.canvas.create_oval(
            x - (car_size/1.5), y - (car_size/1.5),
            x + (car_size/1.5), y + (car_size/1.5),
            fill=color, outline="black", tags=f"car_{car_id}"
        )
        label = self.canvas.create_text(
            x, y, text=str(car_id)+emoji, fill="black", font=("Courier", 20, "bold")
        )
        self.car_objects[car_id] = {"car": car, "label": label, "position": (x, y)}
        self.car_count += 1
        self.car_count_label.config(text=f"Cars: {self.car_count}")
        return car

    def move_car(self, car_id, path_points, speed=100, on_exit=None):
        if car_id not in self.car_objects:
            return
        car_obj = self.car_objects[car_id]
        car = car_obj["car"]
        label = car_obj["label"]

        def animate_path(points, idx=0):
            # If we've reached the end of the path, call on_exit and remove the car.
            if idx >= len(points) - 1:
                if on_exit:
                    on_exit()
                self.canvas.delete(car)
                self.canvas.delete(label)
                del self.car_objects[car_id]
                self.car_count -= 1
                self.car_count_label.config(text=f"Cars: {self.car_count}")
                return

            start_x, start_y = points[idx]
            end_x, end_y = points[idx+1]
            distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            steps = max(int(distance / speed * 10), 1)
            steps = 30
            dx = (end_x - start_x) / steps
            dy = (end_y - start_y) / steps

            def move_step(step=0):
                if step >= steps:
                    car_obj["position"] = (end_x, end_y)
                    # Move on to the next segment
                    self.root.after(10, lambda: animate_path(points, idx+1))
                    return
                self.canvas.move(car, dx, dy)
                self.canvas.move(label, dx, dy)
                self.root.after(10, lambda: move_step(step+1))

            move_step()

        animate_path(path_points)

    def calculate_car_path(self, origin, destiny):
        lane_width = self.lane_width
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cw = width // 2
        ch = height // 2

        start_positions = {
            0: (cw - lane_width/2, 50),                              # North incoming (left lane)
            1: (canvas_width - 50, ch - lane_width/2),               # East incoming (top lane)
            2: (cw + lane_width/2, canvas_height - 50),              # South incoming (right lane)
            3: (50, ch + lane_width/2)                               # West incoming (bottom lane)
        }
        middle_points = {
            0: (cw - lane_width/2, ch - lane_width/2),               # NW quadrant
            1: (cw + lane_width/2, ch - lane_width/2),               # NE quadrant
            2: (cw + lane_width/2, ch + lane_width/2),               # SE quadrant
            3: (cw - lane_width/2, ch + lane_width/2)                # SW quadrant
        }
        exit_points = {
            0: (cw + lane_width/2, 0),                               # North exit (right lane)
            1: (canvas_width, ch + lane_width/2),                    # East exit (bottom lane)
            2: (cw - lane_width/2, canvas_height),                   # South exit (left lane)
            3: (0, ch - lane_width/2)                                # West exit (top lane)
        }

        #Determine the path based on the origin and destiny
        path = []
        if origin == 0 and destiny == 1:
            path = [start_positions[origin], middle_points[0], middle_points[3], middle_points[2], exit_points[destiny]]
        elif origin == 0 and destiny == 2:
            path = [start_positions[origin], middle_points[0], middle_points[3], exit_points[destiny]]
        elif origin == 0 and destiny == 3:
            path = [start_positions[origin], middle_points[0], exit_points[destiny]]
        elif origin == 1 and destiny == 0:
            path = [start_positions[origin], middle_points[1], exit_points[destiny]]
        elif origin == 1 and destiny == 2:
            path = [start_positions[origin], middle_points[1], middle_points[0], middle_points[3], exit_points[destiny]]
        elif origin == 1 and destiny == 3:
            path = [start_positions[origin], middle_points[1], middle_points[0], exit_points[destiny]]
        elif origin == 2 and destiny == 0:
            path = [start_positions[origin], middle_points[2], middle_points[1], exit_points[destiny]]
        elif origin == 2 and destiny == 1:
            path = [start_positions[origin], middle_points[2], exit_points[destiny]]
        elif origin == 2 and destiny == 3:
            path = [start_positions[origin], middle_points[2], middle_points[1], middle_points[0], exit_points[destiny]]
        elif origin == 3 and destiny == 0:
            path = [start_positions[origin], middle_points[3], middle_points[2], middle_points[1], exit_points[destiny]]
        elif origin == 3 and destiny == 1:
            path = [start_positions[origin], middle_points[3], middle_points[2], exit_points[destiny]]
        elif origin == 3 and destiny == 2:
            path = [start_positions[origin], middle_points[3], exit_points[destiny]]
        return path

class Car(threading.Thread):
    def __init__(self, id, origin, destiny, gui):
        threading.Thread.__init__(self)
        self.id = id
        self.origin = origin
        self.destiny = destiny
        self.gui = gui
        self.color = CAR_COLORS[id % len(CAR_COLORS)]
        self.emoji = CAR_EMOJIS[id % len(CAR_EMOJIS)]

    def run(self):
        # Create the car graphic and calculate its path through the intersection.
        self.gui.create_car(self.id, self.origin, self.color, self.emoji)
        path = self.gui.calculate_car_path(self.origin, self.destiny)
        base = (self.origin + 1) % 4

        # Get the lock for the direction
        mutexDirection[self.origin].acquire(self.id)

        # Acquire locks before movement
        if (self.origin + 1) % 4 == self.destiny:
            mutexIntersection[base].acquire()
            self.gui.move_car(
                self.id,
                path,
                on_exit=lambda: self.release_locks([base])
            )
        elif (self.origin + 2) % 4 == self.destiny:
            locks = sorted([base, (base + 1) % 4])
            for l in locks:
                mutexIntersection[l].acquire()
            self.gui.move_car(
                self.id,
                path,
                on_exit=lambda: self.release_locks(list(reversed(locks)))
            )
        else:
            locks = sorted([base, (base + 1) % 4, (base + 2) % 4])
            for l in locks:
                mutexIntersection[l].acquire()
            self.gui.move_car(
                self.id,
                path,
                on_exit=lambda: self.release_locks(list(reversed(locks)))
            )

        # Release the lock for the direction
        mutexDirection[self.origin].release()

    def release_locks(self, locks):
        for l in locks:
            mutexIntersection[l].release()

def spawn_cars(gui, num_cars=10):
    cars_created = 0
    def create_car():
        nonlocal cars_created
        if cars_created < num_cars:
            origin = random.randint(0, 3)
            destiny = random.randint(0, 3)
            while origin == destiny:
                destiny = random.randint(0, 3)
            Car(cars_created, origin, destiny, gui).start()
            cars_created += 1
            gui.root.after(500, create_car)
    gui.root.after(500, create_car)

def main():
    root = tk.Tk()
    gui = IntersectionGUI(root)
    gui.draw_intersection()
    spawn_cars(gui, 100)
    root.mainloop()

if __name__ == "__main__":
    main()