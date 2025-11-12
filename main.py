import tkinter as tk
from tkinter import ttk, colorchooser
import random
from typing import Generator, Iterable, Tuple, List

# ----------------------------
# Sorting Visualizer (Tkinter)
# ----------------------------
# This app lets you watch different sorting algorithms work in real-time.
# You can change array size, speed, algorithm type, and even customize colors.
# It uses Tkinter for the GUI and draws the array as vertical bars.

class SortingVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sorting Visualizer")
        self.root.geometry("900x650")


        self.canvas_height = 420
        self.data: List[int] = []      # the numbers we’re sorting
        self.rects: List[int] = []     # rectangle handles on the canvas
        self.default_bar_color = "#3B82F6"  # default = blue
        self.highlight_color = "#EF4444"    # default = red
        self.sort_gen: Generator | None = None
        self.animating = False  # prevents starting two sorts at once

        # --- Canvas to draw bars ---
        self.canvas = tk.Canvas(self.root, height=self.canvas_height, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        # When window is resized, redraw bars to fit
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # --- Controls row ---
        controls = tk.Frame(self.root)
        controls.pack(fill="x", padx=10, pady=10)

        # Algorithm dropdown
        tk.Label(controls, text="Algorithm:").grid(row=0, column=0, sticky="w")
        self.algo_choice = tk.StringVar(value="Bubble Sort")
        self.algo_menu = ttk.Combobox(
            controls, textvariable=self.algo_choice,
            values=["Bubble Sort", "Insertion Sort", "Merge Sort", "Bucket Sort"],
            state="readonly", width=16,
        )
        self.algo_menu.grid(row=0, column=1, padx=(6, 16), sticky="w")

        # Speed slider (smaller = faster)
        tk.Label(controls, text="Step delay (seconds):").grid(row=0, column=2, sticky="w")
        self.speed_scale = tk.Scale(controls, from_=0.0, to=0.5, resolution=0.01, orient="horizontal", length=180)
        self.speed_scale.set(0.05)
        self.speed_scale.grid(row=0, column=3, padx=(6, 16), sticky="w")

        # Bar amount spinner
        tk.Label(controls, text="Array size:").grid(row=0, column=4, sticky="w")
        self.size_var = tk.IntVar(value=100)
        self.size_spin = tk.Spinbox(controls, from_=10, to=400, increment=5, textvariable=self.size_var, width=6)
        self.size_spin.grid(row=0, column=5, padx=(6, 16), sticky="w")

        # Other buttons
        self.start_btn = ttk.Button(controls, text="Start Sorting", command=self.start_sort)
        self.start_btn.grid(row=0, column=6, padx=(0, 8))
        self.new_btn = ttk.Button(controls, text="Generate New Data", command=self.generate_data)
        self.new_btn.grid(row=0, column=7, padx=(0, 8))
        self.quit_btn = ttk.Button(controls, text="Quit", command=self.root.destroy)
        self.quit_btn.grid(row=0, column=8)

        # --- Color pickers row ---
        colors = tk.Frame(self.root)
        colors.pack(fill="x", padx=10, pady=(0,10))

        self.bar_color_btn = ttk.Button(colors, text="Bar Color", command=self.choose_bar_color)
        self.bar_color_btn.pack(side="left")
        self.highlight_color_btn = ttk.Button(colors, text="Highlight Color", command=self.choose_highlight_color)
        self.highlight_color_btn.pack(side="left", padx=8)

        # Create the first dataset to show
        self.generate_data()

    # ---------------------------
    # Data + Drawing
    # ---------------------------

    def generate_data(self):
        """Make a brand new random array of the chosen size and draw it."""
        size = int(self.size_var.get())
        size = max(10, min(size, 400))  # clamp array size
        # Values go from 10 up to canvas height
        self.data = [random.randint(10, self.canvas_height - 4) for _ in range(size)]
        self._build_rects()
        self._draw_all()

    def _build_rects(self):
        """(Re)create the bar rectangles to match the array size."""
        self.canvas.delete("all")
        self.rects = []
        bar_w = self._bar_width()
        for i, h in enumerate(self.data):
            x0 = int(i * bar_w)
            y0 = self.canvas_height - int(h)
            x1 = int((i + 1) * bar_w)
            y1 = self.canvas_height
            r = self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.default_bar_color, width=0)
            self.rects.append(r)

    def _bar_width(self) -> float:
        """Compute how wide each bar should be to fill the canvas."""
        cw = max(self.canvas.winfo_width(), 1)
        return cw / max(len(self.data), 1)

    def _on_canvas_resize(self, _event):
        """When you resize the window, adjust bar widths/positions."""
        self._redraw_positions_only()

    def _redraw_positions_only(self):
        """Move bars to their new positions (on resize)."""
        bar_w = self._bar_width()
        for i, h in enumerate(self.data):
            x0 = int(i * bar_w)
            y0 = self.canvas_height - int(h)
            x1 = int((i + 1) * bar_w)
            y1 = self.canvas_height
            self.canvas.coords(self.rects[i], x0, y0, x1, y1)

    def _draw_all(self):
        """Full refresh: redraw all bars with base color."""
        bar_w = self._bar_width()
        for i, h in enumerate(self.data):
            x0 = int(i * bar_w)
            y0 = self.canvas_height - int(h)
            x1 = int((i + 1) * bar_w)
            y1 = self.canvas_height
            self.canvas.coords(self.rects[i], x0, y0, x1, y1)
            self.canvas.itemconfig(self.rects[i], fill=self.default_bar_color)

    def _update_indices(self, idxs: Iterable[int], highlight: bool = True):
        """Update only the bars at the given indices."""
        bar_w = self._bar_width()
        for i in idxs:
            if 0 <= i < len(self.data):
                h = self.data[i]
                x0 = int(i * bar_w)
                y0 = self.canvas_height - int(h)
                x1 = int((i + 1) * bar_w)
                y1 = self.canvas_height
                self.canvas.coords(self.rects[i], x0, y0, x1, y1)
                self.canvas.itemconfig(
                    self.rects[i],
                    fill=(self.highlight_color if highlight else self.default_bar_color),
                )

    def _clear_highlights(self, idxs: Iterable[int]):
        """Reset highlighted bars back to the default color."""
        for i in idxs:
            if 0 <= i < len(self.data):
                self.canvas.itemconfig(self.rects[i], fill=self.default_bar_color)

    # ---------------------------
    # Color pickers
    # ---------------------------

    def choose_bar_color(self):
        """Let the user pick a new color for the bars."""
        color = colorchooser.askcolor(color=self.default_bar_color, title="Choose bar color")[1]
        if color:
            self.default_bar_color = color
            self._draw_all()

    def choose_highlight_color(self):
        """Let the user pick a new highlight color."""
        color = colorchooser.askcolor(color=self.highlight_color, title="Choose highlight color")[1]
        if color:
            self.highlight_color = color

    # ---------------------------
    # Sorting control
    # ---------------------------

    def start_sort(self):
        # Start the sorting animation using the chosen algorithm
        if self.animating:
            return  # already running
        algo = self.algo_choice.get()
        if algo == "Bubble Sort":
            self.sort_gen = self._bubble_sort()
        elif algo == "Insertion Sort":
            self.sort_gen = self._insertion_sort()
        elif algo == "Merge Sort":
            self.sort_gen = self._merge_sort()
        elif algo == "Bucket Sort":
            self.sort_gen = self._bucket_sort()
        else:
            return

        self.animating = True
        self._step_animation()

    def _step_animation(self):
        # Advance one 'frame' of the sorting animation.
        if not self.sort_gen:
            self.animating = False
            return

        try:
            to_update, to_unhi = next(self.sort_gen)
            if to_unhi:
                self._clear_highlights(to_unhi)
            if to_update:
                self._update_indices(to_update, highlight=True)
        except StopIteration:
            # Finished: reset all bars to base color
            self._draw_all()
            self.animating = False
            self.sort_gen = None
            return

        delay_ms = max(0, int(self.speed_scale.get() * 1000))
        self.root.after(delay_ms, self._step_animation)

    # ---------------------------
    # Sorting algorithms
    # ---------------------------
    # Each one is a generator: it yields whenever a bar changes,
    # so the animation can update the screen in small steps.

    def _bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    swapped = True
                    yield ((j, j+1), ())   # highlight these bars
                    yield ((), (j, j+1))   # un-highlight them
            if not swapped:
                break
        yield ((), range(n))  # final cleanup

    def _insertion_sort(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and self.data[j] > key:
                self.data[j + 1] = self.data[j]
                yield ((j+1,), ())
                yield ((), (j+1,))
                j -= 1
            self.data[j + 1] = key
            yield ((j+1,), ())
            yield ((), (j+1,))
        yield ((), range(len(self.data)))

    def _merge_sort(self):
        def merge(l, m, r):
            temp = self.data[l:r+1]
            i, j, k = 0, m - l + 1, l
            while i <= m - l and j <= r - l:
                if temp[i] <= temp[j]:
                    self.data[k] = temp[i]; i += 1
                else:
                    self.data[k] = temp[j]; j += 1
                yield ((k,), ()); yield ((), (k,))
                k += 1
            while i <= m - l:
                self.data[k] = temp[i]; i += 1
                yield ((k,), ()); yield ((), (k,))
                k += 1
            while j <= r - l:
                self.data[k] = temp[j]; j += 1
                yield ((k,), ()); yield ((), (k,))
                k += 1

        def sort(l, r):
            if l >= r: return
            m = (l + r) // 2
            yield from sort(l, m)
            yield from sort(m+1, r)
            yield from merge(l, m, r)

        yield from sort(0, len(self.data)-1)
        yield ((), range(len(self.data)))

    def _bucket_sort(self):
        if not self.data: return
        n = len(self.data)
        bucket_count = max(1, n // 3)
        max_val = max(self.data)
        buckets = [[] for _ in range(bucket_count)]

        # Put each element in a bucket
        for idx, num in enumerate(self.data):
            bi = int(bucket_count * num / (max_val+1))
            bi = min(max(bi, 0), bucket_count-1)
            buckets[bi].append(num)
            yield ((idx,), ()); yield ((), (idx,))

        # Sort each bucket and merge
        for b in buckets: b.sort()
        k = 0
        for b in buckets:
            for val in b:
                self.data[k] = val
                yield ((k,), ()); yield ((), (k,))
                k += 1
        yield ((), range(n))


if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
