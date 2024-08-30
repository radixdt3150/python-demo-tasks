import csv

# Example structure
data = [
    {"Column1": "Value1", "Column2": "Value2"},
    {"Column1": "Value3", "Column2": "Value4"},
]

with open("output.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Column1", "Column2"])
    writer.writeheader()
    writer.writerows(data)
