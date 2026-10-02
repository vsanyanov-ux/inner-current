import os
import subprocess
from pathlib import Path

BASE_DIR = Path(r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\content\ukulele_shorts")
AUDIO_DIR = BASE_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "exports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ASS_PATH = BASE_DIR / "subtitles.ass"

# Get exact duration of each audio scene
scene_durations = []
for i in range(1, 7):
    fpath = AUDIO_DIR / f"scene{i}.mp3"
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
    "Title: Ukulele of Consciousness",
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
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    f"Dialogue: 0,{fmt(time_points[0])},{fmt(time_points[1])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H00D7FF&}}СКОЛЬКО ВЕСИТ ДУША?{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[1])},{fmt(time_points[2])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H34D399&}}ОШИБКА 2500 ЛЕТ{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[2])},{fmt(time_points[3])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H00D7FF&}}СМОТРИ НА ПАЛЬЦАХ{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[3])},{fmt(time_points[4])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H4141FF&}}МЁРТВАЯ ХВАТКА ЭГО{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[4])},{fmt(time_points[5])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H34D399&}}ТОК = РЕЗОНАНС{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[5])},{fmt(time_points[6])},Header,,0,0,0,,{{\\an8\\bord6\\shad3\\c&H00D7FF&}}НАСТРОЙ СВОЙ ТОК{{\\c&HFFFFFF&}}",
    "",
    f"Dialogue: 0,{fmt(time_points[0] + 0.1)},{fmt(time_points[0] + 5.5)},Subtitle,,0,0,0,,Ученые веками спорят,\\N{{\\c&H00D7FF&}}СКОЛЬКО ВЕСИТ ДУША?{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[0] + 5.5)},{fmt(time_points[1] - 0.1)},SubtitleGold,,0,0,0,,Укулеле — 400 граммов.\\NА музыка — {{\\c&H34D399&}}НОЛЬ ГРАММОВ!{{\\c&HFFFFFF&}}",
    "",
    f"Dialogue: 0,{fmt(time_points[1] + 0.1)},{fmt(time_points[1] + 5.0)},Subtitle,,0,0,0,,Две с половиной тысячи лет споров:\\Nчто первично — {{\\c&H00D7FF&}}МАТЕРИЯ ИЛИ ДУХ?{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[1] + 5.0)},{fmt(time_points[2] - 0.1)},SubtitleGreen,,0,0,0,,Но на самом деле\\Nникакой {{\\c&H34D399&}}ЗАГАДКИ НЕТ!{{\\c&HFFFFFF&}}",
    "",
    f"Dialogue: 0,{fmt(time_points[2] + 0.1)},{fmt(time_points[2] + 6.0)},Subtitle,,0,0,0,,Смотри на пальцах: материя — это {{\\c&H00D7FF&}}КОРПУС,{{\\c&HFFFFFF&}}\\Nа дух — его {{\\c&H34D399&}}ЗВУЧАНИЕ!{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[2] + 6.0)},{fmt(time_points[3] - 0.1)},SubtitleGold,,0,0,0,,Музыка не «вселяется» в дерево.\\NДух — это {{\\c&H00D7FF&}}ЧИСТЫЙ ЗВУК МАТЕРИИ!{{\\c&HFFFFFF&}}",
    "",
    f"Dialogue: 0,{fmt(time_points[3] + 0.1)},{fmt(time_points[3] + 6.0)},Subtitle,,0,0,0,,Почему люди выгорают?\\NВцепляются в контроль {{\\c&H4141FF&}}МЁРТВОЙ ХВАТКОЙ!{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[3] + 6.0)},{fmt(time_points[4] - 0.1)},SubtitleGold,,0,0,0,,Пережал гриф — и вместо радости\\N{{\\c&H4141FF&}}ПОЛУЧАЕТСЯ СКРИП И БОЛЬ!{{\\c&HFFFFFF&}}",
    "",
    f"Dialogue: 0,{fmt(time_points[4] + 0.1)},{fmt(time_points[4] + 4.5)},SubtitleGreen,,0,0,0,,Всё, что нужно —\\N{{\\c&H34D399&}}ОТПУСТИТЬ ЗАЖИМ!{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[4] + 4.5)},{fmt(time_points[5] - 0.1)},Subtitle,,0,0,0,,Живот расслаблен, руки свободны —\\Nток радости от {{\\c&H00D7FF&}}ЛЁГКОГО КАСАНИЯ!{{\\c&HFFFFFF&}}",
    "",
    f"Dialogue: 0,{fmt(time_points[5] + 0.1)},{fmt(time_points[5] + 4.5)},Subtitle,,0,0,0,,Твоё тело — это инструмент.\\N{{\\c&H34D399&}}НАУЧИСЬ ЗВУЧАТЬ!{{\\c&HFFFFFF&}}",
    f"Dialogue: 0,{fmt(time_points[5] + 4.5)},{fmt(time_points[6] - 0.1)},SubtitleGold,,0,0,0,,Подпишись на канал, чтобы\\N{{\\c&H00D7FF&}}НАСТРОИТЬ ВНУТРЕННИЙ ТОК!{{\\c&HFFFFFF&}}"
]

with open(ASS_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Generated subtitles ASS: {ASS_PATH}")

# Audio mix and concat with adelay & loudnorm
delays = [int(tp * 1000) for tp in time_points[:-1]]
inputs = []
filter_inputs = []
for i in range(1, 7):
    inputs.extend(["-i", str(AUDIO_DIR / f"scene{i}.mp3")])
    filter_inputs.append(f"[{i-1}:a]adelay={delays[i-1]}|{delays[i-1]}[v{i}];")

mix_filter = "".join(filter_inputs) + "".join([f"[v{i}]" for i in range(1, 7)]) + f"amix=inputs=6:normalize=0:duration=longest[amixed];[amixed]loudnorm=I=-14:TP=-1.0:LRA=7[aout]"

out_audio = OUTPUT_DIR / "ukulele_full_voiceover_lufs14.m4a"

cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", mix_filter, "-map", "[aout]", "-c:a", "aac", "-b:a", "192k", str(out_audio)]
print("Running ffmpeg audio mix...")
subprocess.run(cmd, check=True)
print(f"Full mixed voiceover saved to: {out_audio}")
