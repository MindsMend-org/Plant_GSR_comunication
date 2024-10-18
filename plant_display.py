# FoldingCircles 2024 X Plants
# Vis for your plants, will handle pc sleep and awake 2 continue coms.
# A simple starting place for anyone to see what all the contraversal hype has been about since before 1970's

import pygame
import serial
import time
import math

# Initialize Pygame
pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("GSR Visualization")

# Set up the serial connection (adjust 'COM7' and baud rate as needed)
def setup_serial_connection(port='COM7', baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Allow time for the connection to establish
        print("Serial connection established.")
        return ser
    except serial.SerialException:
        print("Failed to connect to serial port. Retrying in 5 seconds...")
        time.sleep(5)
        return setup_serial_connection(port, baudrate)

# Initialize serial connection
ser = setup_serial_connection()

# Define variables
pool = []
background_color = (0, 0, 0)  # Black background
plot_color = (0, 255, 0)  # Green color for GSR plot
high_color = (255, 0, 0)  # Red color for highest GSR plot
low_color = (0, 0, 255)  # Blue color for lowest GSR plot
yellow_color = (255, 255, 0)  # Yellow color for percentage line

global_y_offset = 1
global_multiplier = 1
global_lowest = -25      # -25
global_highest = 730   # 630

global_flip_polarity = True
global_polarity_base = 90
global_polarity_last = -1.0
global_polarity_value = 0.0
global_extracted = 0.0

def polarity_difference(value):
    global global_polarity_value, global_flip_polarity, global_polarity_last
    diff = 0.1

    if value != abs(global_polarity_last):
        diff = abs(value - global_polarity_last)

    if global_flip_polarity:
        diff = global_flip_polarity * diff

    global_flip_polarity = -global_flip_polarity

    global_polarity_value = diff
    global_polarity_last = abs(value)
    return global_polarity_value * 1.618

fullscreen = False  # Track the current window mode (fullscreen or windowed)


def read_arduino_gsr():
    global ser
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            return float(line)
    except (ValueError, serial.SerialException):
        print("Lost connection to the serial port. Attempting to reconnect...")
        ser.close()
        ser = setup_serial_connection()  # Reconnect to the serial port
    return None


def update_pool(value):
    global global_y_offset, global_multiplier, global_highest, global_lowest, global_extracted
    global_extracted = abs(int((value - int(value)) * 10))

    print(f"\rValue: {int(value)}  Extract decimal:{global_extracted} ", end="", flush=True)

    # Adjust the GSR value
    _v = abs(value) * global_multiplier
    value_final = global_y_offset + _v + global_extracted

    # Update global high/low markers
    global_lowest = min(global_lowest, value_final)
    global_highest = max(global_highest, value_final)

    pool.append(value_final)

    # Keep the pool at the desired size
    if len(pool) > width:  # Use the current width to adjust pool size
        pool.pop(0)


def draw_pool():
    screen.fill(background_color)

    gap = global_highest - global_lowest if global_highest > global_lowest else 1

    for x, value in enumerate(pool):
        y = int(height - (value + 100) * (height / 1124))
        ly = int(height - (global_lowest + 100) * (height / 1124))
        hy = int(height - (global_highest + 100) * (height / 1124))

        pygame.draw.line(screen, high_color, (x, hy), (x, hy))
        pygame.draw.line(screen, plot_color, (x, y), (x, y))
        pygame.draw.line(screen, low_color, (x, ly), (x, ly))

        _diff = polarity_difference(y)
        sine_frequency = 0.3
        diff = math.sin(x * sine_frequency) * min(_diff, 15)

        polarity_diff = global_polarity_base + diff
        pygame.draw.line(screen, plot_color, (x - 1, polarity_diff), (x, polarity_diff))

    if pool:
        last_value = pool[-1]
        percent = (last_value - global_lowest) / gap
        yellow_y = int(height - percent * height)
        pygame.draw.line(screen, yellow_color, (0, yellow_y), (width, yellow_y), 2)
        pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Read GSR value
    gsr_value = read_arduino_gsr()
    if gsr_value is not None:
        gsr_value = 10 * gsr_value  # Adjust scaling if needed
        update_pool(gsr_value)
        draw_pool()

# Clean up
ser.close()
pygame.quit()
