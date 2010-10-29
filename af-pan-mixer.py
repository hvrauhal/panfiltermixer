try: 
    from tkinter import *
    import getopt
except Exception as err:
    print("Error: " + str(err))
    print("This program requires Python 3.1")
    import sys
    sys.exit(2)

class AfPanGenerator:
    '''A GUI for generating the commandlines for MPlayers pan audio filter. 
    
    See http://www.mplayerhq.hu/DOCS/HTML/en/advaudio-channels.html for details of the commandline format.
    '''
    def __init__(self, master, input_count=5, output_count=2):
        self.output_channels = output_count
        self.input_channels = input_count
        Label(master, text="{} input channels, {} output channels for each".format(self.input_channels, self.output_channels)).pack(side=TOP)

        slidersFrame = Frame(master)
        slidersFrame.pack(side=TOP)

        self.channelScales = self.generate_scales(slidersFrame, self.input_channels, self.output_channels)

        bottomFrame = Frame(master)
        bottomFrame.pack(side=TOP)

        self.getAfPanButton = Button(bottomFrame, text="Print commandline", command=self.generate_cmdline)
        self.getAfPanButton.pack()
        
    def generate_scales(self, frame, input_channels, output_channels):
        scales = []
        for i in range(input_channels):
            channelFrame = LabelFrame(frame, text=str(i+1), padx=1, pady=1)
            channelFrame.pack(side=LEFT, padx=10, pady=10)
            channels = []
            for j in range(output_channels):
                channel = Scale(channelFrame, from_=1.5, to=0, resolution=0.1)
                channel.pack(side=LEFT, padx=1)
                channels += [channel]
            scales += [channels]
        return scales
        
    def generate_cmdline(self):
        def joinScales(scales):
            scaleValues = [str(scale.get()) for scale in scales]
            return ":".join(scaleValues)

        allChannels = [joinScales(channel) for channel in self.channelScales]
        slidersCombined=":".join(allChannels)
        print ("-channels {} -af pan={}:{}".format(str(self.input_channels), str(self.output_channels), slidersCombined))



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
