"""
Hack Two-Pass Assembler (Nand to Tetris - Part B)
Student: Aman Kumar | Roll No: 2501730172 | K = 72
K mod 3 = 0 -> Additional Feature: Save all labels and variables with their addresses in symbols.txt
"""

from __future__ import annotations

import os
import sys

PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    **{f"R{i}": i for i in range(16)},
}

COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}

DEST_TABLE = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111",
}

JUMP_TABLE = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def clean_line(raw_line: str) -> str:
    """Remove // comments and all whitespace from a Hack assembly line."""
    no_comment = raw_line.split("//", 1)[0]
    return "".join(no_comment.split())


def first_pass(lines: list[str]) -> tuple[dict[str, int], dict[str, int], list[str]]:
    """
    First pass: strip comments/blank lines, record (LABEL) ROM addresses,
    and return (symbol_table, labels_only, cleaned_instructions).
    """
    symbol_table = dict(PREDEFINED_SYMBOLS)
    labels = {}
    instructions = []
    rom_address = 0

    for raw_line in lines:
        line = clean_line(raw_line)
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            symbol_table[label] = rom_address
            labels[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1

    return symbol_table, labels, instructions


def translate_c_instruction(line: str) -> str:
    """Translate a C-instruction ([dest=]comp[;jump]) into a 16-bit binary string."""
    dest = ""
    jump = ""
    comp_part = line

    if "=" in comp_part:
        dest, comp_part = comp_part.split("=", 1)
    if ";" in comp_part:
        comp, jump = comp_part.split(";", 1)
    else:
        comp = comp_part

    if comp not in COMP_TABLE:
        raise ValueError(f"Unknown comp mnemonic: '{comp}' in '{line}'")
    if dest not in DEST_TABLE:
        raise ValueError(f"Unknown dest mnemonic: '{dest}' in '{line}'")
    if jump not in JUMP_TABLE:
        raise ValueError(f"Unknown jump mnemonic: '{jump}' in '{line}'")

    return "111" + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]


def second_pass(
    instructions: list[str], symbol_table: dict[str, int]
) -> tuple[list[str], dict[str, int]]:
    """
    Second pass: convert instructions to 16-bit binary and allocate RAM
    addresses (starting at 16) for new variables.
    """
    machine_code = []
    variables = {}
    next_ram_address = 16

    for line in instructions:
        if line.startswith("@"):
            symbol = line[1:]
            if symbol.isdigit():
                address = int(symbol)
            elif symbol in symbol_table:
                address = symbol_table[symbol]
            else:
                address = next_ram_address
                symbol_table[symbol] = address
                variables[symbol] = address
                next_ram_address += 1
            machine_code.append(f"0{address:015b}")
        else:
            machine_code.append(translate_c_instruction(line))

    return machine_code, variables


def save_symbols_file(
    output_path: str, labels: dict[str, int], variables: dict[str, int]
) -> None:
    """Save all labels and variables with their addresses to symbols.txt (K mod 3 = 0)."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=== LABELS (ROM Addresses) ===\n")
        if labels:
            for name, addr in labels.items():
                f.write(f"{name} = {addr}\n")
        else:
            f.write("(none)\n")

        f.write("\n=== VARIABLES (RAM Addresses) ===\n")
        if variables:
            for name, addr in variables.items():
                f.write(f"{name} = {addr}\n")
        else:
            f.write("(none)\n")


def assemble_file(asm_path: str, hack_path: str | None = None) -> tuple[str, str]:
    """Assemble a .asm file into .hack and write symbols.txt in the same folder."""
    with open(asm_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    symbol_table, labels, instructions = first_pass(lines)
    machine_code, variables = second_pass(instructions, symbol_table)

    if hack_path is None:
        base, _ = os.path.splitext(asm_path)
        hack_path = f"{base}.hack"

    with open(hack_path, "w", encoding="utf-8") as f:
        f.write("\n".join(machine_code) + ("\n" if machine_code else ""))

    symbols_path = os.path.join(os.path.dirname(os.path.abspath(hack_path)), "symbols.txt")
    save_symbols_file(symbols_path, labels, variables)

    return hack_path, symbols_path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <input.asm> [output.hack]")
        sys.exit(1)

    asm_path = sys.argv[1]
    hack_path = sys.argv[2] if len(sys.argv) >= 3 else None
    out_hack, out_symbols = assemble_file(asm_path, hack_path)
    print(f"Assembled: {out_hack}")
    print(f"Symbols saved: {out_symbols}")


if __name__ == "__main__":
    main()
