## LM567 Audio Filter Decoder
[CW Modem](https://www.kk5jy.net/cw-modem-v1/)

Modify this for 3V output

Here is your summary in short point form sentences:

* **R1 (Trimmer Resistor) sets center frequency** of the LM567 VCO.

  * 9kΩ → \~1kHz center frequency.
  * 13kΩ → \~700Hz.
  * 20kΩ → <400Hz.
  * Series combo (e.g. 10kΩ fixed + 10kΩ trimmer) limits tuning range (e.g. 450–950Hz).
  * Tuning speed depends on ratio of fixed/trimmer resistor.

* **C2 (1μF) controls detection bandwidth**.

  * \~10–15% bandwidth from 400Hz–1000Hz.
  * \~70–100Hz actual BW — good selectivity.
  * Use smaller C2 for wider bandwidth; larger for narrower.

* **C3 (Output filter capacitor) affects speed response**.

  * 2.2μF is good up to \~30 WPM.
  * Use 1.0μF for \~50 WPM.
  * C3 should be ≥ 2× C2 (datasheet recommendation).
  * Matching C3 and C2 balances PLL and output responsiveness.

* **Max switching speed = f0 / 20 (from datasheet)**.

  * 400Hz → \~24 WPM max.
  * 600Hz → \~36 WPM.
  * 800Hz → \~48 WPM.
  * 700Hz (\~42 WPM) is a good practical choice.

* **VCO stability issues and solutions**:

  * Use high-quality trimmer (cheap ones drift or are touch-sensitive). TEN-TURN 10K in series with 5K6
  * Use 4.7μF capacitor between pin 4 and pin 7 to stabilize supply voltage and reduce jitter.
  * Arduino 5V line can be noisy; local decoupling helps.

```circuit

     5V Input
        │
        │
     [ 220Ω ]
        │
        +-----------o 3.3V Output <------ [10KΩ ]...............o Pin 8 (LM567)
        │                                          |
     [ Zener Diode ]                               |
        │    (Vz = 3.3V, e.g., 1N4728A)            -------------o Data output  (3.3V TTL) Pi Pico (GP2 pin 4)
        │
       GND
```

```circuit

       Radio Speaker Output (≈3W @ 4Ω)
                     │
                     ├────────────────────────────O Ext Speaker
                     │
                  [100µF]
                     │
                  [1kΩ]
                     │
                     ├─────────────┬────────────── LM567 Pin 3 (SIGIN)
                     │             │
                  ┌──┴──┐       ┌──┴──┐
     Forward      │     │       │     │
     biased       │  →| │       │  |← │Reversed
                  │ D1  │       │ D2  │biased
                  │1N4148       │1N4148
                  └─────┘       └─────┘
                     │             │
                    GND           GND

```


