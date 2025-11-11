"""
Tkinter GUI application that demonstrates bubble sort interactively.
"""

from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import Iterable, List, Optional

from algorithms import BubbleSortState, bubble_sort_steps

# Configuration constants
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 360
PADDING = 20
BAR_COLOR = "#4f6df5"
BAR_COLOR_ACTIVE = "#ff6b6b"
BAR_COLOR_SWAP = "#ffa94d"
BACKGROUND_COLOR = "#0b132b"

DEFAULT_LIST_SIZE = 16
MIN_VALUE = 1
MAX_VALUE = 50


class SortingApp:
    """Encapsulates the GUI and sorting interaction."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Bubble Sort Visualizer")
        self.root.configure(bg=BACKGROUND_COLOR)

        self.data: List[int] = []
        self.state_generator = iter(())
        self.current_state: Optional[BubbleSortState] = None
        self.after_id: Optional[str] = None

        self._build_widgets()
        self.generate_new_data()

    def _build_widgets(self) -> None:
        """Create and place UI widgets."""
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="List size:").grid(row=0, column=0, padx=5)
        self.size_var = tk.IntVar(value=DEFAULT_LIST_SIZE)
        self.size_spinbox = ttk.Spinbox(
            control_frame, from_=5, to=32, textvariable=self.size_var, width=5
        )
        self.size_spinbox.grid(row=0, column=1, padx=5)

        ttk.Button(
            control_frame, text="Generate", command=self.generate_new_data
        ).grid(row=0, column=2, padx=5)

        ttk.Button(control_frame, text="Step", command=self.next_step).grid(
            row=0, column=3, padx=5
        )

        self.playing = tk.BooleanVar(value=False)
        self.play_button = ttk.Button(
            control_frame, text="Play", command=self.toggle_play
        )
        self.play_button.grid(row=0, column=4, padx=5)

        ttk.Label(control_frame, text="Speed (ms):").grid(row=0, column=5, padx=5)
        self.speed_var = tk.IntVar(value=400)
        self.speed_scale = ttk.Scale(
            control_frame, from_=50, to=2000, orient=tk.HORIZONTAL, variable=self.speed_var
        )
        self.speed_scale.grid(row=0, column=6, padx=5, sticky=tk.EW)
        control_frame.columnconfigure(6, weight=1)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            self.root, textvariable=self.status_var, padding=(10, 5), foreground="white", background=BACKGROUND_COLOR
        )
        status_label.pack(side=tk.BOTTOM, anchor=tk.W)

        self.canvas = tk.Canvas(
            self.root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def generate_new_data(self) -> None:
        """Create a fresh dataset and reset the state."""
        size = self.size_var.get()
        self.data = [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(size)]
        self.state_generator = bubble_sort_steps(self.data)
        self.current_state = None
        self.status_var.set("Random data generated. Press Play or Step to watch sorting.")
        self._cancel_animation()
        self.playing.set(False)
        self.play_button.config(text="Play")
        self._draw_data(self.data)

    def _draw_data(self, data: Iterable[int], active_indices: Iterable[int] = ()) -> None:
        """Render the data as vertical bars on the canvas."""
        self.canvas.delete("all")
        values = list(data)
        if not values:
            return

        max_value = max(values)
        bar_width = (CANVAS_WIDTH - 2 * PADDING) / len(values)
        for idx, value in enumerate(values):
            x0 = PADDING + idx * bar_width
            x1 = x0 + bar_width * 0.9
            height_ratio = value / max_value if max_value else 0
            bar_height = height_ratio * (CANVAS_HEIGHT - 2 * PADDING)
            y0 = CANVAS_HEIGHT - PADDING
            y1 = y0 - bar_height

            color = BAR_COLOR
            if idx in active_indices:
                color = BAR_COLOR_SWAP if idx == max(active_indices) else BAR_COLOR_ACTIVE

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            self.canvas.create_text(
                (x0 + x1) / 2,
                y0 + 12,
                text=str(value),
                fill="white",
                font=("TkDefaultFont", 10, "bold"),
            )

    def next_step(self) -> None:
        """Advance the sorting algorithm by one comparison."""
        try:
            state = next(self.state_generator)
        except StopIteration as exc:
            self._handle_sort_completed(getattr(exc, "value", None))
            return

        self.current_state = state
        highlight = {state.index_a, state.index_b}
        self._draw_data(state.data, highlight)
        status = (
            f"Pass {state.pass_index + 1}, comparing indices {state.index_a} and {state.index_b}."
        )
        if state.swapped:
            status += " Swapped!"
        self.status_var.set(status)

    def toggle_play(self) -> None:
        """Start or pause automatic playback."""
        if self.playing.get():
            self.playing.set(False)
            self.play_button.config(text="Play")
            self._cancel_animation()
        else:
            self.playing.set(True)
            self.play_button.config(text="Pause")
            self._schedule_next_step()

    def _schedule_next_step(self) -> None:
        if not self.playing.get():
            return
        self.next_step()
        speed = max(50, int(self.speed_var.get()))
        self.after_id = self.root.after(speed, self._schedule_next_step)

    def _cancel_animation(self) -> None:
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def _handle_sort_completed(self, sorted_values: Optional[List[int]]) -> None:
        """Update UI when sorting finishes."""
        self._cancel_animation()
        self.playing.set(False)
        self.play_button.config(text="Play")
        if sorted_values is not None:
            self._draw_data(sorted_values)
            self.data = sorted_values
        self.status_var.set("Sorting complete!")


def main() -> None:
    """Entry point for running the GUI."""
    root = tk.Tk()
    SortingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()



