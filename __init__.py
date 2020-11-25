"""
From:
https://www.pololu.com/product/2547
 The WS2812B seems to be more sensitive than the TM1804 on our original LED strips. We recommend taking several precautions to protect it:

    Connect a capacitor of at least 100 μF between the ground and power lines on the power input.
    Avoiding making or changing connections while the circuit is powered.
    Minimize the length of the wires connecting your microcontroller to the LED strip.
    Follow generally good engineering practices, such as taking precautions against electrostatic discharge (ESD).
    Consider adding a 100 Ω to 500 Ω resistor between your microcontroller’s data output and the LED strip to reduce the noise on that line.

If the strip does get damaged, it is often just the first LED that is broken; in such cases, cutting off this first segment and resoldering the connector to the second segment brings the strip back to life.
However, it is unnecessary for WS2113 indeed.
"""
