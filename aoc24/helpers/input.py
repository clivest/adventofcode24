from pathlib import Path


def input_file(day: int) -> Path:
    return Path(__file__).parent.parent.parent / "inputs" / f"i{day}.txt"
