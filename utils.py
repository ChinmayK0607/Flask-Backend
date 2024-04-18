from string import ascii_letters
import random
from queue import Queue

def generate_room_code(length: int, existing_codes: list[str]) -> str:
    while True:
        code_chars = [random.choice(ascii_letters) for _ in range(length)]
        code = ''.join(code_chars)

        if code not in existing_codes:
            return code

def find_room(room_code:str, room_queue: dict) -> int:
    for id in range(len(room_queue)):
        if str(room_queue[id]) == room_code:
            return id

def init_room_queues(ROOMS: list, room_queue: dict):
    for room in ROOMS:
        room_name = Queue()
        room_queue[room] = room_name


