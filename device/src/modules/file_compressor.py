import zlib
import gzip
import bz2
import lzma
import zipfile
import tarfile
import shutil
import subprocess

import time
import os

from utils import ZIP_PATH, RAW_PATH, LOGS_PATH


def compress_file(filepath):
    file_name = os.path.basename(filepath)
    file_dir = os.path.dirname(filepath)
    original_size = os.path.getsize(filepath)

    compression_results = []

    # Compress using zlib
    try:
        start = time.time()
        with open(filepath, "rb") as f_in:
            original_data = f_in.read()
            compressed_data = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)
        end = time.time()
        duration = end - start
        compressed_size = len(compressed_data)
        compress_ratio = (original_size - compressed_size) / original_size
        with open(os.path.join(file_dir, file_name + ".zlib"), "wb") as f_out:
            f_out.write(compressed_data)
        compression_results.append(
            ("zlib", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using gzip
    try:
        start = time.time()
        with open(filepath, "rb") as f_in:
            with gzip.open(os.path.join(file_dir, file_name + ".gz"), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(os.path.join(file_dir, file_name + ".gz"))
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("gzip", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using bz2
    try:
        start = time.time()
        with open(filepath, "rb") as f_in:
            with bz2.open(os.path.join(file_dir, file_name + ".bz2"), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(os.path.join(file_dir, file_name + ".bz2"))
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("bz2", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using lzma
    try:
        start = time.time()
        with open(filepath, "rb") as f_in:
            with lzma.open(os.path.join(file_dir, file_name + ".xz"), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(os.path.join(file_dir, file_name + ".xz"))
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("lzma", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using zipfile
    try:
        start = time.time()
        with zipfile.ZipFile(
            os.path.join(file_dir, file_name + ".zip"), "w", zipfile.ZIP_DEFLATED
        ) as zipf:
            zipf.write(filepath, arcname=file_name)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(os.path.join(file_dir, file_name + ".zip"))
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("zipfile", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using tarfile with gzip
    try:
        start = time.time()
        with tarfile.open(
            os.path.join(file_dir, file_name + ".tar.gz"), "w:gz"
        ) as tarf:
            tarf.add(filepath, arcname=file_name)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(os.path.join(file_dir, file_name + ".tar.gz"))
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("tar.gz", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using tarfile with bz2
    try:
        start = time.time()
        with tarfile.open(
            os.path.join(file_dir, file_name + ".tar.bz2"), "w:bz2"
        ) as tarf:
            tarf.add(filepath, arcname=file_name)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(
            os.path.join(file_dir, file_name + ".tar.bz2")
        )
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("tar.bz2", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Compress using tarfile with lzma
    try:
        start = time.time()
        with tarfile.open(
            os.path.join(file_dir, file_name + ".tar.xz"), "w:xz"
        ) as tarf:
            tarf.add(filepath, arcname=file_name)
        end = time.time()
        duration = end - start
        compressed_size = os.path.getsize(os.path.join(file_dir, file_name + ".tar.xz"))
        compress_ratio = (original_size - compressed_size) / original_size
        compression_results.append(
            ("tar.xz", duration, compress_ratio, original_size, compressed_size)
        )
    except Exception as e:
        print(e)

    # Print results
    for (
        method,
        duration,
        compress_ratio,
        original_size,
        compressed_size,
    ) in compression_results:
        print(
            f"{method} - Tempo: {duration:.2f}s, Compressão: {compress_ratio:.2%}, Tamanho Original: {original_size} bytes, Tamanho Comprimido: {compressed_size} bytes"
        )


def _test_compressors(filepath):
    file_name = os.path.basename(filepath)
    file_dir = os.path.dirname(filepath)

    # Compress using zlib
    start = time()
    try:
        with open(filepath, "rb") as f_in:
            with open(os.path.join(file_dir, file_name + ".zlib"), "wb") as f_out:
                f_out.write(zlib.compress(f_in.read()))
    except Exception as e:
        print(e)
    end = time()
    print(f"Zlib - Tempo: {end - start:.2f}s")

    # Compress using gzip
    try:
        with open(filepath, "rb") as f_in:
            with gzip.open(os.path.join(file_dir, file_name + ".gz"), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(e)

    # Compress using bz2
    start = time()
    try:
        with open(filepath, "rb") as f_in:
            with bz2.open(os.path.join(file_dir, file_name + ".bz2"), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(e)
    end = time()
    print(f"Bz2 - Tempo: {end - start:.2f}s")

    # Compress using lzma
    start = time()
    try:
        with open(filepath, "rb") as f_in:
            with lzma.open(os.path.join(file_dir, file_name + ".xz"), "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        print(e)
    end = time()
    print(f"Lzma - Tempo: {end - start:.2f}s")

    # Compress using zipfile
    start = time()
    try:
        with zipfile.ZipFile(
            os.path.join(file_dir, file_name + ".zip"), "w", zipfile.ZIP_DEFLATED
        ) as zipf:
            zipf.write(filepath, arcname=file_name)
    except Exception as e:
        print(e)
    end = time()
    print(f"Zipfile - Tempo: {end - start:.2f}s")

    # Compress using tarfile with gzip
    start = time()
    try:
        with tarfile.open(
            os.path.join(file_dir, file_name + ".tar.gz"), "w:gz"
        ) as tarf:
            tarf.add(filepath, arcname=file_name)
    except Exception as e:
        print(e)
    end = time()
    print(f"Tar.gz - Tempo: {end - start:.2f}s")

    # Compress using tarfile with bz2
    start = time()
    try:
        with tarfile.open(
            os.path.join(file_dir, file_name + ".tar.bz2"), "w:bz2"
        ) as tarf:
            tarf.add(filepath, arcname=file_name)
    except Exception as e:
        print(e)
    end = time()
    print(f"Tar.bz2 - Tempo: {end - start:.2f}s")

    # Compress using tarfile with lzma
    start = time()
    try:
        with tarfile.open(
            os.path.join(file_dir, file_name + ".tar.xz"), "w:xz"
        ) as tarf:
            tarf.add(filepath, arcname=file_name)
    except Exception as e:
        print(e)
    end = time()
    print(f"Tar.xz - Tempo: {end - start:.2f}s")

    # # zlib
    # start = time()
    # original_data = open(filepath, "rb").read()
    # compressed_file = zlib.compress(original_data, zlib.Z_BEST_COMPRESSION)
    # end = time()
    # compress_ratio = (float(len(original_data)) - float(len(compressed_file))) / float(
    #     len(original_data)
    # )
    # duration = end - start
    # print(f"Zlib - Tempo: {duration:.2f}s")
    # print(f"Compress ratio: {compress_ratio:.2f}")


def _get_file():
    for file in os.listdir(RAW_PATH):
        if file.endswith(".raw"):
            return file
    return None


if __name__ == "__main__":
    file = _get_file()
    if file:
        filepath = os.path.join(RAW_PATH, file)
        print(f"File: {filepath}")
        # _test_compressors(filepath)
        compress_file(filepath)
    else:
        print("No file found")
