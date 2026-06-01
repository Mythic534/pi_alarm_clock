import subprocess


class AlarmPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.process = None

    def is_playing(self):
        return self.process is not None and self.process.poll() is None

    def sound_alarm(self):
        if not self.is_playing():
            self.process = subprocess.Popen(["mpg123", self.audio_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_alarm(self):
        if self.is_playing():
            self.process.terminate()
            self.process = None

if __name__ == "__main__":
    player = AlarmPlayer("./alarm_sounds/strobe.mp3")
    player.sound_alarm()