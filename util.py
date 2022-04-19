from scipy.io.wavfile import read as wavread
import numpy as np
import scipy.fftpack
import csv
from scipy.signal import medfilt, butter, lfilter, freqz

# using functions from previous assignments
def ToolReadAudio(cAudioFilePath):
    [f_s, x] = wavread(cAudioFilePath)

    if x.dtype == 'float32':
        x = x
    else:
        # change range to [-1,1)
        if x.dtype == 'uint8':
            nbits = 8
        elif x.dtype == 'int16':
            nbits = 16
        elif x.dtype == 'int32':
            nbits = 32

        x = x / float(2**(nbits - 1))

    # special case of unsigned format
    if x.dtype == 'uint8':
        x = x - 1.

    return f_s, x


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


def block_audio(x, blockSize, hopSize, fs):
    # allocate memory
    numBlocks = math.ceil(x.size / hopSize)
    xb = np.zeros([numBlocks, blockSize])
    # compute time stamps
    t = (np.arange(0, numBlocks) * hopSize) / fs

    x = np.concatenate((x, np.zeros(blockSize)), axis=0)

    for n in range(0, numBlocks):
        i_start = n * hopSize
        i_stop = np.min([x.size - 1, i_start + blockSize - 1])

        xb[n][np.arange(0, blockSize)] = x[np.arange(i_start, i_stop + 1)]

    return (xb, t)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# get silences from audio
def extract_rmsDb(xb, DB_TRUNCATION_THRESHOLD=-100):
    rmsDb = np.maximum(20 * np.log10(np.sqrt(np.mean(xb ** 2, axis=-1))), DB_TRUNCATION_THRESHOLD)  #need to handle zero blocks
    return rmsDb


def create_voicing_mask(rmsDb, thresholdDb): 
    return 0 + (rmsDb >= thresholdDb)


def apply_voicing_mask(f0, mask):
    return f0 * mask

def detect_silence(xb, f0, thres_dB):
    rmsDb = extract_rmsDb(xb, DB_TRUNCATION_THRESHOLD=-100)
    mask = create_voicing_mask(rmsDb, thres_dB)
    f0f = apply_voicing_mask(f0, mask)
    return f0f

# A function that wraps around the frequency in a given range to remove octave errors
def f0_scaled(f0, fmin, fmax):
    if f0 == 0:
        f_wrapped = f0
    elif f0 >= fmin and f0 <= fmax:
        f_wrapped = f0
    elif f0 > 0 and f0 < fmin:
        # add relevant f0
        f0_wrapped = f0
    elif f0 > fmax:
        # add relevant f0
        f0_wrapped = f0
    return f0_wrapped

def wrapped_f0(f0, fmin, fmax):
    # f0: array or current frame.
    if len(f0) == 1:
        f0_wrapped = f0_scaled(f0, fmin, fmax)
    
    else:
        f0_wrapped = np.array([])
        for f in f0:
            f0_wrapped = np.append(f0_wrapped, f0_scaled(f, fmin, fmax))
            
    return f0_wrapped