import os
import subprocess
import sys

# Import nessesary libraries
try:
    import gradio as gr
    import ffmpeg
    from pytube import YouTube as yt
    from moviepy.editor import VideoFileClip
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ffmpeg"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pytube"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
    import ffmpeg
    from pytube import YouTube as yt
    import gradio as gr
    from moviepy.editor import VideoFileClip


def clean_folder(folder, filetype=None):
    for path, directories, files in os.walk(folder):
        for file in files:
            if filetype:
                if file.endswith(filetype):
                    os.remove(os.path.join(path, file))
            else:
                os.remove(os.path.join(path, file))


def convert_mp3(mp4_file):
    """
    Converts mp4 to mp3 file.
    Inputs:
        mp4_file (str) : path to the .mp4 file 
    Returns :
        mp3_filepath (str) : converted .mp3 file filepath
    """
    clip = VideoFileClip(mp4_file)

    mp3_filepath = mp4_file[:-4] + ".mp3"
    clip.audio.write_audiofile(mp3_filepath)

    return mp3_filepath


def download_youtube_video(url, output_folder):
    """
    Downloads video from the giving url
    Inputs:
        url (str): video url to download
        output_folder (str): folder path to download
    Returns:
        downloaded_vid (str): downloaded video's filepath
    """
    youtube_video = yt(url)
    hd_stream = youtube_video.streams.get_highest_resolution()
    downloaded_vid = hd_stream.download(output_folder)

    return downloaded_vid


def simple_download(url_paths, dl_path=None, convert_to_mp3=False):
    """ 
    Downloads youtube max available quality video to the giving path
    and returns it's path
    """
    downloaded_videos = []
    downloaded_audios = []
    if not dl_path:
        dl_path = ""
    # clean_folder(dl_path)
    
    urls = url_paths.split("\n")
    for url in urls:
        
        # Download videos and store their paths
        mp4_filepath = download_youtube_video(url, dl_path)
        downloaded_videos.append(mp4_filepath)

        # Convert video to mp3 if needed
        if convert_to_mp3:
            print(type(mp4_filepath))
            mp3_file = convert_mp3(mp4_filepath)
            downloaded_audios.append(mp3_file)

    return [downloaded_videos, downloaded_audios]


with gr.Blocks() as downloader:
    
    input_link = gr.Textbox(label="YouTube links", placeholder="copy youtube link here", value="https://youtu.be/dQw4w9WgXcQ")
    checkbox_convert_to_mp3 = gr.Checkbox(label="Create .mp3 files from videos" )
    download_path = gr.Textbox(label="Path to Download")
    output_vids = gr.Files(label="Downloaded videos", visible=True)
    output_audios = gr.Files(label="Downloaded audios", visible=True)

    download_btn = gr.Button("Download")
    download_btn.click(fn=simple_download, inputs=[input_link, download_path, checkbox_convert_to_mp3], outputs=[output_vids, output_audios])

downloader.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
