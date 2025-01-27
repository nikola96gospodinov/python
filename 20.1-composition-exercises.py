from typing import List

class Song:
    def __init__(self, title, artist, duration_in_seconds) -> None:
        self._title = ""
        self._artist = ""
        self._duration_in_seconds = 0
        
        self.title = title
        self.artist = artist
        self.duration_in_seconds = duration_in_seconds
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("title must be a string")
        if value.strip() == "":
            raise ValueError("title must be a non empty string")
        
        self._title = value
        
    @property
    def artist(self):
        return self._artist
        
    @artist.setter
    def artist(self, value):
        if not isinstance(value, str):
            raise TypeError("artist must be a string")
        if value.strip() == "":
            raise ValueError("artist must be a non empty string")
        
        self._artist = value
        
    @property
    def duration_in_seconds(self):
        return self._duration_in_seconds
    
    @duration_in_seconds.setter
    def duration_in_seconds(self, value):
        if not isinstance(value, int):
            raise TypeError("duration must be an integer")
        if value <= 0:
            raise ValueError("duration must be a positive integer")
        
        self._duration_in_seconds = value
        
class Playlist:
    def __init__(self, name) -> None:
        self._name = ""
        self._songs: List[Song] = []
        self._current_song: Song | None = None
        
        self.name = name
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Playlist name must be a string")
        if value.strip() == "":
            raise ValueError("Playlist name must be a non empty string")
        
        self._name = value
        
    @property
    def current_song(self):
        return self._current_song
        
    def validate_song(self, song: Song):
        if not isinstance(song, Song):
            raise TypeError("make sure you're passing a song")
        
    def add_song(self, song: Song):
        self.validate_song(song)
        
        if len(self._songs) == 0:
            self._current_song = song
        
        self._songs.append(song)
        
    def remove_song(self, song: Song):
        self.validate_song(song)
        
        if song not in self._songs or len(self._songs) == 0:
            print("Song not in the playlist")
            return
        
        if len(self._songs) == 1:
            self._current_song = None
        
        self._songs.remove(song)
        
        if self._songs:
            self._current_song = self._songs[0]
    
    def play_next_song(self):
        current_song = self._current_song
        
        if current_song:
            current_song_index = self._songs.index(current_song)
            
            if current_song_index + 1 > len(self._songs) - 1:
                print("This is the last song")
            else:
                self._current_song = self._songs[current_song_index + 1]
        else:
            print("There are currently no songs")
            return None
        
    def play_previous_song(self):
        current_song = self._current_song
        
        if current_song:
            current_song_index = self._songs.index(current_song)
            
            if current_song_index == 0:
                print("This is the first song")
            else:
                self._current_song = self._songs[current_song_index - 1]
        else:
            print("There are currently no songs")
            return None 
        
class AudioDevice:
    def __init__(self, volume) -> None:
        self._status = "paused"
        self._volume = 0
        
        self.volume = volume
        
    @property
    def status(self):
        return self._status
        
    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        if not isinstance(value, int):
            raise TypeError("Volume must be an integer")
        if value < 0  or value > 100:
            raise ValueError("Value must be between 0 and 100")
        
        self._volume = value
        
    def play_audio(self):
        self._status = "playing"
        
    def pause_audio(self):
        self._status = "paused"
        
class MusicPlayer:
    def __init__(self, playlist: Playlist, audio_device: AudioDevice):
        self._playlist = None
        self._audio_device = None
        
        self.playlist = playlist
        self.audio_device = audio_device
        
    @property
    def playlist(self):
        return self._playlist
    
    @playlist.setter
    def playlist(self, value):
        if not isinstance(value, Playlist):
            raise TypeError("Make sure you pass a Playlist")
        
        self._playlist = value
        
    @property
    def audio_device(self):
        return self._audio_device
    
    @audio_device.setter
    def audio_device(self, value):
        if not isinstance(value, AudioDevice):
            raise TypeError("Make sure you pass an AudioDevice")
        
        self._audio_device = value
        
    def play(self):
        current_song = self._playlist.current_song
        
        if current_song:
            self._audio_device.play_audio()
            print(f"Playing {current_song.title}")
        else:
            print("No songs added")
            
    def pause(self):
        current_status = self._audio_device.status
        
        if current_status == "paused":
            print("The audio player isn't running")
        else:
            self._audio_device.pause_audio()
            
    def next_song(self):
        self._playlist.play_next_song()
        
    def previous_song(self):
        self._playlist.play_previous_song()


class Device:
    def __init__(self, name, location):
        self._name = ""
        self._location = ""
        self._is_on = False
        
        self.name = name
        self.location = location
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if value.strip() == "":
            raise ValueError("name must be a non empty string")
        
        self._name = value
        
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, value):
        if not isinstance(value, str):
            raise TypeError("location must be a string")
        if value.strip() == "":
            raise ValueError("location must be a non empty string")
        
        self._location = value
        
    def turn_on(self):
        if self._is_on:
            print(f"{self._name} is already on")
        
        self._is_on = True
        print(f"{self._name} is turned on") 
        
    def turn_off(self):
        if self._is_on == False:
            print(f"{self._name} is already off")
        
        self._is_on = False
        print(f"{self._name} is turned off")
        
    @property
    def status(self):
        return "On" if self._is_on else "Off"
    
class Light(Device):
    def __init__(self, name, location, brightness=100):
        super().__init__(name, location)
        self._brightness = 0
        
        self.brightness = brightness
        
    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, int):
            raise TypeError("Brightness must be an integer")
        if value < 0  or value > 100:
            raise ValueError("Value must be between 0 and 100")
        
        self._brightness = value
        
class Thermostat(Device):
    def __init__(self, name, location, temperature=22):
        super().__init__(name, location)
        self._temperature = 0
        
        self.temperature = temperature
        
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("temperature must be a number")
        
        self._temperature = value
        
class SecurityCamera(Device):
    def __init__(self, name, location, recording_status="recording"):
        super().__init__(name, location)
        self._recording_status = "recording"
        
        self.recording_status = recording_status
        
    @property
    def recording_status(self):
        return self._recording_status
    
    @recording_status.setter
    def recording_status(self, value):
        if value not in ("recording", "not recording"):
            raise ValueError("must be either recording or not recording")
        
        self._recording_status = value
    
    def record(self):
        if self.recording_status == "recording":
            print("Already recording")
            return
        
        self.recording_status = "recording"
        
    def stop_recording(self):
        if self.recording_status == "not recording":
            print("Already not recording")
            return
        
        self.recording_status = "not recording"
        
class SmartHome:
    def __init__(self):
        self._devices: List[Device] = []
        
    def validate_device(self, value: Device):
        if not isinstance(value, Device):
            raise TypeError("Make sure you pass a Device")
    
    def add_device(self, device: Device):
        self.validate_device(device)
        self._devices.append(device)
    
    def remove_device(self, device: Device):
        self.validate_device(device)
        
        if device not in self._devices:
            print("Device not found")
            return
        
        self._devices.remove(device)

    
    def get_device_status(self, location):
        devices_by_location = [device for device in self._devices if device.location == location]
        
        for device in devices_by_location:
            print(f"{device.name} is {device.status}")
    
    def turn_all_off(self):
        for device in self._devices:
            device.turn_off()
    
    def turn_all_on(self):
        for device in self._devices:
            device.turn_on()