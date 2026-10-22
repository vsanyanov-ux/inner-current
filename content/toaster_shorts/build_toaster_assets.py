import os
import subprocess
from pathlib import Path

BASE_DIR = Path(r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\content\toaster_shorts")
AUDIO_DIR = BASE_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "exports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ASS_PATH = BASE_DIR / "subtitles.ass"

# Get exact duration of each audio scene
scene_durations = []
for i in range(1, 7):
    fpath = AUDIO_DIR / f"scene{i}.mp3"
    if not fpath.exists():
        print(f"Waiting for {fpath}...")
        exit(1)
    res = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(fpath)
    ]).decode().strip()
    scene_durations.append(float(res))

print("Scene durations:", [round(d, 2) for d in scene_durations])

# Calculate start and end offsets with small padding
time_points = [0.0]
for d in scene_durations:
    time_points.append(time_points[-1] + d + 0.3)

def fmt(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    cs = int((sec - int(sec)) * 100)
    return f"0:{m:02d}:{s:02d}.{cs:02d}"

lines = [
    "[Script Info]",
    "Title: Toaster and Socket Metaphor Shorts",
    "ScriptType: v4.00+",
    "WrapStyle: 0",
    "ScaledBorderAndShadow: yes",
    "YCbCr Matrix: TV.601",
    "PlayResX: 1080",
    "PlayResY: 1920",
    "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Header,Arial,58,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,8,40,40,140,1",
    "Style: Subtitle,Arial,64,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,7,3,2,60,60,420,1",
    "Style: SubtitleGold,Arial,66,&H0000D7FF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,8,4,2,60,60,420,1",
    "Style: SubtitleGreen,Arial,66,&H0099D334,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,8,4,2,60,60,420,1",
    "Style: SubtitleRed,Arial,66,&H004141FF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,8,4,2,60,60,420,1",
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    f"Dialogue: 0,{fmt(time_points[0])},{fmt(time_points[1])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H00D7FF&}}«У МЕНЯ ЖЕ ЕСТЬ РАФ!»{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[1])},{fmt(time_points[2])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H4141FF&}}ВЫБИЛО ПРОБКИ?{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[2])},{fmt(time_points[3])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H4141FF&}}ТОКА НЕТ В СЕТИ{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[3])},{fmt(time_points[4])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H34D399&}}В ЧЁМ СЕКРЕТ?{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[4])},{fmt(time_points[5])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H00D7FF&}}СВЕРХПРОВОДИМОСТЬ{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[5])},{fmt(time_points[6])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H00D7FF&}}ВКЛЮЧИ СВОЙ ТОК{{\\c&HFFFFFF&}}",
    "",
    # Scene 1 subtitles
    f"Dialogue: 0,{fmt(time_points[0] + 0.1)},{fmt(time_points[0] + 4.2)},Subtitle,,0,0,0,,Человек защищается списком радостей:\\N«У меня же есть раф, море, шопинг!»",
    f"Dialogue: 0,{fmt(time_points[0] + 4.2)},{fmt(time_points[1] - 0.1)},SubtitleGold,,0,0,0,,Но твой раф или отпуск —\\Nэто {{\\c&H00D7FF&}}ПРОСТО КРУТОЙ ТОСТЕР!{{\\c&HFFFFFF&}}",
    "",
    # Scene 2 subtitles
    f"Dialogue: 0,{fmt(time_points[1] + 0.1)},{fmt(time_points[1] + 3.8)},Subtitle,,0,0,0,,Если в розетке нет тока\\Nили выбило пробки —",
    f"Dialogue: 0,{fmt(time_points[1] + 3.8)},{fmt(time_points[2] - 0.1)},SubtitleRed,,0,0,0,,Сколько тостеров ни тыкай,\\N{{\\c&H4141FF&}}ХЛЕБ ОСТАНЕТСЯ СЫРЫМ!{{\\c&HFFFFFF&}}",
    "",
    # Scene 3 subtitles
    f"Dialogue: 0,{fmt(time_points[2] + 0.1)},{fmt(time_points[2] + 4.0)},Subtitle,,0,0,0,,Если проводка сожжена тревогой\\Nи зажимом эго —",
    f"Dialogue: 0,{fmt(time_points[2] + 4.0)},{fmt(time_points[3] - 0.1)},SubtitleRed,,0,0,0,,Самый дорогой раф на пляже\\N{{\\c&H4141FF&}}ВСТАЁТ СУХИМ КОМОМ В ГОРЛЕ!{{\\c&HFFFFFF&}}",
    "",
    # Scene 4 subtitles
    f"Dialogue: 0,{fmt(time_points[3] + 0.1)},{fmt(time_points[3] + 4.0)},SubtitleGreen,,0,0,0,,Внутренний ток — это {{\\c&H34D399&}}ЭЛЕКТРИЧЕСТВО!{{\\c&HFFFFFF&}}\\NУдовольствия — лишь приборы.",
    f"Dialogue: 0,{fmt(time_points[3] + 4.0)},{fmt(time_points[4] - 0.1)},SubtitleGold,,0,0,0,,Источник счастья —\\N{{\\c&H00D7FF&}}В НАПРЯЖЕНИИ ТВОЕЙ СЕТИ!{{\\c&HFFFFFF&}}",
    "",
    # Scene 5 subtitles
    f"Dialogue: 0,{fmt(time_points[4] + 0.1)},{fmt(time_points[4] + 3.0)},Subtitle,,0,0,0,,Когда ток течёт чисто —",
    f"Dialogue: 0,{fmt(time_points[4] + 3.0)},{fmt(time_points[5] - 0.1)},SubtitleGold,,0,0,0,,Даже кусок чёрного хлеба с водой\\N{{\\c&H00D7FF&}}ДАЁТ ВОСТОРГ БЫТИЯ!{{\\c&HFFFFFF&}}",
    "",
    # Scene 6 subtitles
    f"Dialogue: 0,{fmt(time_points[5] + 0.1)},{fmt(time_points[5] + 3.5)},SubtitleGreen,,0,0,0,,Перестань скупать тостеры.\\N{{\\c&H34D399&}}ВКЛЮЧИ ТОК В РОЗЕТКЕ!{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[5] + 3.5)},{fmt(time_points[6] - 0.1)},SubtitleGold,,0,0,0,,Подпишись на канал, чтобы\\N{{\\c&H00D7FF&}}НАСТРОИТЬ ВНУТРЕННИЙ ТОК!{{\\c&HFFFFFF&}}"
]

ASS_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"[OK] Generated dynamic ASS subtitles: {ASS_PATH}")

# Concatenate all voiceovers with FFmpeg loudnorm -14 LUFS
audio_inputs = []
delays = []
filter_parts = []

current_ms = 200
for i in range(1, 7):
    audio_inputs.extend(["-i", str(AUDIO_DIR / f"scene{i}.mp3")])
    filter_parts.append(f"[{i-1}:a]adelay={int(current_ms)}|{int(current_ms)}[v{i}];")
    current_ms += (scene_durations[i-1] + 0.3) * 1000

mix_inputs = "".join([f"[v{i}]" for i in range(1, 7)])
filter_complex = "".join(filter_parts) + f"{mix_inputs}amix=inputs=6:normalize=0[amixed];[amixed]loudnorm=I=-14:TP=-1.0:LRA=7[aout]"

out_m4a = OUTPUT_DIR / "toaster_full_voiceover_lufs14.m4a"
cmd = [
    "ffmpeg", "-y",
    *audio_inputs,
    "-filter_complex", filter_complex,
    "-map", "[aout]",
    "-c:a", "aac", "-b:a", "192k",
    str(out_m4a)
]

print("Running FFmpeg audio mix and Loudnorm normalization...")
subprocess.run(cmd, check=True)
print(f"[OK] Master voiceover generated: {out_m4a}")
print(f"Total duration: {round(current_ms / 1000, 2)} seconds")
