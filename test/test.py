# SPDX-License-Identifier: Apache-2.0
#
# Tests for the TT06 "Inverters" design (tt_um_wokwi_395134712676183041).
#
#   ui_in[0]     --> D flip-flop --> uo_out[0]   (copied on each rising edge of clk)
#   ui_in[1..7]  --> inverters   --> uo_out[1..7]
#   uio[0,2,4,6] --> inverters   --> uio[1,3,5,7]
#   ui_in[7] = 1 turns on the outputs uio[1,3,5,7]
#   ui_in[6] = 1 would drive uio[0,2,4,6] low, so the tests keep it at 0 while they use those pins

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


async def apply(dut, ui_in, uio_in=0):
    """Set the inputs, wait two clock edges for the flip-flop, then let the outputs settle.

    Two edges, not one, so the gate-level netlist (which has gate delays) also captures the new input.
    """
    dut.ui_in.value = ui_in
    dut.uio_in.value = uio_in
    await ClockCycles(dut.clk, 2)
    await Timer(1, units="us")


@cocotb.test()
async def test_inverters(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())
    dut.ena.value = 1
    dut.rst_n.value = 1

    # All inputs low: every inverter output is high, and the flip-flop holds 0.
    await apply(dut, 0b0000_0000)
    assert dut.uo_out.value == 0b1111_1110

    # All inputs high: every inverter output is low, and the flip-flop holds 1.
    await apply(dut, 0b1111_1111)
    assert dut.uo_out.value == 0b0000_0001

    # One input high at a time: only that output goes low.
    for bit in range(1, 8):
        await apply(dut, 1 << bit)
        expected = 0b1111_1110 & ~(1 << bit)
        assert dut.uo_out.value == expected, f"ui_in[{bit}] did not invert"


@cocotb.test()
async def test_bidirectional_inverters(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())
    dut.ena.value = 1
    dut.rst_n.value = 1

    # ui_in[7] = 1 makes uio[1,3,5,7] outputs; ui_in[6] = 0 keeps uio[0,2,4,6] as inputs.
    await apply(dut, 0b1000_0000, uio_in=0b0000_0000)
    assert dut.uio_oe.value == 0b1010_1010

    # Inputs uio[0,2,4,6] low: outputs uio[1,3,5,7] high.
    assert dut.uio_out.value & 0b1010_1010 == 0b1010_1010

    # Inputs uio[0,2,4,6] high: outputs uio[1,3,5,7] low.
    await apply(dut, 0b1000_0000, uio_in=0b0101_0101)
    assert dut.uio_out.value & 0b1010_1010 == 0b0000_0000
