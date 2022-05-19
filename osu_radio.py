import os, random, vlc, time, subprocess, pypresence, json

class OsuRadio:
    def __init__(self):
        self.config = None
        with open("./config.json", "r") as f:
            self.config = json.load(f)

        self.songs = self.config["songs_folder"]
        self.songs_folders = os.listdir(self.songs)
        self.client_id = "976575798502883361"
        self.rpc = pypresence.Presence(self.client_id)
        self.connected = False

        random.shuffle(self.songs_folders)

    def try_connect(self):
        if self.connected: return

        try:
            self.rpc.connect()
            self.connected = True
        except Exception as e: print(e)

    def get_map_id(self, folder):
        folder = folder.split(" ")[0]
        return "https://osu.ppy.sh/beatmapsets/" + folder

    def format_song(self, folder):
        folder = folder.split(" ")
        song = ""
        
        for i in range(len(folder)):
            if not i == 0:
                song += folder[i] + " "
        return song[:-1]

    def set_status(self, map_name, duration):
        self.try_connect()

        try:
            map_id = self.get_map_id(map_name)
            map_name = self.format_song(map_name)
            self.rpc.update(state=map_name, end=int(time.time() + int(duration)), large_image="osu", buttons=[{"label": "Beatmap", "url": map_id}])
        except Exception as e: print(e)

    def play(self):
        for folder in self.songs_folders:
            _og = folder
            folder = os.path.join(self.songs, folder)

            if os.path.isdir(folder):
                for filename in os.listdir(folder):
                    filename = os.path.join(self.songs, folder, filename)

                    if filename.endswith(".mp3"):
                        player = vlc.MediaPlayer(filename)

                        args = ["ffprobe", "-show_entries", "format=duration", "-i", filename]
                        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
                        popen.wait()
                        output = popen.stdout.read().decode()
                        duration = float(output.split("duration=")[1].split("\n")[0])

                        self.set_status(_og, duration)

                        player.play()
                        time.sleep(duration)
                        player.stop()

                        break

OsuRadio().play()

