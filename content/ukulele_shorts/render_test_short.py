import os
import subprocess
from pathlib import Path

BASE_DIR = Path(r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\content\ukulele_shorts")
EXPORTS_DIR = BASE_DIR / "exports"
AUDIO_VOICE = EXPORTS_DIR / "ukulele_full_voiceover_lufs14.m4a"
BG_MUSIC = Path(r"c:\Users\vanya\Antigravity Projects\Misc\YouTube Single Tax\assets\audio\ambient_bg.wav")
ASS_FILE = BASE_DIR / "subtitles.ass"
OUTPUT_VIDEO = EXPORTS_DIR / "Ukulele_Consciousness_Short_Test.mp4"

# Durations calculated in build_ukulele_assets:
# [12.01, 9.71, 14.75, 12.35, 9.78, 11.00]
scene_durations = [12.01, 9.71, 14.75, 12.35, 9.78, 11.00]
images = [
    EXPORTS_DIR / "scene1_keyframe.jpg",
    EXPORTS_DIR / "scene2_keyframe.jpg",
    EXPORTS_DIR / "scene3_keyframe.jpg",
    EXPORTS_DIR / "scene4_keyframe.jpg",
    EXPORTS_DIR / "scene5_keyframe.jpg",
    EXPORTS_DIR / "scene6_keyframe.jpg",
]

# Generate temporary video clips for each image
clip_files = []
for idx, (img, dur) in enumerate(zip(images, scene_durations), 1):
    clip_path = EXPORTS_DIR / f"clip_{idx}.mp4"
    clip_files.append(clip_path)
    print(f"Creating clip {idx} for {dur:.2f}s...")
    
    # Scale and pad to 1080x1920, 30fps
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-t", f"{dur:.2f}",
        "-i", str(img),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-r", "30",
        str(clip_path)
    ]
    subprocess.run(cmd, check=True)

# Create concat list
concat_list = EXPORTS_DIR / "concat_list.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for clip in clip_files:
        f.write(f"file '{clip.as_posix()}'\n")

# Mix voiceover with ambient background music
final_audio = EXPORTS_DIR / "final_mixed_soundtrack.m4a"
print("Mixing audio with background music...")
if BG_MUSIC.exists():
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(AUDIO_VOICE),
        "-stream_loop", "-1", "-i", str(BG_MUSIC),
        "-filter_complex", "[1:a]volume=0.10[bg];[0:a][bg]amix=inputs=2:duration=first[aout];[aout]loudnorm=I=-14:TP=-1.0:LRA=7[anorm]",
        "-map", "[anorm]",
        "-c:a", "aac", "-b:a", "192k",
        str(final_audio)
    ]
else:
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(AUDIO_VOICE),
        "-c:a", "copy",
        str(final_audio)
    ]
subprocess.run(cmd_audio, check=True)

# Final render: Concat clips + burn ASS subtitles + mux audio
print("Rendering final video with burned-in subtitles...")
ass_escaped = str(ASS_FILE).replace("\\", "/").replace(":", "\\:")

cmd_final = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", str(concat_list),
    "-i", str(final_audio),
    "-vf", f"subtitles='{ass_escaped}'",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "18",
    "-c:a", "copy",
    "-shortest",
    str(OUTPUT_VIDEO)
]
subprocess.run(cmd_final, check=True)
print(f"[OK] SUCCESS! Final video created at: {OUTPUT_VIDEO}")
