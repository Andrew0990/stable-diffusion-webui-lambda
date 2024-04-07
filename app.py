import os

# Define functions for common operations

def clone_repository(repo_url, target_dir):
    os.system(f"git clone {repo_url} {target_dir}")

def download_file(url, target_dir, output_filename):
    os.system(f"aria2c --console-log-level=error -c -x 16 -s 16 -k 1M {url} -d {target_dir} -o {output_filename}")

def execute_img2vid_model(input_image_path, output_video_path):
    os.system(f"python /home/demo/source/stable-video-diffusion-img2vid-xt/run.py {input_image_path} {output_video_path}")

# Main setup functions

def setup_extensions():
    extensions = [
        "deforum-for-automatic1111-webui",
        "sd-webui-infinite-image-browsing",
        "stable-diffusion-webui-huggingface",
        "sd-civitai-browser",
        "sd-webui-additional-networks",
        "sd-webui-controlnet",
        "openpose-editor",
        "sd-webui-depth-lib",
        "posex",
        "sd-webui-tunnels",
        "batchlinks-webui",
        "stable-diffusion-webui-catppuccin",
        "a1111-sd-webui-locon",
        "stable-diffusion-webui-rembg",
        "stable-diffusion-webui-two-shot",
        "SadTalker"
    ]
    for extension in extensions:
        clone_repository(f"https://github.com/camenduru/{extension}", f"/home/demo/source/stable-diffusion-webui/extensions/{extension}")

def download_controlnet_checkpoints():
    checkpoints = [
        "control_v11e_sd15_ip2p_fp16",
        "control_v11e_sd15_shuffle_fp16",
        "control_v11p_sd15_canny_fp16",
        "control_v11f1p_sd15_depth_fp16",
        # Add other checkpoints here
    ]
    for checkpoint in checkpoints:
        download_file(f"https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/{checkpoint}.safetensors", 
                      "/home/demo/source/stable-diffusion-webui/extensions/sd-webui-controlnet/models", 
                      f"{checkpoint}.safetensors")

def modify_shared_py():
    os.system("sed -i -e 's/\"sd_model_checkpoint\"\,/\"sd_model_checkpoint\,sd_vae\,CLIP_stop_at_last_layers\"\,/g' /home/demo/source/stable-diffusion-webui/modules/shared.py")

def launch_webui():
    os.system("python launch.py --port 8266 --listen --cors-allow-origins=* --xformers --enable-insecure-extension-access --theme dark --gradio-queue --disable-safe-unpickle --api --api-log")

if __name__ == "__main__":
    # Initial setup
    os.system("git lfs install")
    os.system("git clone -b v2.2 https://github.com/camenduru/stable-diffusion-webui /home/demo/source/stable-diffusion-webui")
    os.system("git clone https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt /home/demo/source/stable-video-diffusion-img2vid-xt")
    os.chdir("/home/demo/source/stable-video-diffusion-img2vid-xt")

    # Clone repositories and download necessary files
    clone_repository("https://huggingface.co/embed/negative", "/home/demo/source/stable-diffusion-webui/embeddings/negative")
    clone_repository("https://huggingface.co/embed/lora", "/home/demo/source/stable-diffusion-webui/models/Lora/positive")
    download_file("https://huggingface.co/embed/upscale/resolve/main/4x-UltraSharp.pth", 
                  "/home/demo/source/stable-diffusion-webui/models/ESRGAN", 
                  "4x-UltraSharp.pth")
    download_file("https://raw.githubusercontent.com/camenduru/stable-diffusion-webui-scripts/main/run_n_times.py", 
                  "/home/demo/source/stable-diffusion-webui/scripts", 
                  "run_n_times.py")
    
    setup_extensions()
    download_controlnet_checkpoints()
    modify_shared_py()

    # Execute the img2vid model to add image to video
    # Launch the web UI
    launch_webui()
