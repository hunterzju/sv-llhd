import sys
from vcd import VCDWriter

class Signal:
    def __init__(self, full_name):
        self.fullname = full_name
        self.modname = None
        self.signame = None
        self.sigvals = []
        self.sigvar = None

    def set_modname(self, mod_name):
        self.modname = mod_name

    def set_signame(self, sig_name):
        self.signame = sig_name

    def add_sigval(self, val):
        self.sigvals.append(val)

    def set_sigvar(self, sig_var):
        self.sigvar = sig_var

class SigVal:
    def __init__(self, time, dlt, eps, val):
        self.time = time
        self.dlt = dlt
        self.eps = eps
        self.val = val
        self.sig = None

    def set_sig(self, sig):
        self.sig = sig

signal_dict = dict()
val_list = []

def create_new_signale(fullname):
    split_names = fullname.split("/")
    sig_name = split_names[-1]
    # print(".".join(split_names[:-1]))
    mod_name = ".".join(split_names[:-1])
    new_sig = Signal(fullname)
    new_sig.set_modname(mod_name)
    new_sig.set_signame(sig_name)
    # print(f"{new_sig.modname}:{new_sig.signame}")
    return new_sig

def dump_vcd(path):
    with open(path, "w") as fw:
        with VCDWriter(fw, timescale='1 ps', date='today') as writer:
            for sig in signal_dict.values():
                sig_var = writer.register_var(sig.modname, sig.signame, 'integer', size=8)
                sig.set_sigvar(sig_var)

            for val in val_list:
                writer.change(val.sig.sigvar, val.time, val.val)

           # for sig in signal_dict.values():
           #     for v in sig.sigvals:
           #         writer.change(sig.sigvar, v.time, v.val)

def main():
    inputfile = sys.argv[1]
    lines = None
    with open(inputfile,"r", newline='') as fread:
        lines = fread.readlines()

    for l in lines:
        content = l.strip("\n").split()
        full_sig = content[3]
        timeval = [int(content[0].strip("ps")), int(content[1].strip("d")), int(content[2].strip("e"))]
        val = int(content[-1], 16)

        if full_sig not in signal_dict.keys():
            signal = create_new_signale(full_sig)
            signal_dict[full_sig] = signal
        else:
            signal = signal_dict[full_sig]
        val = SigVal(timeval[0], timeval[1], timeval[2], val)
        val.set_sig(signal)
        val_list.append(val)
        signal.add_sigval(val)

    outputfile = sys.argv[2]
    dump_vcd(outputfile)



if __name__ == "__main__":
    main()

