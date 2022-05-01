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


def get_positions(filename, current_position):
    file = open(filename)
    csvreader = csv.reader(file)
    # header = next(csvreader)
    # print (header)
    # note_nums = np.array([])
    positions = []
    abs_pos = []
    # timestamps = np.array([])
    # durations = np.array([])

    for i, row in enumerate(csvreader):
        if i >=1:
            # print (len(row))
            # note_nums = np.append(note_nums, row[0])
            positions.append(int(float(row[1])+current_position))
            abs_pos.append(int(float(row[1])))
            # timestamps = np.array(timestamps, row[2])
            # durations = np.array(durations, row[3])
        else:
            pass
    return positions, abs_pos


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

def twos_complement(pos):
    loc = pos + 4294967296
    return loc

def negative_goal_val(pos):
    loc = pos - 4294967296 
    return loc

## Code for making notes

# Create fake data

def servo_delay_time(deltaPosition):
    dur = deltaPosition/5000
    return dur

def stepper_comm_delay(dur):
    time.sleep(dur)
    # print ("Stepper message sent")

def rotate_stepper(dur):
    time.sleep(dur)
    # print ('stepper rotated')

def damp(stepper_state, durComm, durRotate):
    stepper_comm_delay(durComm)
    rotate_stepper(durRotate)
    stepper_state = 0
    return stepper_state

def pluck(stepper_state, durComm, durRotate):
    stepper_comm_delay(durComm)
    rotate_stepper(durRotate)
    stepper_state = 1
    return stepper_state

def rotate_servo(dur):
    # Start rotating the servo
    servo_rotate = 1
    time.sleep(dur)
    servo_rotate = 0

## Every note type will have goalPosition, noteDur, damping boolean, durComm: communication delay between py and arduino, durRotate: time to pluck/ damp after stepper starts moving

def normal(deltaPosition, noteDur, durComm, durRotate, t0, damping):
    # Rotate the Servo to the goal position
    servoDur = servo_delay_time(deltaPosition)
    rotate_servo(servoDur)
    # Pluck the note
    pluck(stepper_state, durComm, durRotate)
    # Sleep for noteDur - delay times
    print ('Normal - Plucked at: ', time.time()-t0)
    if damping == 1:
        time.sleep(noteDur-durComm-durRotate)
        damp(stepper_state, durComm, durRotate)
    
def slide(deltaPosition, noteDur, durComm, durRotate, t0, damping):
    # Pluck the note
    pluck(stepper_state, durComm, durRotate)
    print('Slide - Plucked at: ', time.time()-t0)
    # Move servo position by delta
    servoDur = servo_delay_time(deltaPosition)
    rotate_servo(servoDur)
    # Damp if needed
    if damping == 1:
        time.sleep(noteDur-durComm-durRotate)
        damp(stepper_state, durComm, durRotate)

def slideWithoutPluck(deltaPosition, noteDur, durComm, durRotate, t0, damping):
    # Move servo position by delta
    servoDur = servo_delay_time(deltaPosition)
    rotate_servo(servoDur)
    # Damp if needed
    if damping == 1:
        time.sleep(noteDur-durComm-durRotate)
        damp(stepper_state, durComm, durRotate)

def normal_wrapper(deltaPosition, noteDur, durComm, durRotate, t0, servoDur, prevDampTime, ibi, damping=True):
    mechDur = servoDur + durComm + durRotate# 2*durComm because we're communicating with two stepper motors. #Replace 2 with 1 if threading
    # pluck at 1s
    sleepTime = ibi-mechDur-prevDampTime
    time.sleep(sleepTime)
    # Execute normal pluck note
    tntmp = time.time()
    normal(deltaPosition, noteDur, durComm, durRotate, t0, damping)
    print('sleeptime: ', sleepTime) #'Timestamp for %sth note: ' % i, time.time()-t0

def slide_wrapper(deltaPosition, noteDur, durComm, durRotate, t0, servoDur, prevDampTime, ibi, damping=True):
    # Add stepper comm time
    mechDur = servoDur + durComm # 2*durComm because we're communicating with two stepper motors
    # sleep before sending the next note to be in time
    sleepTime = ibi-mechDur-prevDampTime
    time.sleep(sleepTime)
    tstmp = time.time()
    # Execute normal pluck note
    slide(deltaPosition, noteDur, durComm, durRotate, t0, damping)
    print('sleeptime: ', sleepTime) #'Timestamp for %sth note: ' % i, time.time()-t0, )

def slideWithoutPluck_wrapper(deltaPosition, noteDur, durComm, durRotate, t0, servoDur, prevDampTime, ibi, damping=True):
    # Add stepper comm time
    mechDur = servoDur # 2*durComm because we're communicating with two stepper motors
    # sleep before sending the next note to be in time
    sleepTime = ibi-mechDur-prevDampTime
    time.sleep(sleepTime)
    # tstmp = time.time()
    # Execute normal pluck note
    slideWithoutPluck(deltaPosition, noteDur, durComm, durRotate, t0, damping)
    print('sleeptime: ', sleepTime) #'Timestamp for %sth note: ' % i, time.time()-t0, )

# Leave 1s blank at the beginning for servo to adjust if needed
def tempoGrid(tempo, songDur):
    # tempo in bpm, maxDur: Song (or max) duration in seconds
    return np.arange(1, songDur+1, 60/tempo)

def exec(tempo, songDur, positions, noteDurations, styles, dampNote, durComm, durRotate):
    ## Play the first note at 1s.
    # Subtract previous damp time from new note sleep time
    
    # get all onset timestamps
    # grid = tempoGrid(tempo, songDur)
    ibi = 60/tempo
    stepper_dur = durComm + durRotate

    # Start global time
    t0 = time.time()
    damping = True

    prevDampTime = 0 # durComm+durRotate
    
    # Write code for the first note
    for i in np.arange(len(positions)):
        print('damp time: ', prevDampTime)
        deltaPosition = positions[i]
        print('Delta position: ', deltaPosition)
        noteDur = noteDurations[i]
        damping = dampNote[i]
        if noteDur <= durComm+durRotate:
            print ('BassBot Error: noteDur less than minimum value. Min value = %s' %stepper_dur, 'for %sth note: '%i)
            break
        # if noteDur == 1:
        #     damping is False
        # compute delay time due to position
        servoDur = servo_delay_time(deltaPosition)
        if styles[i] =='n': 
            normal_wrapper(deltaPosition, noteDur, durComm, durRotate, t0, servoDur, prevDampTime, ibi, damping)
        elif styles[i] == 's':
            slide_wrapper(deltaPosition, noteDur, durComm, durRotate, t0, servoDur, prevDampTime, ibi, damping)
        elif styles[i] == 'o':
            slideWithoutPluck_wrapper(deltaPosition, noteDur, durComm, durRotate, t0, servoDur, prevDampTime, ibi, damping=True)
            
        if damping == 0:
            prevDampTime = 0
        else:
            prevDampTime = noteDur

