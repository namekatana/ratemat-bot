from aiogram.fsm.state import State, StatesGroup


class Verification(StatesGroup):
    awaiting_video_note = State()
