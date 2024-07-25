import kivy
kivy.require('1.3.0') # 1.3.0: for Sound.volume

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

import os


# Config app
# to run on opengl 1.1 as well
Config.set('graphics', 'multisamples', '0')
# set window size
Config.set('graphics', 'width', 480)
Config.set('graphics', 'height', 320)
# apply config settings
Config.write()

# Load UI declarations
Builder.load_file('AquaScreen.kv')
Builder.load_file('Layouts.kv')
Builder.load_file('Widgets.kv')
Builder.load_file('MainScreen.kv')
Builder.load_file('StorageScreen.kv')
Builder.load_file('MediaPlayerScreen.kv')
Builder.load_file('BluetoothScreen.kv')

# Declare all screens
class MainScreen(Screen):
    pass

class StorageScreen(Screen):
    pass

class MediaPlayerScreen(Screen):
    pass

class BluetoothScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(StorageScreen(name='storage'))
sm.add_widget(MediaPlayerScreen(name='mediaPlayer'))
sm.add_widget(BluetoothScreen(name='bluetooth'))


class MainApp(App):
    # Current music
    sound = None
    volume = 1.0

    def build(self):
        return sm

    def setScreen(self, name):
        sm.current = name

    # Called from MediaPlayerScreen.FileChooserListView when a file is selected
    def onListItemSelected(self, selectedFilePaths):
        try:
            # Check file type
            (name, extension) = os.path.splitext(selectedFilePaths[0])
            if extension == '.mp3':
                # Stop previous track if present
                if self.sound:
                    self.sound.stop()

                print 'Playing file:', selectedFilePaths[0]
                # Load new track
                self.sound = SoundLoader.load(selectedFilePaths[0])
                # Apply previously set volume for new track
                self.sound.volume = self.volume
                # Play new track
                self.sound.play()
            else:
                print 'File type', extension, 'is not supported!'

        # IndexError can occur from selectedFilePaths[0]
        except IndexError as detail:
            print 'IndexError:', detail

    def playOrStop(self):
        if sm.current == 'bluetooth':
            # TODO handle bluetooth play/stop
            pass
        else:
            if sm.current == 'mediaPlayer':
                if self.sound is not None:
                    if self.sound.state == 'play':
                        # self.sound.get_pos() # returns always 0 :(
                        self.sound.stop()
                    else:
                        self.sound.play()

    def volUp(self):
        if sm.current == 'bluetooth':
            # TODO handle volume at system level
            pass
        else:
            if sm.current == 'mediaPlayer':
                if self.sound is not None:
                    if self.sound.volume <= 0.9:
                        self.sound.volume = self.sound.volume + 0.1
                        # save volume info for next track
                        self.volume = self.sound.volume

    def volDown(self):
        if sm.current == 'bluetooth':
            # TODO handle volume at system level
            pass
        else:
            if sm.current == 'mediaPlayer':
                if self.sound is not None:
                    if self.sound.volume >= 0.1:
                        self.sound.volume = self.sound.volume - 0.1
                        # save volume info for next track
                        self.volume = self.sound.volume


if __name__ == '__main__':
    MainApp().run()
