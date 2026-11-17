# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 18:38:22 2025

@author: 13221
"""
import os
from openai import OpenAI
import mimetypes
import subprocess
import torch
import whisper
import warnings


def transcribe_audio():
    def check_gpu():
        if torch.cuda.is_available():
            print(f"GPU is available: {torch.cuda.get_device_name(0)}")
        else:
            print("GPU is not available.")

    def check_device():
        return "cuda" if torch.cuda.is_available() else "cpu"

    warnings.simplefilter("ignore", UserWarning)
    check_gpu()
    device = check_device()
    print(f"Using device: {device}")
    model = whisper.load_model("turbo").to("cuda")
    result = model.transcribe(audio_file_path)
    if result["text"] is None:
        raise ValueError("Transcription failed, no result returned.")
    segments = result["segments"]
    time_text_list = []
    result = []
    for segment in segments:
        start_time = segment["start"]
        formatted_time = (
            f"{int((start_time % 3600) // 60):02}:{int(start_time % 60):02}"
        )
        text = segment["text"]
        time_text_list.append((formatted_time, text))
    for time, text in time_text_list:
        print(f"[{time}]{text}")
        result.append(f"[{time}]{text}")
    return result


def generate_notes(text):
    if text is None:
        raise ValueError("No text provided for note generation.")
    client = OpenAI(
        # Zhipu AI
        # Credentials must come from the process environment.
        # base_url="https://open.bigmodel.cn/api/paas/v4",
        #
        # Deepseek AI
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com",
    )
    prompt = (
        f"Write notes based on time and content (Markdown format, mark time): {text}"
    )

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


def main():
    video_to_audio()
    transcription_text = transcribe_audio()
    notes = generate_notes(transcription_text)
    print("Note: \n", notes)


def video_to_audio():
    global audio_file_path

    def is_video_file(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type and mime_type.startswith("video")

    if is_video_file(file_path):
        command = f"ffmpeg -y -i {file_path} -vn -acodec copy {cov_audio_file_path}"
        subprocess.run(command, shell=True)
        print(f"Conversion successful: {cov_audio_file_path}")
        audio_file_path = cov_audio_file_path
    else:
        print(f"{file_path} is not a video file and does not need to be converted.")
        audio_file_path = file_path

    print(audio_file_path)


file_path = r"test_video.mp4"
audio_file_path = r""
cov_audio_file_path = r"cov_audio.m4a"
# model_name="glm-4"
model_name = "deepseek-reasoner"
main()
