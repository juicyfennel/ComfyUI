import hashlib
import struct
import comfy.utils
import time
import os
import folder_paths


class SaveFileWebsocket:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "file_path": ("STRING",),
                    "chunk_size": ("INT", {"default": 65536, "min": 0, "max": 1073741824})
                }
        }

    RETURN_TYPES = ("STRING","STRING",)

    RETURN_NAMES = ("sha256","file_type",)

    FUNCTION = "save_file"

    OUTPUT_NODE = True

    CATEGORY = "api/util"

    def save_file(self, file_path, chunk_size=65536):
        full_path = os.path.join(folder_paths.get_output_directory(), file_path)
        print(full_path)
        file_type = os.path.splitext(file_path)[1]
        with open(full_path, "rb") as f:
            bytes = f.read()
        num_chunks = len(bytes) // chunk_size
        sha256 = hashlib.sha256(bytes).hexdigest()
        pbar = comfy.utils.ProgressBar(num_chunks)
        step = 0
        for i in range(0, len(bytes), chunk_size):
            chunk = bytes[i:i+chunk_size]
            part = struct.pack(">I", step)
            total = struct.pack(">I", num_chunks)
            message = bytearray(part)
            message.extend(total)
            message.extend(chunk)
            pbar.update_absolute(step, num_chunks, message)
            step += 1

        return {"ui": {"sha256": [sha256], "file_type": [file_type]}, "result": sha256}

    @classmethod
    def IS_CHANGED(s, file_path, chunk_size):
        return time.time()

NODE_CLASS_MAPPINGS = {
    "SaveFileWebsocket": SaveFileWebsocket
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveFileWebsocket": "SaveFileWebsocket"
}

