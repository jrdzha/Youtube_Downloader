import os
import sys
from pytube import YouTube
import subprocess

# video/audio itag preference
video_itag_pref_list = [337, 336, 315, 313, 308, 266, 271, 264, 138, 38, 335, 303, 299, 248, 169, 137, 96, 85, 46, 37]
audio_itag_pref_list = [141, 251, 171, 140, 250]

total_MB = -1

def reset_progress_bar():
    global total_MB
    total_MB = -1

def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    global total_MB
    if (total_MB == -1):
        total_MB = int(bytes_remaining)
    # print('\r' + str(int(total_MB - (bytes_remaining / 1000000)) / total_MB), end='')
    printProgressBar(int(total_MB - bytes_remaining), total_MB, prefix = 'Progress:', suffix = 'Complete', length = 100)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '')
    # Print New Line on Complete
    if iteration == total:
        print()

def download_video(url):
    # load video
    video = YouTube(url)
    video.register_on_progress_callback(show_progress_bar)

    # define the name of the directory to be created
    path = video.title

    # create new directory for this video
    try:
        os.mkdir(path)
        os.mkdir(path + '/audio')
        os.mkdir(path + '/video')
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    stream_list = video.streams.all()

    # select stream with highest video
    selected_video_stream = None
    for video_itag_pref in video_itag_pref_list:
        for stream in stream_list:
            if int(stream.itag) == video_itag_pref and selected_video_stream == None:
                selected_video_stream = stream
    selected_audio_stream = None
    for audio_itag_pref in audio_itag_pref_list:
        for stream in stream_list:
            if int(stream.itag) == audio_itag_pref and selected_audio_stream == None:
                selected_audio_stream = stream

    reset_progress_bar()
    print('Downloading ' + str(selected_video_stream))
    selected_video_stream.download(path + '/video')
    reset_progress_bar()
    print('Downloading ' + str(selected_audio_stream))
    selected_audio_stream.download(path + '/audio')

    convert_video(video.title, selected_video_stream.mime_type[6:], selected_audio_stream.mime_type[6:])

def convert_video(title, video_format, audio_format):
    title_cleaned = title.replace(':', '')
    title_cleaned = title.replace('?', '')
    title_cleaned = title.replace('|', '')

    video_path = title + '/video/' + title_cleaned + '.' + video_format
    audio_path = title + '/audio/' + title_cleaned + '.' + audio_format
    output_path = title + '/' + title_cleaned + '.' + video_format

    video_path = video_path.replace(' ', '\ ')
    audio_path = audio_path.replace(' ', '\ ')
    output_path = output_path.replace(' ', '\ ')

    video_path = video_path.replace('(', '\(')
    audio_path = audio_path.replace('(', '\(')
    output_path = output_path.replace('(', '\(')

    video_path = video_path.replace(')', '\)')
    audio_path = audio_path.replace(')', '\)')
    output_path = output_path.replace(')', '\)')

    video_path = video_path.replace('|', '\|')
    audio_path = audio_path.replace('|', '\|')
    output_path = output_path.replace('|', '\|')

    cmd = 'ffmpeg -i ' +  video_path + ' -i ' + audio_path + ' -c copy ' + output_path
    print(cmd)
    subprocess.call(cmd, shell=True)  # "Muxing Done
    print('Done.')

download_video(sys.argv[1])
# convert_video('TIMELAPSE OF THE FUTURE: A Journey to the End of Time (4K)', 'webm', 'webm')






