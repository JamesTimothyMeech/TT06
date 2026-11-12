# Test the real TT06 "Inverters" chip on the Tiny Tapeout demoboard.
#
# 1. Turn the ui_in DIP switches OFF and unplug any PMODs.
# 2. Copy this file to the board:   mpremote cp test/chip/test_on_chip.py :
# 3. In the board's REPL, where `tt` already exists, run:
#        import test_on_chip
#        test_on_chip.run(tt)
#
# It prints PASS or FAIL for each check, then a summary.

from ttboard.mode import RPMode


def run(tt):
    failures = []

    def check(name, got, expected):
        ok = got == expected
        print("{}  {}  (got {:08b}, expected {:08b})".format("PASS" if ok else "FAIL", name,
                                                              got, expected))
        if not ok:
            failures.append(name)

    # Let the RP2040 drive the inputs, and select this design.
    # The TT06 firmware names the project "wokwi_inverters".
    tt.mode = RPMode.ASIC_RP_CONTROL
    tt.shuttle.wokwi_inverters.enable()
    tt.clock_project_stop()
    tt.uio_oe_pico.value = 0           # the RP2040 drives no uio pin yet

    # ui_in[1..7] are inverted onto uo_out[1..7]; the flip-flop copies ui_in[0] to uo_out[0].
    tt.ui_in.value = 0b0000_0000
    tt.clock_project_once()
    check("all inputs low", int(tt.uo_out.value), 0b1111_1110)

    tt.ui_in.value = 0b1111_1111
    tt.clock_project_once()
    check("all inputs high", int(tt.uo_out.value), 0b0000_0001)

    for bit in range(1, 8):
        tt.ui_in.value = 1 << bit
        tt.clock_project_once()
        check("ui_in[%d] high" % bit, int(tt.uo_out.value), 0b1111_1110 & ~(1 << bit))

    # Bidirectional inverters: ui_in[7] = 1 turns on the outputs uio[1,3,5,7].
    # ui_in[6] stays 0 so uio[0,2,4,6] are inputs, which the RP2040 then drives.
    tt.ui_in.value = 0b1000_0000
    tt.uio_oe_pico.value = 0b0101_0101

    tt.uio_in.value = 0b0000_0000
    tt.clock_project_once()
    check("uio inputs low", int(tt.uio_out.value) & 0b1010_1010, 0b1010_1010)

    tt.uio_in.value = 0b0101_0101
    tt.clock_project_once()
    check("uio inputs high", int(tt.uio_out.value) & 0b1010_1010, 0b0000_0000)

    tt.uio_oe_pico.value = 0           # back to all inputs

    if failures:
        print("%d check(s) FAILED: %s" % (len(failures), ", ".join(failures)))
    else:
        print("ALL PASS")
    return not failures
