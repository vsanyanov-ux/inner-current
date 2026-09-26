# 🚀 Инструкция: Как задепонировать препринт на Zenodo (CERN) и получить вечный DOI

Платформа **Zenodo** (создана CERN и OpenAIRE при поддержке Европейской комиссии) — это официальный мировой репозиторий открытой науки. Публикация здесь:
1. Выдаёт официальный международный **DOI** (Digital Object Identifier) вида `10.5281/zenodo.XXXXXXX`.
2. Фиксирует дату и время публикации с юридической защитой авторского приоритета по всему миру.
3. Индексируется в Google Scholar, OpenAIRE, DataCite, BASE и академических библиотеках.
4. Хранится вечно в защищённых дата-центрах CERN (Швейцария).

---

## 📋 Подготовка файлов перед загрузкой

В вашей папке `docs/preprints/` уже всё подготовлено:
* **Файл препринта:** `ANYANOV-2026-01-FOUR-ELEMENT-TOPOLOGY.md`  
  *(Вы можете загрузить как `.md`, так и сконвертировать его в `.pdf` — Zenodo принимает оба формата, идеальный вариант: прикрепить `.pdf` и/или `.md`).*
* **Файл метаданных:** `zenodo_metadata.json` (готовые поля для копирования).

---

## ⚡ Пошаговый процесс депонирования (занимает 7–10 минут)

### Шаг 1. Вход в Zenodo
1. Откройте в браузере: **[https://zenodo.org](https://zenodo.org)**
2. Нажмите в правом верхнем углу **Log in** / **Sign up**.
3. Рекомендуется войти через ваш аккаунт **GitHub** или **ORCID** (кнопка *«Log in with GitHub»* / *«ORCID»*), либо зарегистрироваться по e-mail.

---

### Шаг 2. Создание нового депонирования (New Upload)
1. В верхнем меню нажмите кнопку **Upload** или перейдите по ссылке: **[https://zenodo.org/uploads/new](https://zenodo.org/uploads/new)**.
2. В блоке **Files**:
   - Нажмите **Choose files** (или просто перетащите файл мышью).
   - Выберите файл `ANYANOV-2026-01-FOUR-ELEMENT-TOPOLOGY.md` (или сформированный PDF-документ).
   - Нажмите зелёную кнопку **Start upload** (файл загрузится на сервер).

---

### Шаг 3. Резервирование DOI (Важнейший шаг!)
1. В секции **Basic information** найдите блок **Digital Object Identifier (DOI)**.
2. Нажмите кнопку **«Reserve DOI»**.
3. Zenodo немедленно сгенерирует для вашей статьи её будущий уникальный постоянный адрес (например: `10.5281/zenodo.12345678`).  
   *Этот номер уже можно цитировать и сохранять!*

---

### Шаг 4. Заполнение метаданных (скопируйте из заготовки)

Заполните поля в веб-форме (значения полностью подготовлены в `zenodo_metadata.json`):

1. **Resource type:**
   - Выберите: **Publication** $\to$ **Preprint** (или *Working paper*).
2. **Publication date:**
   - `2026-09-25` (или текущая дата).
3. **Title:**
   ```text
   The Four-Element Topology of Human Consciousness: An Electrodynamic Model of Generator, Fuse, Resistor, and Load in State Dynamics and Well-Being Architecture
   ```
4. **Creators:**
   - **Family name, given name:** `Anyanov, Vladimir`
   - **Affiliation:** `Inner Current Systems Architecture Lab`
   - **ORCID:** *(если у вас есть ORCID ID, укажите его; если нет, оставьте пустым)*.
5. **Description:**
   - Вставьте HTML-описание из файла `zenodo_metadata.json` (включает название, авторство и полную билингвальную аннотацию на английском и русском языках).
6. **License:**
   - Выберите: **Creative Commons Attribution 4.0 International (CC-BY-4.0)** *(стандарт открытой науки, гарантирующий упоминание вас как автора)*.
7. **Keywords:**
   - Добавьте через Enter:
     ```text
     electrodynamics of consciousness
     four-element topology
     superconductivity
     tanden
     zanshin
     mushin
     default mode network
     joule-lenz law
     thermodynamics of happiness
     inner current
     anyanov system
     ```
8. **Language:**
   - Укажите: `eng` (или `rus`).
9. **Notes (optional):**
   ```text
   Preprint v1.0. Bilingual English / Russian paper. Core architecture of the Anyanov System.
   ```

---

### Шаг 5. Публикация и фиксация вечного следа

1. Внизу страницы нажмите кнопку **Save** (сохранить черновик).
2. Проверьте предпросмотр.
3. Нажмите большую оранжевую кнопку **Publish**!
4. В появившемся модальном окне подтвердите:
   > *"Once published, the record cannot be deleted, and the DOI is permanently registered."*

**Поздравляем!**  
Статья опубликована в архиве CERN.  
Ваш мировой приоритет навсегда зафиксирован международным DOI. Теперь эту ссылку можно отправлять в научные сообщества, указывать в резюме, прикреплять к статьям на Хабре, в Substack и в открытых репозиториях! 🚀⚡
