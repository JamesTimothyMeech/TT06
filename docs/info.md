<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
I made this design with the goal of seeing what different measurements I could perform on an inverter with an analog Tiny Tapeout tile: https://github.com/JamesTimothyMeech/tt06-programmable-thing compared to this digital one. 
This project contains 11 inverters and one D flip-flop. In the fabricated chip every inverter is the same standard cell (`sky130_fd_sc_hd__inv_2`), so they are all the same size.

| Input | Output | Between them |
| --- | --- | --- |
| ui[0] | uo[0] | D flip-flop, copies the input on each rising edge of `clk` |
| ui[1] to ui[7] | uo[1] to uo[7] | one inverter each |
| uio[0], uio[2], uio[4], uio[6] | uio[1], uio[3], uio[5], uio[7] | one inverter each |

Two inputs also control the bidirectional pins:

- **ui[7] = 1** turns on the outputs uio[1], uio[3], uio[5] and uio[7]. Set it to 1 to see them.
- **ui[6] = 1** turns uio[0], uio[2], uio[4] and uio[6] into outputs that drive 0. Keep it at 0 while you drive those pins, so the chip does not fight your signal.

The Wokwi circuit diagram is at https://wokwi.com/projects/395134712676183041 and the pinout is in the info.yaml: https://github.com/JamesTimothyMeech/TT06/blob/main/info.yaml

## How to test

The TT06 demoboard is all you need to check the logic. Its RP2040 can drive every input and read every output, for example from the MicroPython REPL or the Tiny Tapeout Commander app.

To go further, apply inputs to the inverters with a square wave or other signal generator and measure the output. Experiment by putting inverters in parallel and see if you can measure any differences in their speed. Try connecting a large capacitor to the input and a resistor between the input and the output to use the inverters as an amplifier: https://www.youtube.com/watch?v=03Ds1TnoMbA&ab_channel=MSMTUE does this work in the same way as the inverter on the analog tile? If not, why? 

## External hardware

The TT06 demoboard on its own is enough to test the logic. A signal generator and an oscilloscope are only needed for the speed and amplifier experiments.
