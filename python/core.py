from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Tuple

from result import Result, Ok, Err

type NumericValue = int
type Direction = Literal["L", "R"]

@dataclass(frozen=True)
class Instruction:
    direction: Direction
    steps: NumericValue

@dataclass(frozen=True)
class NormalizedData:
    values: Tuple[str, ...]

@dataclass(frozen=True)
class RawInput:
    content: str

@dataclass(frozen=True)
class InputFilePath:
    value: Path

@dataclass(frozen=True)
class ParseError:
    reason: str
    raw: str

def read_input_file(path: InputFilePath) -> Result[RawInput, str]:
    if not path.value.exists():
        return Err(f"File not found: {path.value}")

    content = path.value.read_text(encoding="utf-8")
    return Ok(RawInput(content=content))

def normalize_data(raw: RawInput) -> NormalizedData:
    values = tuple(
        value.strip()
        for value in raw.content.replace("\r", "\n").split("\n")
        if value.strip()
    )
    return NormalizedData(values)

def parse_instruction(raw: str) -> Result[Instruction, ParseError]:
    if len(raw) < 2:
        return Err(ParseError("Instruction too short", raw))

    direction = raw[0]
    if direction not in ("L", "R"):
        return Err(ParseError("Invalid direction", raw))

    steps_part = raw[1:]
    if not steps_part.isdigit():
        return Err(ParseError("Invalid numeric value", raw))

    return Ok(
        Instruction(
            direction=direction,
            steps=int(steps_part)
        )
    )

def parse_instructions(
    data: NormalizedData
) -> Result[Tuple[Instruction, ...], ParseError]:

    instructions: list[Instruction] = []

    for raw in data.values:
        result = parse_instruction(raw)

        if isinstance(result, Err):
            return result

        instructions.append(result.ok_value)

    return Ok(tuple(instructions))

def rollet(start_point: int, instructions: Tuple[Instruction, ...]) -> int:
    LIMIT_UP = 99
    LIMIT_DOWN = 0
    SIZE = LIMIT_UP - LIMIT_DOWN + 1

    position = start_point
    pwd = 0

    for instruction in instructions:
        delta = (
            instruction.steps
            if instruction.direction == "R"
            else -instruction.steps
        )

        position = (position + delta) % SIZE

        if position == 0:
            pwd += 1

    return pwd

def main() -> None:
    file_path = InputFilePath(Path("./input.txt"))

    result = read_input_file(file_path)

    if isinstance(result, Err):
        print(result.value)
        return

    normalized = normalize_data(result.ok_value)
    parsed = parse_instructions(normalized)

    if isinstance(parsed, Err):
        print(f"Parse error: {parsed.value.reason} -> {parsed.value.raw}")
        return

    output = rollet(50, parsed.ok_value)
    print(f"Rollet result: {output}")

if __name__ == "__main__":
    main()
