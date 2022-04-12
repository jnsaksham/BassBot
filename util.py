# from scipy.io.wavfile import read as wavread
import numpy as np
# import scipy.fftpack
import csv

# using functions from previous assignments
# def ToolReadAudio(cAudioFilePath):
#     [samplerate, x] = wavread(cAudioFilePath)
#     if x.ndim == 2:
#         x = x[:, 1]
#     if x.dtype == 'float32':
#         audio = x
#     else:
#         # change range to [-1,1)
#         if x.dtype == 'uint8':
#             nbits = 8
#         elif x.dtype == 'int16':
#             nbits = 16
#         elif x.dtype == 'int32':
#             nbits = 32
#         audio = x / float(2 ** (nbits - 1))
#     # special case of unsigned format
#     if x.dtype == 'uint8':
#         audio = audio - 1.
#     return (samplerate, audio)


# def block_audio(x, blockSize, hopSize, fs):
#     # allocate memory
#     numBlocks = math.ceil(x.size / hopSize)
#     xb = np.zeros([numBlocks, blockSize])
#     # compute time stamps
#     t = (np.arange(0, numBlocks) * hopSize) / fs
#     x = np.concatenate((x, np.zeros(blockSize)), axis=0)
#     for n in range(0, numBlocks):
#         i_start = n * hopSize
#         i_stop = np.min([x.size - 1, i_start + blockSize - 1])
#         xb[n][np.arange(0, blockSize)] = x[np.arange(i_start, i_stop + 1)]
#     return xb, t


def get_positions(filename):
    file = open(filename)
    csvreader = csv.reader(file)
    # header = next(csvreader)
    # print (header)
    # note_nums = np.array([])
    positions = []
    # timestamps = np.array([])
    # durations = np.array([])

    for i, row in enumerate(csvreader):
        if i >=1:
            # print (len(row))
            # note_nums = np.append(note_nums, row[0])
            positions.append(int(float(row[1])))
            # timestamps = np.array(timestamps, row[2])
            # durations = np.array(durations, row[3])
        else:
            pass
    return positions