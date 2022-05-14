"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pickle
import datetime


def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, preamble_bits=1, edge_offset=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='KeyFob Decoder',   # will show up in GRC
            in_sig=[np.float32, np.float32],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.preamble_bits = preamble_bits
        self.edge_offset = edge_offset
        self.total_data_points = 0
        self.data_points_threshold = []
        self.data_points_signal = np.array([])
        self.state = 1
        self.frame_start = None
        self.frame_stop = None
        self.keys = [
                "000000000000000001110000000000000000000000000000000011101111",
                "000000000000000000010000000000000000000000000000000010100010",
                "000000000000000000110000000000000000000000000000000010011001",
                "000000000000000000010000000000000000000000000000000010100010",
                "000000000000000011110000000000000000000000000000000000000011",
                "000000000000000000010000000000000000000000000000000010100010",
                "000000000000000000110000000000000000000000000000000010011001",
                "000000000000000000010000000000000000000000000000000010100010",
                    ]

    def work(self, input_items, output_items):
        input_threshold = np.array(input_items[0])
        input_signal = np.array(input_items[1])
        if np.any(input_threshold > 0.5):
            print(len(input_signal))
            # self.total_data_points += len(input_signal)
            # # print(f"input signal len({len(input_signal)}), total {self.total_data_points})")
            # if self.state == 1:
            #     leading_edge = (input_threshold[:-1] - input_threshold[1:]) < -0.5
            #     if len(np.where(leading_edge)) > 1:
            #         print(f"multi leading edge {len(leading_edge)}")
            #     if np.any(leading_edge == True):
            #         #Find the first place that a negative is located.
            #         location = np.where(leading_edge)[0][0]
            #         #Store the start location.
            #         self.frame_start = location + 0 #delay start to eliminate leading jitter.
            #         #When edge is found start looking for the trailing edge
            #         self.state = 2
            #         #Store the data because it will span several frames.
            #         self.data_points_signal = np.append(self.data_points_signal, input_signal)
            #
            # if self.state == 2:
            #     self.data_points_signal = np.append(self.data_points_signal, input_signal)
            #     # Calculate sample 1 minus sample 2. If edge goes negative then the answer is positive.
            #     trailing_edge = (input_threshold[:-1] - input_threshold[1:]) > 0.5
            #     if len(np.where(trailing_edge)) > 1:
            #         print("multi trailing edge {len(trailing_edge)}")
            #     # self.total_data_points += len(input_threshold)
            #     # self.data_points_threshold.append(input_threshold)
            #     # if self.total_data_points > 700000: # depends on the sample rate in gnuradio
            #     #     print(f"Threshold!, points collected: {self.total_data_points}")
            #     #     self.total_data_points = 0
            #     #     for data_point in self.data_points_threshold:
            #     #         if np.any(data_point > 0.5):
            #     #             if np.any((data_point[:-1] - data_point[1:]) < -0.5):
            #     #                 leading_edge = (data_point[:-1] - data_point[1:]) < -0.5
            #     #                 location = np.where(leading_edge)[0][0]
            #     #                 print(f"leading edge at:{index},{int(location + 1)}")
            #         # with open(f'{datetime.datetime.now().strftime("%Y%m%d_%H%m%S")}_data_points.pkl', 'ab') as file:
            #         #     pickle.dump(self.data_points_threshold, file, pickle.HIGHEST_PROTOCOL)
            #         # self.data_points_threshold = []
            #
            #     # Check if any go positive.
            #     if np.any(trailing_edge == True):
            #         # Find the first place a positive is located.
            #         location = np.where(trailing_edge)[0][0]
            #         # Store the relative stop location as it is in the whole data set not just the current frame.
            #         self.frame_stop = (len(self.data_points_signal) - int(len(input_signal))) + location
            #         # debug
            #         # print 'trailing edge location ', stop
            #         # print 'stop minus start', (stop - start)
            #         self.state = 3
            #
            # if self.state == 3:
            #     positive_edges = []
            #     negative_edges = []
            #     state = 0
            #     data = self.data_points_signal
            #     for index, d in enumerate(data):
            #         if state == 0 and d == 1:
            #             positive_edges.append(index)
            #             state = 1
            #         if state == 1 and d == 0:
            #             negative_edges.append(index)
            #             state = 0
            #     durations = []
            #     for index, edge in enumerate(positive_edges):
            #         diff = negative_edges[index] - edge
            #         durations.append(diff)
            #     signal1 = []
            #     signal_started = False
            #     signal_end = None
            #     for index, d in enumerate(durations):
            #         if d > 1000 or signal_started:
            #             signal_started = True
            #             if 1000 < d < 1500:
            #                 signal1.append(1)
            #             if d < 1000:
            #                 signal1.append(0)
            #             if d > 1500:
            #                 signal_end = index + 1  # save where signal has ended in the data
            #                 signal_started = False
            #                 break
            #     signal2 = []
            #     for index, d in enumerate(durations[signal_end:]):
            #         if d > 1000 or signal_started:
            #             signal_started = True
            #             if 1000 < d < 1500:
            #                 signal2.append(1)
            #             if d < 1000:
            #                 signal2.append(0)
            #             if d > 1500:
            #                 break
            #     print(f"Singal_1: {bitstring_to_bytes(''.join(str(d) for d in signal1))}, bitstream {''.join(str(d) for d in signal1)}")
            #     # print(f"Singal_2: {bitstring_to_bytes(''.join(str(d) for d in signal2))}, bitstream {''.join(str(d) for d in signal2)}")
            #     signal = ''.join(str(d) for d in signal1)
            #     for key in self.keys:
            #         next_signal = []
            #         for index,s in enumerate(signal):
            #             next_signal.append(int(s) ^ int(key[index]))
            #         print(''.join(str(d) for d in next_signal))
            #     self.total_data_points = 0
            #     self.data_points_threshold = []
            #     self.data_points_signal = np.array([])
            #     self.state = 1
            #     self.frame_start = None
            #     self.frame_stop = None
        return len(input_items[0])

