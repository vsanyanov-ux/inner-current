import asyncio
import os
import re
import sys
import json
import argparse
import subprocess
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')

VOICE = "ru-RU-DmitryNeural"
RATE = "-2%"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
BOOK_FILE = os.path.join(PROJECT_ROOT, "book_outline.md")
AUDIO_OUTPUT_DIR = os.path.join(CURRENT_DIR, "tracks")
PUBLIC_AUDIO_DIR = os.path.join(PROJECT_ROOT, "public", "audio")
COVER_PATH = os.path.join(PROJECT_ROOT, "public", "assets", "book_cover.jpg")
MANIFEST_FILE = os.path.join(PROJECT_ROOT, "public", "audio", "audiobook_manifest.json")

def sanitize_text_for_speech(raw_text: str) -> str:
    # 1. Strip code blocks (Mermaid, ASCII art, and scripts) line-by-line
    lines = raw_text.split('\n')
    clean_lines = []
    in_code = False
    for line in lines:
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        clean_lines.append(line)
    text = '\n'.join(clean_lines)

    # 2. Remove ASCII box-drawing characters, arrows, and geometric glyphs
    text = re.sub(r'[─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬▲▼►◄◆◇○●■□→←↑↓↔↕\\]', '', text)
    
    # 3. Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # 4. Clean obsidian callouts: > [!quote] Title
    text = re.sub(r'>\s*\[![^\]]+\][^\n]*', '', text)
    # Remove leading quote '>' marks
    text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)
    
    # Replace math formulas with spoken Russian
    replacements = [
        (r'\$Q\s*=\s*I\^2\s*R\s*t\$', 'закон Джоуля — Ленца: количество тепла Ку равно произведению квадрата силы тока на сопротивление и время'),
        (r'\$R_{\\text\{ego\}}\s*>\s*0\$', 'сопротивление эго больше нуля'),
        (r'\$R_{ego}\s*>\s*0\$', 'сопротивление эго больше нуля'),
        (r'\$R\s*\\to\s*0\$', 'сопротивление стремится к нулю'),
        (r'\$R\s*=\s*0\$', 'сопротивление равно нулю'),
        (r'\$R\s*>\s*0\$', 'сопротивление больше нуля'),
        (r'\$I\$', 'ток И'),
        (r'\$U\$', 'напряжение У'),
        (r'\$R\$', 'сопротивление Эр'),
        (r'\$M\s*>\s*0\$', 'взаимная индукция больше нуля'),
        (r'\\Delta v\s*=\s*v_e\s*\\ln\s*\\frac\{m_0\}\{m_f\}', 'дельта вэ равно скорости истечения газов, умноженной на натуральный логарифм отношения начальной массы к конечной'),
        (r'\$\\mathcal\{H\}\$', 'аш счастья'),
        (r'\$([^\$]+)\$', r'\1'), # fallback for remaining inline math
        (r'\$\$([^\$]+)\$\$', r'\1') # display math
    ]
    
    for pattern, rep in replacements:
        text = re.sub(pattern, rep, text)
        
    # Clean Markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Clean bold / italics
    text = re.sub(r'\*{1,3}([^\*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    
    # Clean headers markdown hashes
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    
    # Clean horizontal rules
    text = re.sub(r'^\s*[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    
    # Clean bullet points to natural speech pauses
    text = re.sub(r'^\s*[\*\-\+]\s+', '• ', text, flags=re.MULTILINE)
    
    # Normalize multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Accent helpers for speech
    text = text.replace('Тандэн', 'Тандэ́н').replace('тандэн', 'тандэ́н')
    text = text.replace('Мусин', 'Муси́н').replace('мусин', 'муси́н')
    text = text.replace('Дзансин', 'Дзанси́н').replace('дзансин', 'дзанси́н')
    text = text.replace('Кансо', 'Кансо́').replace('кансо', 'кансо́')
    
    return text.strip()

def split_text_into_chunks(text: str, max_chars: int = 1000) -> list[str]:
    """Splits long text by paragraphs and sentences so no chunk ever exceeds max_chars."""
    paragraphs = text.split('\n\n')
    units = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if len(p) <= max_chars:
            units.append(p)
        else:
            # Split long paragraph by sentences
            sentences = re.split(r'(?<=[.!?…])\s+', p)
            current_s = []
            current_s_len = 0
            for s in sentences:
                s = s.strip()
                if not s:
                    continue
                if current_s_len + len(s) + 1 > max_chars and current_s:
                    units.append(' '.join(current_s))
                    current_s = [s]
                    current_s_len = len(s)
                else:
                    current_s.append(s)
                    current_s_len += len(s) + 1
            if current_s:
                units.append(' '.join(current_s))

    chunks = []
    current_chunk = []
    current_len = 0
    for u in units:
        if current_len + len(u) + 2 > max_chars and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [u]
            current_len = len(u)
        else:
            current_chunk.append(u)
            current_len += len(u) + 2
            
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
        
    return chunks

def parse_book():
    with open(BOOK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track 0: Слово к русскому изданию
    word_ru_match = re.search(r'## 🏛️ СЛОВО К РУССКОМУ ИЗДАНИЮ(.*?)## Оглавление', content, re.DOTALL)
    word_ru_text = word_ru_match.group(1).strip() if word_ru_match else ""

    manifest_pos = content.find('## МАНИФЕСТ ДЗЕН-ИНЖЕНЕРА\n### От абстрактных сказок')
    if manifest_pos == -1:
        manifest_pos = content.find('## МАНИФЕСТ ДЗЕН-ИНЖЕНЕРА')
        
    book_body = content[manifest_pos:]
    pattern = r'(?=(?:^##\s+|^###\s+Глава\s+))'
    raw_sections = re.split(pattern, book_body, flags=re.MULTILINE)
    
    chapters = []
    
    # Add Track 0
    chapters.append({
        "track": 0,
        "title": "Слово к русскому изданию: Русский синтез",
        "clean_text": sanitize_text_for_speech("Слово к русскому изданию.\nРусский синтез: от омического ада к чертежу Циолковского.\n\n" + word_ru_text),
        "words": len(re.findall(r'\b\w+\b', word_ru_text))
    })
    
    track_num = 1
    for sec in raw_sections:
        sec = sec.strip()
        if not sec:
            continue
        first_line = sec.split('\n')[0].strip()
        title = re.sub(r'^#{1,3}\s+', '', first_line)
        clean_title = re.sub(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]', '', title).strip()
        body = '\n'.join(sec.split('\n')[1:]).strip()
        if len(body) < 100:
            continue
        words_count = len(re.findall(r'\b\w+\b', body))
        chapters.append({
            "track": track_num,
            "title": clean_title,
            "clean_text": sanitize_text_for_speech(sec),
            "words": words_count
        })
        track_num += 1
        
    return chapters

async def synthesize_chunk(text: str, output_path: str, max_retries: int = 5):
    for attempt in range(1, max_retries + 1):
        try:
            comm = edge_tts.Communicate(text, VOICE, rate=RATE)
            await asyncio.wait_for(comm.save(output_path), timeout=60.0)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                await asyncio.sleep(0.4) # polite delay between chunks
                return True
        except Exception as e:
            err_msg = repr(e) if not str(e) else str(e)
            print(f"      ⚠️ Попытка {attempt}/{max_retries} не удалась ({err_msg})")
            await asyncio.sleep(2.5 * attempt)
    raise RuntimeError(f"Не удалось синтезировать фрагмент после {max_retries} попыток.")

async def synthesize_track(chap: dict, total_tracks: int):
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    os.makedirs(PUBLIC_AUDIO_DIR, exist_ok=True)
    
    track_id = f"{chap['track']:02d}"
    slug = re.sub(r'[^\w\-_]', '_', chap['title'])[:30].strip('_')
    final_filename = f"{track_id}_{slug}.mp3"
    final_path = os.path.join(AUDIO_OUTPUT_DIR, final_filename)
    public_path = os.path.join(PUBLIC_AUDIO_DIR, final_filename)
    
    # Check if already generated
    if os.path.exists(final_path) and os.path.getsize(final_path) > 10000:
        print(f"[{track_id}/{total_tracks:02d}] Уже существует: {final_filename} ({os.path.getsize(final_path):,} байт)")
        if not os.path.exists(public_path):
            import shutil
            shutil.copy2(final_path, public_path)
        return final_path

    print(f"\n⚡ [{track_id}/{total_tracks:02d}] Генерация: {chap['title']} ({chap['words']:,} слов)...")
    
    chunks = split_text_into_chunks(chap['clean_text'])
    temp_files = []
    
    try:
        for idx, chunk in enumerate(chunks):
            temp_file = os.path.join(AUDIO_OUTPUT_DIR, f"temp_{track_id}_{idx}.mp3")
            print(f"   Синтез фрагмента {idx+1}/{len(chunks)} ({len(chunk):,} симв)...")
            await synthesize_chunk(chunk, temp_file)
            temp_files.append(temp_file)
            
        # Concat & Master via FFmpeg
        concat_txt = os.path.join(AUDIO_OUTPUT_DIR, f"concat_{track_id}.txt")
        with open(concat_txt, "w", encoding="utf-8") as f:
            for tf in temp_files:
                f.write(f"file '{os.path.abspath(tf)}'\n")
                
        raw_concat = os.path.join(AUDIO_OUTPUT_DIR, f"raw_{track_id}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", raw_concat
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Mastering with loudnorm & tags
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_concat,
        ]
        has_cover = os.path.exists(COVER_PATH)
        if has_cover:
            cmd.extend(["-i", COVER_PATH])

        cmd.extend([
            "-filter_complex", "[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[aout]"
        ])

        if has_cover:
            cmd.extend([
                "-map", "[aout]",
                "-map", "1:0",
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-c:v", "copy",
                "-id3v2_version", "3",
                "-metadata:s:v", 'title="Cover"',
                "-metadata:s:v", 'comment="Cover (front)"'
            ])
        else:
            cmd.extend([
                "-map", "[aout]",
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-id3v2_version", "3"
            ])

        cmd.extend([
            "-metadata", f"title={chap['title']}",
            "-metadata", "artist=Владимир Аньянов",
            "-metadata", "album_artist=Владимир Аньянов",
            "-metadata", "album=Внутренний ток: Архитектура счастья",
            "-metadata", "composer=Владимир Аньянов",
            "-metadata", f"track={chap['track']:02d}/{total_tracks:02d}",
            "-metadata", "genre=Audiobook",
            "-metadata", "date=2026",
            "-metadata", "comment=Официальная аудиокнига «Внутренний ток: Архитектура счастья»",
            final_path
        ])

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Готово: {final_filename} ({os.path.getsize(final_path):,} байт)")
        
        # Copy to public/audio
        import shutil
        shutil.copy2(final_path, public_path)

        # Cleanup temps
        for tf in temp_files:
            if os.path.exists(tf): os.remove(tf)
        if os.path.exists(concat_txt): os.remove(concat_txt)
        if os.path.exists(raw_concat): os.remove(raw_concat)
        
        return final_path
        
    except Exception as e:
        print(f"❌ Ошибка при сборке трека {track_id}: {e}")
        return None

def get_track_duration(filepath: str) -> float:
    try:
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", filepath
        ], capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def build_manifest(chapters: list[dict]):
    manifest = []
    total_tracks = len(chapters)
    
    for chap in chapters:
        track_id = f"{chap['track']:02d}"
        slug = re.sub(r'[^\w\-_]', '_', chap['title'])[:30].strip('_')
        filename = f"{track_id}_{slug}.mp3"
        track_path = os.path.join(AUDIO_OUTPUT_DIR, filename)
        
        exists = os.path.exists(track_path)
        duration = get_track_duration(track_path) if exists else 0.0
        
        manifest.append({
            "track": chap['track'],
            "title": chap['title'],
            "words": chap['words'],
            "filename": filename,
            "url": f"/audio/{filename}",
            "duration": round(duration, 1),
            "duration_formatted": f"{int(duration // 60):02d}:{int(duration % 60):02d}",
            "status": "ready" if exists else "pending"
        })
        
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    ready_count = sum(1 for m in manifest if m['status'] == 'ready')
    total_sec = sum(m['duration'] for m in manifest if m['status'] == 'ready')
    print(f"\n📊 Манифест обновлён: {MANIFEST_FILE}")
    print(f"   Готово треков: {ready_count}/{total_tracks}")
    print(f"   Общий хронометраж готовых: {int(total_sec // 3600)} ч {int((total_sec % 3600) // 60)} мин {int(total_sec % 60)} сек")
    return manifest

async def main():
    parser = argparse.ArgumentParser(description="Audiobook Builder for Inner Current")
    parser.add_argument("--all", action="store_true", help="Сгенерировать все главы")
    parser.add_argument("--track", type=int, help="Сгенерировать конкретный номер трека (например 1)")
    parser.add_argument("--range", type=str, help="Диапазон треков, например 1-5")
    parser.add_argument("--manifest-only", action="store_true", help="Только обновить JSON-манифест")
    args = parser.parse_args()
    
    chapters = parse_book()
    total_tracks = len(chapters) - 1 # from 0 to 49
    
    # If track 0 already exists in public/audio, ensure it's in tracks
    track0_src = os.path.join(CURRENT_DIR, "00_Слово_к_русскому_изданию_Демо.mp3")
    track0_dst = os.path.join(AUDIO_OUTPUT_DIR, "00_Слово_к_русскому_изданию_Русский_синтез.mp3")
    if os.path.exists(track0_src) and not os.path.exists(track0_dst):
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
        import shutil
        shutil.copy2(track0_src, track0_dst)
    
    if args.manifest_only:
        build_manifest(chapters)
        return
        
    selected_chapters = []
    if args.track is not None:
        selected_chapters = [c for c in chapters if c['track'] == args.track]
    elif args.range:
        parts = [int(p) for p in args.range.split('-')]
        start, end = parts[0], parts[1]
        selected_chapters = [c for c in chapters if start <= c['track'] <= end]
    elif args.all:
        selected_chapters = chapters
    else:
        # Default: generate first 3 introductory tracks (Manifest, Preface, Intro)
        selected_chapters = [c for c in chapters if 0 <= c['track'] <= 3]
        
    for chap in selected_chapters:
        await synthesize_track(chap, len(chapters))
        
    build_manifest(chapters)

if __name__ == "__main__":
    asyncio.run(main())
