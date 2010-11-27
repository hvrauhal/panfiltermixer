import unittest
from af_pan_mixer import AfPanGenerator

class AfPanTests(unittest.TestCase):
    def test_split_single(self):
        self.assertEquals([[1]], AfPanGenerator.group_mixer_to_Is_and_Os("1",1))
    def test_split_two_inputs(self):
        self.assertEquals([[1,2]], AfPanGenerator.group_mixer_to_Is_and_Os("1:2",2))
    def test_split_two_inputs_two_outputs(self):
        self.assertEquals([[1,2],[3,4]], AfPanGenerator.group_mixer_to_Is_and_Os("1:2:3:4",2))
    def test_split_three_inputs(self):
        self.assertEquals([[1,2,3]], AfPanGenerator.group_mixer_to_Is_and_Os("1:2:3",3))
    def test_split_three_inputs_two_outputs(self):
        self.assertEquals([[1,2,3],[4,5,6]], AfPanGenerator.group_mixer_to_Is_and_Os("1:2:3:4:5:6",3))

    def test_mixerstring_to_scales_and_cmdline(self):
        class MockMixerString():
            def get(self):
                return "0.1:1.1:2.1:3.1:4.1:5.1"
        class MS:
            def __init__(self, value):
                self.value = value
            def __repr__(self):
                return str(self.value)
            def set(self, value):
                self.value = value

        afPan = AfPanGenerator(None)
        afPan.channelScales=[[MS(0),MS(1),MS(2)],[MS(3),MS(4),MS(5)]]
        afPan.mixerString = MockMixerString()
        afPan.output_channels = 3
        afPan.mixerstring_to_scales_and_cmdline()
        self.assertEquals("[[0.1, 1.1, 2.1], [3.1, 4.1, 5.1]]", str(afPan.channelScales))

if __name__ == '__main__':
    unittest.main()
            
