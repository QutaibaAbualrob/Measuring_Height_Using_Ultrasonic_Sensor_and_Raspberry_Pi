# height_lcd.py
from time import sleep
import board
from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

# LCD wiring 
LCD_COLUMNS = 16
LCD_ROWS = 2

# Default pins used
_LCD_RS_PIN = board.D26
_LCD_EN_PIN = board.D19
_LCD_D4_PIN = board.D13
_LCD_D5_PIN = board.D6
_LCD_D6_PIN = board.D5
_LCD_D7_PIN = board.D11

# module-level lcd object
_lcd = None

def _center(text, width=LCD_COLUMNS):
    t = str(text)[:width]
    pad = max(0, width - len(t))
    left = pad // 2
    return " " * left + t + " " * (width - left - len(t))

def init_lcd(rs_pin=_LCD_RS_PIN,
             en_pin=_LCD_EN_PIN,
             d4_pin=_LCD_D4_PIN,
             d5_pin=_LCD_D5_PIN,
             d6_pin=_LCD_D6_PIN,
             d7_pin=_LCD_D7_PIN,
             columns=LCD_COLUMNS,
             rows=LCD_ROWS):
    """
    Initialize the LCD hardware. Must be called before any show_* functions.
    Safe to call multiple times.
    """
    global _lcd
    if _lcd is not None:
        return _lcd

    lcd_rs = DigitalInOut(rs_pin)
    lcd_en = DigitalInOut(en_pin)
    lcd_d4 = DigitalInOut(d4_pin)
    lcd_d5 = DigitalInOut(d5_pin)
    lcd_d6 = DigitalInOut(d6_pin)
    lcd_d7 = DigitalInOut(d7_pin)

    _lcd = Character_LCD_Mono(
        lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, columns, rows
    )
    _lcd.clear()
    return _lcd

def show_message(line1, line2=""):
    """
    Display two centered lines on the LCD.
    Call init_lcd() first.
    """
    if _lcd is None:
        raise RuntimeError("LCD not initialized. Call init_lcd() first.")
    _lcd.message = _center(line1)[:LCD_COLUMNS] + "\n" + _center(line2)[:LCD_COLUMNS]

def show_height(height_cm, greeting="Hello!"):
    """
    Display height on line1 and greeting (or message) on line2.
    """
    top = f"Height: {height_cm:.2f}cm"
    show_message(top, greeting)

def show_small_measure(line1, line2):
    """
    Quick helper to show two short lines without centering logic outside.
    """
    if _lcd is None:
        raise RuntimeError("LCD not initialized. Call init_lcd() first.")
    _lcd.message = str(line1)[:LCD_COLUMNS] + "\n" + str(line2)[:LCD_COLUMNS]

def clear():
    if _lcd is None:
        return
    _lcd.clear()

def goodbye(msg1="Goodbye!", msg2="See you"):
    if _lcd is None:
        return
    _lcd.clear()
    _lcd.message = _center(msg1)[:LCD_COLUMNS] + "\n" + _center(msg2)[:LCD_COLUMNS]
    sleep(0.9)
    _lcd.clear()

def shutdown():
    """Clear LCD and release resources. Call at program exit."""
    try:
        goodbye()
    except Exception:
        pass
