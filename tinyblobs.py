import os
import json
import io
import pickle

DEFAULT_BUFFER_SIZE = 1024 * 4

class StringStreamBase(object):
    def readString(self, *args, format='utf-8', **argz):
        return self.read(*args, **argz).decode(format)

    def writeString(self, data, *args, format='utf-8', **argz):
        return self.write(data.encode(format), *args, **argz)

class JsonStreamBase(StringStreamBase):
    def readJSON(self, buffersize=DEFAULT_BUFFER_SIZE):
        original_file_position = self.tell()
        decoder = json.JSONDecoder(strict=False)
        buffer = ''

        for block in iter(lambda: self.readString(buffersize), ''):
            buffer += block
            try:
                result, index = decoder.raw_decode(buffer)
                self.seek(index - len(buffer), SEEK_CUR)
            except ValueError as e: pass

        self.seek(original_file_position)
        return None

    def iterJSON(self, buffersize=DEFAULT_BUFFER_SIZE):
        decoder = json.JSONDecoder(strict=False)
        buffer = ''
        for block in iter(lambda: self.readString(buffersize), ''):
            buffer += block
            try:
                while True:
                    result, index = decoder.raw_decode(buffer)
                    buffer = buffer[index:]
                    yield result
            except ValueError as e: pass

    def writeJSON(self, object):
        self.writeString(json.dumps(object))


try:
    import gzip
    class GzipDataStream(JsonStreamBase, gzip.GzipFile):
        pass
except ImportError: pass

try:
    import lzma
    class LzmaDataStream(JsonStreamBase, lzma.LZMAFile):
        pass
except ImportError: pass

try:
    import bz2
    class BZ2DataStream(JsonStreamBase, bz2.BZ2File):
        pass
except ImportError: pass

class SimpleDataStream(JsonStreamBase, io.FileIO):
    pass

def open_stream(filename, mode, *args, **argz):
    ext = os.path.splitext(filename)[-1].lower()
    if ext == '.gz':
        return GzipDataStream(filename, mode, *args, **argz)
    elif ext == '.lzma':
        return LzmaDataStream(filename, mode, *args, **argz)
    elif ext == '.bz2':
        return BZ2DataStream(filename, mode, *args, **argz)
    else:
        return SimpleDataStream(filename, mode, *args, **argz)
