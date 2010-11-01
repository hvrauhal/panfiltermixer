try: 
    from tkinter import *
    import getopt
except Exception as err:
    print("Error: " + str(err))
    print("This program requires Python 3.1")
    import sys
    sys.exit(2)
import re

class AfPanGenerator:
    def __init__(self, master, input_count=5, output_count=2):
        self.output_channels = output_count
        self.input_channels = input_count
        Label(master, text="{} input channels, {} output channels for each".format(self.input_channels, self.output_channels)).pack(side=TOP)

        slidersFrame = Frame(master)
        slidersFrame.pack(side=TOP)

        self.channelScales = self.generate_scales(slidersFrame, self.input_channels, self.output_channels)

        bottomFrame = Frame(master)
        bottomFrame.pack(side=TOP)
        Label(bottomFrame, text="Template").pack()
        self.template = Entry(bottomFrame, width=80)
        self.template.insert(INSERT, "-channels {} -af pan={}:{}")
        self.template.pack(padx=10, pady=3)
        Label(bottomFrame, text="Mixer string").pack()
        mixerStringFrame = Frame(bottomFrame)
        mixerStringFrame.pack()
        self.mixerString = Entry(mixerStringFrame, width=80)
        self.mixerString.pack(padx=10, pady=3, side=LEFT)
        self.mixerString.bind("<KeyRelease>", self.mixerStringToChannels)

        Label(bottomFrame, text="Commandline").pack(side=TOP)
        self.commandLine = Entry(bottomFrame, width=80)
        self.commandLine.pack(padx=10, pady=3)

    def mixerStringToChannels(self, event=None):
        msString = self.mixerString.get()
        msList = [float(val) for val in msString.split(":")]
        msSubLists = [msList[i:i+2] for i  in range(0, len(msList), 2)]
        for i in range(len(msSubLists)):
            currentChannels = msSubLists[i]
            for j in range(len(currentChannels)):
                self.channelScales[i][j].set(currentChannels[j])
        self.generate_cmdline(event)

    def generate_scales(self, frame, input_channels, output_channels):
        scales = []
        for i in range(input_channels):
            channelFrame = LabelFrame(frame, text=str(i+1), padx=1, pady=1)
            channelFrame.pack(side=LEFT, padx=10, pady=10)
            channels = []
            for j in range(output_channels):
                channel = Scale(channelFrame, from_=1.5, to=0, resolution=0.1)
                channel.bind("<ButtonRelease-1>", self.update_mixerstring)
                channel.pack(side=LEFT, padx=1)
                channels.append(channel)
            scales.append(channels)
        return scales
        
    def update_mixerstring(self, event=None):
        def joinScales(scales):
            scaleValues = [re.sub(".0$","",str(scale.get())) for scale in scales]
            return ":".join(scaleValues)

        allChannels = [joinScales(channel) for channel in self.channelScales]
        slidersCombined=":".join(allChannels)
        self.mixerString.delete("0", END)
        self.mixerString.insert("0", slidersCombined)
        self.generate_cmdline(event)

    def generate_cmdline(self, event=None):
        cmdLine = self.template.get().format(str(self.input_channels), str(self.output_channels), self.mixerString.get())
        self.commandLine.delete("0", END)
        self.commandLine.insert("0", cmdLine)



if __name__ == "__main__":
    def usage():
        print ("""A visual mixer for generating commandlines for MPlayer's pan filter.

Usage: {} [-i input_channels] [-o output_channels]

See http://www.mplayerhq.hu/DOCS/HTML/en/advaudio-channels.html for details.""".format(sys.argv[0]))
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "i:o:h",["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        sys.exit(2)
    input_channels = 5
    output_channels = 2
    for o, a in opts:
        if o == "-i":
            input_channels = int(a)
        elif o == "-o":
            output_channels = int(a)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"  
        
    root = Tk()
    app = AfPanGenerator(root, input_channels, output_channels)
    root.mainloop()
    try: 
        root.destroy()
    except:
        pass
