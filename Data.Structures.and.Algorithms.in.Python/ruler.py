"""
---- 0          ----- 0             --- 0
-               -                   -
--              --                  --
-               -                   -
---             ---                 --- 1
-               -                   -
--              --                  --
-               -                   -
---- 1          ----                --- 2
-               -                   -
--              --                  --
-               -                   -
---             ---                 --- 3
-               -
--              --
-               -
---- 2          ----- 1
(a)             (b)                 (c)

Three sample outputs of an English ruler drawing:
(a) a 2-inch ruler with major tick length 4;
(b) a 1-inch ruler with major tick length 5;
(c) a 3-inch ruler with major tick length 3.
"""
def draw_line(tick_length, tick_label=''):
    """Draw one line with given tick length (followed by optional label)."""
    line = "-" * tick_length
    if tick_label:
        line += " " + tick_label
    print(line)

def draw_interval(center_length):
    """Draw tick interval based upon a central tick length."""
    if center_length > 0:
        draw_interval(center_length - 1)
        draw_line(center_length)
        draw_interval(center_length - 1)

def draw_ruler(num_inches, major_length):
    """Draw English ruler with given number of inches, major tick length."""
    draw_line(major_length, '0')
    for j in range(1, 1 + num_inches):
        draw_interval(major_length - 1)
        draw_line(major_length, str(j))

if __name__ == "__main__":
    print ("Case (a):\n")
    draw_ruler(2, 4)
    print ("\nCase (b):\n")
    draw_ruler(1, 5)
    print ("\nCase (c):\n")
    draw_ruler(3, 3)
