import hashlib
import os
import shutil
from pathlib import Path

BLOCKSIZE = 65536


def hash_file(path: Path):
    hasher = hashlib.sha1()
    with path.open("rb") as _file:
        buf = _file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = _file.read(BLOCKSIZE)
    return hasher.hexdigest()


def sync(src, dst):
    source_hashes = {}
    for folder, _, files in os.walk(src):
        for file_name in files:
            source_path = Path(folder) / file_name
            source_hash = hash_file(source_path)
            source_hashes[source_hash] = file_name

    seen = set()

    for folder, _, files in os.walk(dst):
        for file_name in files:
            dest_path = Path(folder) / file_name
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            if dest_hash not in source_hashes:
                dest_path.unlink()
            elif dest_hash in source_hashes and file_name != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(dst) / source_hashes[dest_hash])

    for source_hash, file_name in source_hashes.items():
        if source_hash not in seen:
            shutil.copy(Path(src) / file_name, Path(dst) / file_name)
