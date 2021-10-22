import csv
import copy

class CSVReader:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def read_and_parse_file(self):

        self.waypoints = []
        with open(self.file_name, 'r') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                self.waypoints.append(row)

        return copy.deepcopy(self.waypoints)

    def print_waypoints(self):
        print(self.waypoints)


