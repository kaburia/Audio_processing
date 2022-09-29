# import required modules
from os import path
from pydub import AudioSegment
import librosa
import librosa.display
import IPython.display


# assign files
input_file = "oh_the_larceny_man_on_a_mission_official_audio_mp3_33970.mp3"
output_file = "result.wav"

# convert mp3 file to wav file
sound = AudioSegment.from_mp3(input_file)
sound.export(output_file, format="wav")





file_name = 'result.wav'
y, sr = librosa.load(file_name)

# # Trim silent edges
# mission, _ = librosa.effects.trim(y)
# librosa.display.waveplot(mission, sr=sr)
IPython.display.Audio(data=y, rate=sr)