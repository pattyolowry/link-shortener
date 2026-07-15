import os
from .redis import redis_client

SHARD_BITS = 14
SEQUENCE_BITS = 50

MAX_SHARD_ID = (1 << SHARD_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1

BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

class ShortIDGenerator:
    def __init__(self):
        self.shard_id = int(os.getenv("SHARD_ID", None))
        self.redis = redis_client
        self.redis_counter_key = f"shortener:shard:{self.shard_id}:sequence"

    def get_new_id(self) -> int:
        sequence = self.redis.incrby(self.redis_counter_key, 1)
        #unique_id = (self.shard_id << SEQUENCE_BITS) | (sequence)
        unique_id = (sequence << SHARD_BITS) | self.shard_id
        return self._base62_encode(unique_id)
    
    def _base62_encode(self, number: int) -> str:
        if number < 0:
            raise ValueError("Base62 encoding only supports non-negative integers")

        if number == 0:
            return BASE62_ALPHABET[0]

        base = len(BASE62_ALPHABET)
        chars = []

        while number > 0:
            number, remainder = divmod(number, base)
            chars.append(BASE62_ALPHABET[remainder])

        return "".join(reversed(chars))

