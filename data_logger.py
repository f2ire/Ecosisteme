import matplotlib.pyplot as plt


class DataLogger:
  """Class to use and log data
  Object contening data to study
  Attribute
  -------
  cell_list : list
      List of data to study (actually a cells list)
  cell_count : list
      List of the number of cell by time
  Methods
  -------
  counting_cell(self) -> None
      Update cell_count and add it the length of the latest self.cell_list
  draw_cell_number_by_time(self) -> None
      Draw a representation of number of cell by time
  """

  def __init__(self, cell_list: list):
    """
    Object to log the data
    Parameters
    ----------
    cell_list : list
        List of cells to log and study
    """
    self.cell_list = cell_list
    self.cell_count = []


  def counting_cell(self):
    self.cell_count.append(len(self.cell_list))


  def draw_cell_number_by_time(self):
    plt.plot([i / 10000 for i in range(len(self.cell_count))], self.cell_count)
    plt.title("Number of cell by time")
    plt.ylabel("Number of cell")
    plt.xlabel("Time (Arbitary units)")
    plt.show()