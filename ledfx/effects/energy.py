from ledfx.effects.audio import AudioReactiveEffect
import voluptuous as vol
import numpy as np


class EnergyAudioEffect(AudioReactiveEffect):

    NAME = "Energy"
    CONFIG_SCHEMA = vol.Schema({
        vol.Optional('blur', description='Amount to blur the effect', default=4.0): vol.Coerce(float),
        vol.Optional('mirror', description='Mirror the effect', default=True): bool,
        vol.Optional('swapColors', description='Swap The the Colours', default=False): bool,
        vol.Optional('scale', description='Scale factor for the energy', default=1.0):  vol.All(vol.Coerce(float), vol.Range(min=0.0, max=5.0)),
    })

    def config_updated(self, config):
        self._p_filter = self.create_filter(
            alpha_decay=0.1,
            alpha_rise=0.50)

    def audio_data_updated(self, data):
        # print(data.melbank_lows())
        # Calculate the low, mids, and high indexes scaling based on the pixel count
        lows_idx = int(np.mean(self.pixel_count *
                               data.melbank_lows()) ** self._config['scale'])
        mids_idx = int(np.mean(self.pixel_count *
                               data.melbank_mids()) ** self._config['scale'])
        highs_idx = int(np.mean(self.pixel_count *
                                data.melbank_highs()) ** self._config['scale'])

        # Build the new energy profile based on the mids, highs and lows setting
        # the colors as red, green, and blue channel respectively

        # Just create an empty pixels array of [[0 (Red),0 (Green),0 (Blue)] x PixelCount]
        p = np.zeros(np.shape(self.pixels))
        if self._config['swapColors']:
            p[:lows_idx, 2] = 255.0
            p[:mids_idx, 1] = 255.0
            p[:highs_idx, 0] = 255.0
        else:
            p[:lows_idx, 0] = 255.0
            p[:mids_idx, 1] = 255.0
            p[:highs_idx, 2] = 255.0

        # Filter and update the pixel values
        self.pixels = self._p_filter.update(p)
