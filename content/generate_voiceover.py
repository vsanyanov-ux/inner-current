import asyncio
import os
import edge_tts

import sys
sys.stdout.reconfigure(encoding='utf-8')

VOICE = "ru-RU-DmitryNeural"
RATE = "+4%"

SCENES = [
    {
        "id": "scene1",
        "text": "Ученые веками спорят, сколько весит душа. Вот эта укулеле весит ровно 400 граммов. А сколько весит музыка, которая из неё звучит?"
    },
    {
        "id": "scene2",
        "text": "Две с половиной тысячи лет философы ломают копья: что первично — материя или дух? Но на самом деле никакой загадки нет!"
    },
    {
        "id": "scene3",
        "text": "Смотри на пальцах: материя — это корпус инструмента. А дух — это его звучание! Музыка не вселяется в укулеле снаружи. Дух — это просто гармоничный звук материи!"
    },
    {
        "id": "scene4",
        "text": "Почему же люди страдают и выгорают? Потому что из-за страха и контроля вцепляются в жизнь мёртвой хваткой! Пережал гриф — и вместо радости получается скрип и боль!"
    },
    {
        "id": "scene5",
        "text": "Всё, что нужно — отпустить зажим. Когда живот расслаблен, а руки свободны — ток радости рождается от малейшего касания!"
    },
    {
        "id": "scene6",
        "text": "Твоё тело — это инструмент. Перестань искать мистику — научись звучать! Подпишись на канал, чтобы настроить свой внутренний ток!"
    }
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "ukulele_shorts", "audio")

async def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Generating voiceover into {OUTPUT_DIR}...")
    for scene in SCENES:
        output_file = os.path.join(OUTPUT_DIR, f"{scene['id']}.mp3")
        communicate = edge_tts.Communicate(scene["text"], VOICE, rate=RATE)
        await communicate.save(output_file)
        size = os.path.getsize(output_file)
        print(f"[OK] Generated {scene['id']}.mp3 ({size} bytes)")

if __name__ == "__main__":
    asyncio.run(generate())
