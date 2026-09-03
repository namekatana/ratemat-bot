from aiogram.fsm.state import State, StatesGroup


class ProfileForm(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()
    description = State()


class FeedForm(StatesGroup):
    viewing = State()
    complaint_reason = State()
