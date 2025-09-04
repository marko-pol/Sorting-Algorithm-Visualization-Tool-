import tkinter as tk
from tkinter import ttk
import random
import time


# Sorting algorithms
def bubble_sort(arr, draw_array, time_step, step_limit=5):
    n = len(arr)
    step_counter = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

            step_counter += 1
            if step_counter >= step_limit:
                draw_array(arr)
                time.sleep(time_step)
                step_counter = 0



def merge_sort(arr, draw_array, time_step):
    def merge_sort_recursive(array, left, right):
        if left < right:
            mid = (left + right) // 2

            # Sort the left half
            merge_sort_recursive(array, left, mid)
            # Sort the right half
            merge_sort_recursive(array, mid + 1, right)

            # Merge the sorted halves
            merge(array, left, mid, right)

    def merge(array, left, mid, right):
        left_half = array[left:mid + 1]
        right_half = array[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                array[k] = left_half[i]
                i += 1
            else:
                array[k] = right_half[j]
                j += 1
            k += 1
            draw_array(arr)  # Visualize the entire array
            time.sleep(time_step)

        # Copy the remaining elements of left_half, if any
        while i < len(left_half):
            array[k] = left_half[i]
            i += 1
            k += 1
            draw_array(arr)  # Visualize the entire array
            time.sleep(time_step)

        # Copy the remaining elements of right_half, if any
        while j < len(right_half):
            array[k] = right_half[j]
            j += 1
            k += 1
            draw_array(arr)  # Visualize the entire array
            time.sleep(time_step)

    merge_sort_recursive(arr, 0, len(arr) - 1)


def bucket_sort(arr, draw_array, time_step):
    max_value = max(arr)
    size = len(arr)

    bucket_count = size // 3
    buckets = [[] for _ in range(bucket_count)]

    for i, num in enumerate(arr):
        index = int(bucket_count * num / (max_value + 1))
        buckets[index].append(num)
        draw_array(arr)
        time.sleep(time_step)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))

    for i in range(len(arr)):
        arr[i] = sorted_arr[i]
        draw_array(arr)
        time.sleep(time_step)


def insertion_sort(arr, draw_array, time_step):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        draw_array(arr)
        time.sleep(time_step)


def generate_data(size, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(size)]


# Visualization Function
def draw_array(arr, canvas, canvas_height, highlight=None):
    canvas_width = canvas.winfo_width()
    bar_width = canvas_width / len(arr)

    canvas.delete("all")
    for i, height in enumerate(arr):
        x0 = i * bar_width
        y0 = canvas_height - height
        x1 = (i + 1) * bar_width
        y1 = canvas_height
        color = "blue" if not highlight or i not in highlight else "red"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=f"rect{i}")

    canvas.update_idletasks()


# Sorting Function
def start_sort():
    global data
    selected_algorithm = algo_choice.get()
    if selected_algorithm == "Bubble Sort":
        bubble_sort(data, lambda arr: draw_array(arr, canvas, canvas_height), speed_scale.get())
    elif selected_algorithm == "Insertion Sort":
        insertion_sort(data, lambda arr: draw_array(arr, canvas, canvas_height), speed_scale.get())
    elif selected_algorithm == "Merge Sort":
        merge_sort(data, lambda arr: draw_array(arr, canvas, canvas_height), speed_scale.get())
    elif selected_algorithm == "Bucket Sort":
        bucket_sort(data, lambda arr: draw_array(arr, canvas, canvas_height), speed_scale.get())


def generate_data():
    global data
    data = [random.randint(10, canvas_height) for _ in range(100)]
    draw_array(data, canvas, canvas_height)


root = tk.Tk()
root.title("Sorting Visualizer")
root.geometry("800x600")

canvas_height = 400
canvas = tk.Canvas(root, height=canvas_height, bg="white")
canvas.pack(fill="both", expand="True")

algo_choice = tk.StringVar()
algo_menu = ttk.Combobox(root, textvariable=algo_choice, values=["Bubble Sort", "Insertion Sort", "Bucket Sort", "Merge Sort"], state="readonly")
algo_menu.pack(pady=10)
algo_menu.current(0)

speed_scale = tk.Scale(root, from_=0.01, to=1.0, resolution=0.01, length=200, orient='horizontal', label="Select Speed In Seconds (Smaller is Faster)")
speed_scale.set(0.1)
speed_scale.pack(pady=10)

start_button = tk.Button(root, text="Start Sorting", command=start_sort)
start_button.pack(pady=10)

generate_button = tk.Button(root, text="Generate New Data", command=generate_data)
generate_button.pack(pady=10)

generate_data()

root.mainloop()
