import os
from gradio_client import Client, handle_file
import folder_paths
import time


class MakeItAnimatableAutoRigger:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "model_path": ("STRING",),
                    "animation_path": ("STRING",)
                }
        }

    RETURN_TYPES = ("STRING",)

    RETURN_NAMES = ("rigged_model_path",)

    FUNCTION = "rig_model"

    OUTPUT_NODE = True

    CATEGORY = "api/3D"

    def rig_model(self, model_path, animation_path):
        uri = "http://localhost:7860"
        client = Client(uri)
        job = client.submit(
            progress=handle_file(os.path.join(folder_paths.get_output_directory(), model_path)), # input model
            param_2=True,           # no fingers
            param_3="T-pose",       # input rest pose
            param_4=[],             # input rest parts
            param_5=False,          # input is gaussian splats
            param_6=0.01,           # opacity threshold
            param_7=True,           # use normals to improve weights
            param_8=True,           # weight post-processing
            param_9="LeftArm",      # bone name for weights visualization
            param_10=True,          # reset to rest pose
            param_11=handle_file(animation_path), # input animation
            param_12=True,          # retarget animation to character
            param_13=True,          # animation in place (no movement)
            api_name="/pipeline"
        )
        while not job.done():
            time.sleep(0.1)

        gradio_path = job.outputs()[4][7]
        file_name = os.path.basename(gradio_path)
        output_path = os.path.join(folder_paths.get_output_directory(), f"rigged_{file_name}")
        os.rename(gradio_path, output_path)

        return (str(f"rigged_{file_name}"),)


NODE_CLASS_MAPPINGS = {
    "MakeItAnimatableAutoRigger": MakeItAnimatableAutoRigger
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MakeItAnimatableAutoRigger": "MakeItAnimatableAutoRigger"
}

