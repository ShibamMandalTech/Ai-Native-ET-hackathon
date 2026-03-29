from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from config import VIDEO_WIDTH, VIDEO_HEIGHT

def create_video(image_paths, audio_path, news_id):
    output_path = f"output/videos/{news_id}.mp4"

    audio = AudioFileClip(audio_path)
    duration = audio.duration / len(image_paths)

    clips = []
    for img in image_paths:
        clip = (
            ImageClip(img)
            .with_duration(duration)
            .resized((VIDEO_WIDTH, VIDEO_HEIGHT))
        )
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    video = video.with_audio(audio)

    video.write_videofile(output_path, fps=30)

    return output_path