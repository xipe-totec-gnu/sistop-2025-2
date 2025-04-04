import random
import threading
import time

# This code simulates a gym where random people (brawny) train with different equipment.
# Each brawny has a unique ID and a list of equipment they will use for training.
# Up to 3 brawny can train at the same time with the same equipment.
# The code uses threading to simulate concurrent training sessions.

# Global variables
EQUIPMENT_NUM = 10
MAX_BRAWNY = EQUIPMENT_NUM * 3

# Equipment class
# Each equipment has an ID and a training number
# The training number indicates how many brawny are using this equipment, including a lock
class Equipment:
    def __init__(self, id: int):
        self.id = id
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
# The brawny will also check if the equipment is available (not in use by 3 or more brawnies)
# The brawny will leave the gym if all the equipment is full and he has already done 5 exercises

class Brawny(threading.Thread):
    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.training_num = random.randint(6,10)
        self.training_num_original = self.training_num # Original number of training exercises
        self.training_equipment = []

        # Generate a random list of equipment for training
        while len(self.training_equipment) < self.training_num:
            equipment = random.randint(0, EQUIPMENT_NUM-1)
            if equipment not in self.training_equipment:
                self.training_equipment.append(equipment)
        # Sort the equipment list to ensure consistent order and avoid deadlocks
        sorted(self.training_equipment)

    def __str__(self):
        return f"Brawny #{self.id}"

    def run(self):
        global brawnyInGym
        global brawnyInGymLock

        # Try to enter the gym until the brawny can enter and train
        while True:
            # Check if the gym is full
            brawnyInGymLock.acquire()
            if brawnyInGym < MAX_BRAWNY:
                # Enter the gym, increment the counter of brawny in the gym
                brawnyInGym += 1
                brawnyInGymLock.release()

                # Enter the gym and start training
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
            tn = self.training_num
            # Search for the equipment
            for equipment in self.training_equipment:
                # Check if the equipment is available (not in use by 3 or more brawny)
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

# Function to spawn and start a brawny thread
def spawn_brawny(brawny_id: int):
    brawny = Brawny(brawny_id)
    print(f"Spawning {brawny}")
    brawny.start()

# Main function
def main():
    print("Starting the gym simulation")
    for i in range(MAX_BRAWNY):
        # Spawn a new brawny thread
        spawn_brawny(i)
        # Sleep for a random time before spawning the next brawny
        time.sleep(random.randint(1, 2))

# Run the main function
if __name__ == "__main__":
    main()
