from picovoice import (Picovoice, PicovoiceInvalidArgumentError, PicovoiceActivationError,
                       PicovoiceActivationLimitError, PicovoiceActivationRefusedError,
                       PicovoiceActivationThrottledError, PicovoiceError)
from pvrecorder import PvRecorder
from pvrhino import Inference
import os
from threading import Thread
from kivy.logger import Logger
from word2number import w2n

from lib.event_queue import BmoEvent, add_event


class SpeechListener:
    def __init__(self, root_path: str) -> None:
        try:
            access_key = os.environ.get('PV_KEY')
            if not access_key:
                raise Exception(f'No access_key defined. Please make sure the PV_KEY environment variable is defined.')
            self.picovoice = Picovoice(
                access_key=access_key,
                keyword_path=f'{root_path}/media/wake_word.ppn',
                wake_word_callback=self.wake_word_callback,
                context_path=f'{root_path}/media/stt_model.rhn',
                inference_callback=self.inference_callback,
            )

            self.recorder = PvRecorder(
                frame_length=self.picovoice.frame_length,
                device_index=-1,
            )
            self.recorder.start()
            Logger.info('Listening ... (Press Ctrl+C to exit)\n')



            add_event(BmoEvent('play_game', {'game': 'pong'}))



        except PicovoiceInvalidArgumentError as e:
            Logger.exception("One or more arguments provided to Picovoice is invalid: ")
            raise e
        except PicovoiceActivationError as e:
            Logger.exception("AccessKey activation error")
            raise e
        except PicovoiceActivationLimitError as e:
            Logger.exception("AccessKey '%s' has reached it's temporary device limit" % access_key)
            raise e
        except PicovoiceActivationRefusedError as e:
            Logger.exception("AccessKey '%s' refused" % access_key)
            raise e
        except PicovoiceActivationThrottledError as e:
            Logger.exception("AccessKey '%s' has been throttled" % access_key)
            raise e
        except PicovoiceError as e:
            Logger.exception("Failed to initialize Picovoice")
            raise e

    def wake_word_callback(self):
        Logger.info('[wake word]\n')

    def inference_callback(self, inference: Inference):
        if inference.is_understood:
            Logger.info(f'INFERENCE INTENT: {inference.intent}; slots: {inference.slots}')
            if inference.intent == 'playEpisode':
                season_str = inference.slots.get('season')
                episode_str = inference.slots.get('episode')

                season = w2n.word_to_num(season_str)
                episode = w2n.word_to_num(episode_str)

                Logger.info(f'PLAY INTENT: season {season}, episode {episode}')
                add_event(
                    BmoEvent(
                        'play_video',
                        {
                            'season': season,
                            'episode': episode,
                        }
                    )
                )
            elif inference.intent == 'pause':
                add_event(BmoEvent('pause', {}))
            elif inference.intent == 'play':
                add_event(BmoEvent('play_video', {}))
            elif inference.intent == 'stop':
                add_event(BmoEvent('stop', {}))
            elif inference.intent == 'playGame':
                add_event(BmoEvent('play_game', {'game': inference.slots.get('game')}))

        else:
            Logger.info("Didn't understand the command.\n")

    def listen(self):
        while True:
            pcm =self. recorder.read()
            self.picovoice.process(pcm)
        return True

    def shutdown(self):
        if self.recorder:
            self.recorder.delete()
        if self.picovoice:
            self.picovoice.delete()


def start_listening(root_path: str) -> Thread:
    th = Thread(target=_listening_thread, args=[root_path])
    th.setDaemon(True)

    th.start()
    return th


def _listening_thread(root_path: str):
    listener = SpeechListener(root_path=root_path)
    listener.listen()
