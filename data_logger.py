import matplotlib.pyplot as plt 


class DataLogger:
    """
    Class to log what happened during the simulation
    """

    def __init__(self, cell_list: list):
        self.cell_list = cell_list
        self.cell_count = []

    def counting_cell(self):
        self.cell_count.append(len(self.cell_list))

    def draw_cell_number_by_time(self):
        plt.plot([i/10000 for i in range(len(self.cell_count))],
                 self.cell_count)
        plt.title("Number of cell by time")
        plt.ylabel("Number of cell")
        plt.xlabel("Time (Arbitary units)")
        plt.show()
