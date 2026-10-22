import asyncio
import os
import sys
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VOICE = "ru-RU-DmitryNeural"
RATE = "+4%"

SCENES = [
    {
        "id": "scene1",
        "text": "Когда человеку говоришь про Внутренний ток, он начинает защищаться списком удовольствий: У меня же есть раф, поездки на море, шопинг! Но смотри: твой раф или отпуск — это просто крутой тостер!"
    },
    {
        "id": "scene2",
        "text": "Но если в розетке нет тока или выбило пробки — сколько тостеров в неё ни тыкай, хлеб останется сырым и холодным!"
    },
    {
        "id": "scene3",
        "text": "Если внутренний ток отключён, а проводка сгорела от тревоги — даже самый дорогой раф на пляже встаёт сухим комом в горле!"
    },
    {
        "id": "scene4",
        "text": "Внутренний ток — это электричество. Удовольствия — это лишь приборы. Источник счастья никогда не был в тостере — он в напряжении твоей сети!"
    },
    {
        "id": "scene5",
        "text": "Когда ток течёт чисто, без сопротивления эго — даже кусок простого чёрного хлеба с водой вызывает чистый экстаз и восторг бытия!"
    },
    {
        "id": "scene6",
        "text": "Перестань скупать новые тостеры. Включи ток в своей розетке! Подпишись на канал, чтобы настроить свой внутренний ток!"
    }
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

async def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating voiceover into {OUTPUT_DIR}...")
    for scene in SCENES:
        output_file = os.path.join(OUTPUT_DIR, f"{scene['id']}.mp3")
        # Retry loop
        success = False
        for attempt in range(1, 4):
            try:
                communicate = edge_tts.Communicate(scene["text"], VOICE, rate=RATE)
                await communicate.save(output_file)
                size = os.path.getsize(output_file)
                print(f"[OK] Generated {scene['id']}.mp3 ({size} bytes)")
                success = True
                break
            except Exception as e:
                print(f"[WARN] {scene['id']} attempt {attempt} failed: {e}. Retrying...")
                await asyncio.sleep(2)
        if not success:
            print(f"[ERROR] Failed to generate {scene['id']}.mp3 after 3 attempts.")
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(generate())
