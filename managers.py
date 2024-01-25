import os
import pickle

class Manager:
    def __init__(self, type):
        self.base_path = os.path.realpath(os.path.dirname(__file__))
        self.type = type
        try:
            self.manage = self.load()
        except FileNotFoundError:
            with open(f"{self.base_path}/{self.type}.dat", "wb") as f:
                self.manage = [f"{self.type}", {}]
                pickle.dump(self.manage, f)
    
    def clear(self):
        with open(f"{self.base_path}/{self.type}.dat", "wb") as f:
            self.manage = [f"{self.type}", {}]
            pickle.dump(self.manage, f)


    def save(self):
        with open(f"{self.base_path}/{self.type}.dat", "wb") as f:
            pickle.dump(self.manage, f)

    
    def load(self):
        with open(f"{self.base_path}/{self.type}.dat", "rb") as f:
            return pickle.load(f)