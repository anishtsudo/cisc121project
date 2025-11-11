# Bubble Sort Visualizer

An interactive Tkinter application that demonstrates the bubble sort algorithm step by step.  
The project highlights algorithm design, GUI programming, testing, and documentation working together in a single, self-contained example.

## Features

- Generate a random list of integers with customizable length.
- Visualize bubble sort comparisons and swaps in real time.
- Step through the algorithm manually or press *Play* to animate automatically.
- Adjust the playback speed without restarting the sort.

## Getting Started

### Prerequisites

- Python 3.10 or later (Tkinter ships with the standard Python installer on macOS and Windows).
- Optional: a virtual environment for isolating dependencies.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the App

```bash
python app.py
```

The window opens with a randomly generated list. Use the *Generate*, *Step*, and *Play/Pause* controls to explore the algorithm.

## Testing

Run the automated tests to confirm the algorithm implementation:

```bash
pytest
```

## Project Structure

- `app.py` — Tkinter GUI entry point.
- `algorithms.py` — Bubble sort implementation that yields intermediate states.
- `tests/test_algorithms.py` — Unit tests validating the algorithm logic.

## Extending the Demo

Ideas for future improvements:

- Add more algorithms (e.g., insertion sort, merge sort, binary search).
- Display metrics such as comparisons and swaps over time.
- Allow custom user input for the dataset.
- Export the sequence of steps for educational worksheets or walkthroughs.



