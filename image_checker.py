import imagehash

import numpy as np


def multi_hash_dist(one_hash, other_hash):
    # Get the hash distance for each region hash within cutoff
    distances = []
    for segment_hash in one_hash.segment_hashes:
        lowest_distance = min(
            (segment_hash.hash == other_segment_hash.hash).mean()
            for other_segment_hash in other_hash.segment_hashes
        )
        distances.append(lowest_distance)
    distance = 1 - (min(distances) - .5) * 2
    np.clip(distance, a_min=0, a_max=1)
    return distance


class ImageChecker:
    hash_func_dict = {
        'ahash': imagehash.average_hash,
        'phash': imagehash.phash,
        'dhash': imagehash.dhash,
        'whash_haar': imagehash.whash,
        'whash_db4': lambda img: imagehash.whash(img, mode='db4'),
        'colorhash': imagehash.colorhash,
        'crop_resistant': imagehash.crop_resistant_hash,
    }

    def __init__(self):
        self.hash_dict = {
            hash_name: {} for hash_name in self.hash_func_dict
        }

    def _get_hash_distance(self, hash1, hash2):
        if type(hash1) != imagehash.ImageMultiHash:
            return 1 - np.clip(((hash1.hash == hash2.hash).mean() - .5) * 2, a_min=0, a_max=1)
        return multi_hash_dist(hash1, hash2)

    def check_image_is_new(self, image, hash_types=None):
        if hash_types is None:
            hash_types = self.hash_func_dict.keys()
        status = True
        log_message = ""
        for hash_type in hash_types:
            hash = self.hash_func_dict[hash_type](image)
            if type(hash) != imagehash.ImageMultiHash:
                if hash in self.hash_dict[hash_type]:
                    status = False
                    log_message += f"hash collision on type {hash_type} with {self.hash_dict[hash_type][hash]}\n"
            else:
                for ref_hash in self.hash_dict[hash_type]:
                    if hash.matches(ref_hash):
                        status = False
                        log_message += f"hash collision on type {hash_type} with {self.hash_dict[hash_type][ref_hash]}\n"
        return status, log_message

    def find_closest_distance(self, image, hash_types=None):
        if hash_types is None:
            hash_types = self.hash_func_dict.keys()
        min_distance = 2
        for hash_type in hash_types:
            hash = self.hash_func_dict[hash_type](image)
            for ref_hash in self.hash_dict[hash_type].keys():
                distance = self._get_hash_distance(hash, ref_hash)
                min_distance = min(min_distance, distance)
        return min_distance

    def register_new_image(self, image, description, hash_types=None):
        if hash_types is None:
            hash_types = self.hash_func_dict.keys()
        for hash_type in hash_types:
            hash = self.hash_func_dict[hash_type](image)
            message = description
            if hash in self.hash_dict[hash_type]:
                message = self.hash_dict[hash_type][hash] + ' & ' + description
            self.hash_dict[hash_type][hash] = message

    def get_image_score(self, image):
        return self.find_closest_distance(image)

