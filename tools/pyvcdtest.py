import sys
from vcd import VCDWriter

with VCDWriter(sys.stdout, timescale='1 ns', date='today') as writer:
    counter_var = writer.register_var('a.b.c', 'counter', 'integer', size=8)
    real_var = writer.register_var('a.b.c', 'x', 'real', init=1.23)
    for timestamp, value in enumerate(range(10, 20, 2)):
        writer.change(counter_var, timestamp, value)
    writer.change(real_var, 5, 3.21)
