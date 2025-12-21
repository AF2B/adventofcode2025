from typing import NewType, List
from dataclasses import dataclass
from pathlib import Path

LetterNumber = NewType("LetterNumber", str)
NumericValue = NewType("NumericValue", int)
NormalizedData = NewType("NormalizedData", List[str])
LineFeed = NewType("LineFeed", str)
CarriageReturn = NewType("CarriageReturn", str)

@dataclass(frozen=True)
class RawInput:
    content: str

@dataclass(frozen=True)
class InputFilePath:
    value: Path

@dataclass(frozen=True)
class ContentRules:
    LineFeed: LineFeed
    CarriageReturn: CarriageReturn

def normalizeData(content: RawInput) -> NormalizedData:
    lines: List[str] = content.content.splitlines()
    return NormalizedData(lines)

def readInputFile(path: InputFilePath) -> RawInput:
    if not path.value.exists():
        raise FileNotFoundError(f"File not found: {path.value}")
    
    content: str = path.value.read_text(encoding="utf-8")
    return RawInput(
        content=content
    )

def separateLetterFromValue(letterNumber: LetterNumber) -> NumericValue:
    raw: str = letterNumber

    if len(raw) < 2:
        raise ValueError("Input must contain one letter followed by numbers.")

    letter_part: str = raw[0]
    numeric_part: str = raw[1:]

    if not letter_part.isalpha():
        raise ValueError("Input must start with a letter.")

    if not numeric_part.isdigit():
        raise ValueError("Input must contain only digits after the letter.")

    return NumericValue(int(numeric_part))

def rollet(start_point: int, inputs: NormalizedData) -> int:
    LIMIT_UP: int = 99
    LIMIT_DOWN: int = 0
    SIZE: int = LIMIT_UP - LIMIT_DOWN + 1

    actual_position: int = start_point
    pwd: int = 0

    for instruction in inputs:
        direction: str = instruction[0]
        steps: int = separateLetterFromValue(LetterNumber(instruction))

        if direction == "R":
            delta = steps
        elif direction == "L":
            delta = -steps
        else:
            raise ValueError(f"Invalid instruction: {instruction}")

        new_position: int = (actual_position + delta) % SIZE

        if new_position == 0:
            pwd += 1

        actual_position = new_position

    return pwd

def main() -> None:
    raw_data: RawInput = readInputFile(InputFilePath(Path("./input.txt")))
    normalizedData: NormalizedData = normalizeData(raw_data)
    result = rollet(50, normalizedData)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
