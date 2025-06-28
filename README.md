# ZS6BVR Morse Sender – Raspberry Pi Pico`



This project uses a **Raspberry Pi Pico** running **MicroPython** to send Morse code by controlling a relay through GPIO pin **GP1**. The relay can be used to key a ham radio transmitter for CW (Morse) transmission.

---

## 1. What You'll Need

- Raspberry Pi Pico (not Pico W unless you adapt for it)
- 5v Reed Relay (not solid-state relay)
- NPN transistor (e.g., 2N2222 or 2N3904 or BC547)
- 1kΩ resistor (base resistor)
- Two Diodes for flyback protection (e.g., 1N4148 or 1N4007)
- 7805 5V regulator
- USB cable (micro USB)
- Thonny IDE software (for uploading/running MicroPython code)

---

## 2. Wiring Diagram

```
 We recomend you place a diode accross the IN and OUT pins of regulator
       
              Cathode   ─────────|<────────────    Anode
                        |                     |
  +7V to +12V DC Input  |  IN ┌───────┐ OUT   |
  ----------o─────────────────│ 7805  │────────────o------------- +5V Regulated
                  |           └───────┘        |
                  | +            │             |+
                 [C1]            │            [C2]
                  | -           GND            |-
                 50uF                         10µF
                  │                            |
                 GND                          GND
                               
                                                     / Toggle switch calibrate/transmit
                      +5V Regulated o───────────┬───o  o───┐
                                                │          │
                                                │          ▼ One side of relay 
                              Raspberry Pi Pico |            and Flyback Diode Cathode
                                                │
                                                |              (Top View)
                                                │
                                                │        ┌─────────────────────┐
     Flyback Diode                              │        │                     │
    (e.g., 1N4148)                              └────────▶ VSYS (Pin 39)       │
    Cathode ──|<── Anode                                 │                     │
                                                         │                     │
     Ocsilloscope Calibrate output   o────────┐          │                     │
                                              |          │                     │
     Flyback Diode Anode              ▶───────┐          │                     │
                                              |          │                     │
     Other side of relay              ▶───────┐          │                     │
                                              |          │                     │
                                 Collector    |          │                     │
                                             ┌▼┐         │                     │
                                NPN Transistor│          │                     │
                                             └┬┘         │                     │
                                              GND        │                     | 
                                                         │                     │
                           Base ── 1kΩ ──────────────────▶ GP1 (Pin 2)         │
                                                         │                     │
                           Emitter ──────── GND ─────────▶ GND (Pin 38)        │
                                                         └─────────────────────┘

Please place a fuse at the input and output of the regulator 0.5A Slow-blow fuses

```

---
## 3. Install needed software
### Step 1: Install MicroPython on the Pico

1. Visit: https://www.raspberrypi.com/documentation/microcontrollers/micropython.html  
   (Or go directly to https://micropython.org/download/rp2-pico/)
2. Press and hold the **BOOTSEL** button on the Pico, then plug it into your PC via USB.
3. A drive called `RPI-RP2` will appear.
4. Download the **MicroPython UF2 file** for the Pico from the site above.
5. Drag and drop the `.uf2` file onto the `RPI-RP2` drive.
6. The Pico will reboot and is now running MicroPython.

---

### Step 2: Install Thonny IDE

### 2.1 On Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install thonny
```

### 2.2 On macOS

* Download from [https://thonny.org](https://thonny.org) and install the `.dmg` file.

### O2.3 n Windows

* Download from [https://thonny.org](https://thonny.org) and run the installer `.exe`.

---

### Step 3: Set Up Thonny for the Pico

1. Open **Thonny**.
2. Go to **Tools > Options > Interpreter**.
3. Set:

   * **Interpreter**: MicroPython (Raspberry Pi Pico)
   * **Port**: Auto or select the port manually (e.g., COM3 on Windows, `/dev/ttyACM0` on Linux)

---

## Step 4: Install the Morse Sender Program

1. Save the MicroPython script as: `zs6bvr-morse-sender.py`
2. In Thonny, click **File > Open...** and load your `zs6bvr-morse-sender.py`
3. Click **Run (▶)** or press `F5` to run the script.
4. In the Thonny shell at the bottom, interact with the program.

---

##  4. Running the Program

After running, you will see:

```
ZS6BVR Morse Sender (Raspberry Pi Pico)
Type message and press ENTER
Special keys: * = quit, + = faster, - = slower, @ = dots mode
```

### 4.1 Commands:

* Type any message (e.g., `CQ CQ DE ZS6BVR`) and press Enter to transmit.
* `+` / `++`: Increase WPM
* `-` / `--`: Decrease WPM
* `@`: Dot mode (sends a stream of dots)
* `*`: Exit program

---

## 5. Customization

* Change the GPIO pin from GP1 by editing this line:

  ```python
  relay_pin = Pin(1, Pin.OUT)
  ```
* Adjust default WPM (words per minute) here:

  ```python
  wpm = 12
  ```

---

## 6. Notes

* Ensure your relay or transistor circuit is properly protected with a **flyback diode**.
* If you're using an external transmitter, key only the **PTT** line, not RF.
* For safety, test using an LED instead of a relay.

---

## 7. Credits

Created by ZS6BVR (Nico Michael) – Morse sender for Raspberry Pi Pico using MicroPython.

---

