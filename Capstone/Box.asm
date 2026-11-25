// Box.asm — Draw a 16x20 black box at row 72 (K = 72) while any key is pressed
// Student: Aman Kumar | Roll No: 2501730172 | K = 72
// Starting row = K = 72 -> offset = 32 * 72 = 2304 -> SCREEN + 2304 = 18688
// Height = 20 rows (rows 72..91)
// Width = 16 * ((72 mod 4) + 1) = 16 pixels (1 word per row, left edge)

(LOOP)
    @KBD
    D=M             // D = keyboard code (0 if no key pressed)
    @ERASE
    D;JEQ           // If D == 0, erase box

    @color
    M=-1            // Key pressed: color = -1 (black)
    @DRAW
    0;JMP

(ERASE)
    @color
    M=0             // No key pressed: color = 0 (white)

(DRAW)
    @SCREEN
    D=A
    @2304           // 32 * 72 = 2304
    D=D+A
    @addr
    M=D             // addr = SCREEN + 2304 (row 72, left edge)

    @20
    D=A
    @count
    M=D             // count = 20 rows

(ROW_LOOP)
    @count
    D=M
    @LOOP
    D;JEQ           // If count == 0, return to keyboard check

    @color
    D=M
    @addr
    A=M
    M=D             // Write color (-1 or 0) to current screen word

    @32
    D=A
    @addr
    M=D+M           // addr += 32 (next screen row)

    @count
    M=M-1           // count--

    @ROW_LOOP
    0;JMP
