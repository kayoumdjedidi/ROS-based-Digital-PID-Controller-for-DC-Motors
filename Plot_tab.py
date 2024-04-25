import csv
import matplotlib.pyplot as plt

# Read data from CSV file
data = []
with open('table.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)


# Plot first column as x and second column as y
x_data = [float(row[0]) for row in data]
y_data = [float(row[1]) for row in data]
plt.figure()
plt.subplot(2,2,1)
plt.plot(x_data, y_data, marker='o', linestyle='-')
plt.xlabel('PWM')
plt.ylabel('Motor Voltage')
plt.title('Motor Voltage en fonction du PWM')
plt.grid(True)


# Plot first column as x and third column as y
x_data = [float(row[0]) for row in data]
y_data = [float(row[2]) for row in data]
plt.subplot(2,2,2)
plt.plot(x_data, y_data, marker='o', linestyle='-')
plt.xlabel('PWM')
plt.ylabel('Motor RPM')
plt.title('Motor RPM en fonction du PWM')
plt.grid(True)


# Plot first column as x and fourth column as y
x_data = [float(row[0]) for row in data]
y_data = [float(row[3]) for row in data]
plt.subplot(2,2,3)
plt.plot(x_data, y_data, marker='o', linestyle='-')
plt.xlabel('PWM')
plt.ylabel('Gear RPM')
plt.title('Gear RPM en fonction du PWM')
plt.grid(True)
plt.show()
