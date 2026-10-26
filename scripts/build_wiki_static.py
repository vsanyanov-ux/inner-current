# -*- coding: utf-8 -*-
"""
Build static data for Inner Current Wiki Reader:
1. Syncs ONLY Inner Current files from Obsidian Vault to local wiki/ and MOC
2. Parses 4 Canonical Layers from Inner Current - MOC.md
3. Detects any unindexed Inner Current articles, brochures and books into Layer V
4. Strictly filters out all non-Inner Current topics (Henry George, Italian, AI coding, Impressionics)
5. Emits:
   - dist_site/data/wiki/catalog.json & public/data/wiki/catalog.json
   - dist_site/data/wiki/articles/art_{id}.json & public/data/wiki/articles/art_{id}.json
   - dist_site/api/wiki/articles (static API fallback)
"""
import os
import re
import sys
import json
import shutil
from datetime import datetime

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_DIR = os.path.join(ROOT_DIR, 'wiki')
MOC_FILE = os.path.join(ROOT_DIR, 'Inner Current - MOC.md')
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')
DIST_DIR = os.path.join(ROOT_DIR, 'dist_site')

VAULT_WIKI = r'C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki'
VAULT_MOC = r'C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\04_Maps\Inner Current MOC.md'

NON_IC_KEYWORDS = [
    'henry george', 'georgism', 'single tax', 'ricardo', 'free trade', 'wages and capital', 'malthusian',
    'italian', 'krashen', 'vocabulary lists', 'future tense', 'imperative mood',
    'ai-auditor', 'agentic engineering', 'vram', 'ollama', 'obsidian', 'rag', 'rubber stamping', 
    'provider pattern', 'software 3.0', 'software entropy', 'spec-driven', 'company world model', 
    'customer world model', 'code review bottleneck', 'deterministic compiler', 'determinization of chaos',
    'digital heritage', 'forward deployed engineer', 'hybrid ai', 'intelligence layer', 'intent-driven',
    'language learning with ai', 'llm wiki', 'productivity paradox', 'unified state space', 'vibe coding',
    'systems thinking', 'tenchat', 'consequence capital', 'global strategic roadmap', 'philosophy of scientific discovery',
    # Impressionics / External magnetism / perfumery / clothing / style
    'impressionics', 'anyanov impressionics', 'applied impression', 'cognitive impressionics', 
    'five fundamental laws of impressionics', 'biophysics of axes', 'brand matrix', 'budget vector search',
    'canonical 10d matrix', 'canonical tetrad of embodiment', 'four olfactory anchors', 'heart distance',
    'market blindspots', 'mathematical model of note-fabric', 'matrix navigation', 'method of extreme contrasts',
    'mirror of fragrances', 'monobrand matrix', 'olfactory timeline', 'origin story (lattafa',
    'perception engine', 'perception engineering', 'perception radar', 'periodic table of clothing',
    'periodic table of fragrances', 'periodic table of scent', 'psychophysical resonance', 'recommendation pipeline',
    'retail synergy matrix', 'semiotics of x-axis', 'signal amplitude and expression', 'style solfeggio',
    'strategic pivot to applied engineering', 'the cardamom case', 'the clone cosine law', 'the overdose paradox',
    'the pyramid weight problem', 'the royal protocol anomaly', 'the tobacco bifurcation', 'three-level isomorphism',
    'top-5 practical applications (impressionics', 'triad of carriers', 'two-tier perception funnel',
    'wearable performance', 'zero-crossing rule', 'импрессионика', 'архитектура впечатления', 
    'одеколон pitch presentation', 'четырёхэтапная методология вычисления координат xy'
]

def is_inner_current(filename, content=""):
    """
    Checks if a markdown file belongs strictly to Inner Current.
    Filters out Henry George economics, Italian grammar, AI engineering, Impressionics, etc.
    """
    fn_lower = filename.lower()
    if 'moc' in fn_lower or filename == 'index.md':
        return False
        
    for kw in NON_IC_KEYWORDS:
        if kw in fn_lower and not ('inner current' in fn_lower or 'внутренний ток' in fn_lower or 'внутреннего тока' in fn_lower):
            return False

    if filename.startswith('Inner Current'):
        return True
    if 'внутренний ток' in fn_lower or 'внутреннего тока' in fn_lower or 'inner current' in fn_lower:
        return True
    if filename.startswith('Брошюра — ') and 'импрессионик' not in fn_lower:
        return True
    if filename.startswith('Книга — ') and any(k in fn_lower for k in ['внутренний', 'синтез', 'фрактал', 'потоковых', 'коперник', 'укулеле', 'триптих']):
        return True
    if filename.startswith('Книга-праймер — Тайна'):
        return True
    if filename.startswith('Презентация — Счастье'):
        return True
    if '懐中電灯' in filename:
        return True
    if re.match(r'^\d{2}-.*\.md$', filename):
        return True

    if content:
        fm_text = content[:1200].lower()
        if 'inner-current' in fm_text or 'node/tanden' in fm_text or 'node/conductor' in fm_text or 'node/ego-resistor' in fm_text:
            return True
        if 'внутренний ток' in fm_text or 'сверхпроводимость цепи' in fm_text:
            return True

    return False

def sync_from_vault():
    os.makedirs(WIKI_DIR, exist_ok=True)
    if os.path.exists(VAULT_WIKI):
        copied = 0
        for f in os.listdir(VAULT_WIKI):
            if f.endswith('.md'):
                src = os.path.join(VAULT_WIKI, f)
                try:
                    with open(src, 'r', encoding='utf-8') as fp:
                        sample = fp.read(1200)
                except Exception:
                    sample = ""
                if is_inner_current(f, sample):
                    dst = os.path.join(WIKI_DIR, f)
                    if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                        shutil.copy2(src, dst)
                        copied += 1
        if copied > 0:
            print(f"🔄 Synced {copied} Inner Current articles from Obsidian Vault to wiki/")

    if os.path.exists(VAULT_MOC):
        if not os.path.exists(MOC_FILE) or os.path.getmtime(VAULT_MOC) > os.path.getmtime(MOC_FILE):
            shutil.copy2(VAULT_MOC, MOC_FILE)
            print("🔄 Synced latest MOC from Obsidian Vault")

def parse_frontmatter_and_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    frontmatter = {}
    content = raw
    fm_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$', raw)
    if fm_match:
        content = fm_match.group(2)
        fm_text = fm_match.group(1)
        for line in fm_text.splitlines():
            kv = re.match(r'^([a-zA-Z0-9_-]+):\s*(.*)$', line)
            if kv:
                k, val = kv.group(1), kv.group(2).strip()
                if val.startswith('[') and val.endswith(']'):
                    val = [s.strip().strip('\'"') for s in val[1:-1].split(',') if s.strip()]
                frontmatter[k] = val

    st = os.stat(file_path)
    mtime = datetime.fromtimestamp(st.st_mtime).isoformat()
    return frontmatter, content, mtime, st.st_size

def build_static_wiki():
    sync_from_vault()

    if not os.path.exists(MOC_FILE):
        raise FileNotFoundError(f"Missing MOC file at {MOC_FILE}")

    with open(MOC_FILE, 'r', encoding='utf-8') as f:
        moc_lines = f.readlines()

    layers = []
    layer_map = {}
    indexed_slugs = set()
    articles_data = []
    slug_map = {}

    current_layer = None
    art_counter = 0

    for line in moc_lines:
        line_str = line.strip()
        layer_match = re.match(r'^####\s+(.+)$', line_str)
        if layer_match:
            current_layer = layer_match.group(1).strip()
            layer_id = f"layer-{len(layers) + 1}"
            if current_layer not in layer_map:
                l_obj = {
                    "id": layer_id,
                    "title": current_layer,
                    "articles": []
                }
                layer_map[current_layer] = l_obj
                layers.append(l_obj)
            continue

        if current_layer:
            am = re.match(r'^\s*(\d+)\.\s+\*\*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\*\*(?:\s*[—–-]\s*(.*))?$', line_str)
            if am:
                moc_idx = int(am.group(1))
                raw_target = am.group(2).strip()
                display_title = am.group(3).strip() if am.group(3) else raw_target
                summary = am.group(4).strip() if am.group(4) else ''

                clean_base = raw_target.replace('02_Wiki/', '').replace('.md', '')
                filename = clean_base + '.md'
                file_path = os.path.join(WIKI_DIR, filename)

                if not os.path.exists(file_path):
                    if os.path.exists(os.path.join(VAULT_WIKI, filename)):
                        file_path = os.path.join(VAULT_WIKI, filename)

                if not os.path.exists(file_path):
                    continue

                fm, content, mtime, size = parse_frontmatter_and_content(file_path)
                
                # Double check that article is Inner Current
                if not is_inner_current(filename, content):
                    continue

                art_counter += 1
                art_id = f"art-{art_counter}"

                meta_entry = {
                    "id": art_id,
                    "mocIndex": moc_idx,
                    "filename": filename,
                    "slug": clean_base,
                    "title": display_title,
                    "summary": summary,
                    "layer": current_layer,
                    "layerId": layer_map[current_layer]["id"],
                    "dataFile": f"data/wiki/articles/{art_id}.json",
                    "created": fm.get('created', mtime[:10]),
                    "tags": fm.get('tags', [])
                }

                full_entry = {
                    "id": art_id,
                    "slug": clean_base,
                    "title": display_title,
                    "filename": filename,
                    "layer": current_layer,
                    "layerId": layer_map[current_layer]["id"],
                    "frontmatter": fm,
                    "content": content,
                    "mtime": mtime,
                    "size": size
                }

                layer_map[current_layer]["articles"].append(meta_entry)
                articles_data.append(full_entry)

                indexed_slugs.add(clean_base.lower())
                slug_map[clean_base.lower()] = art_id
                slug_map[clean_base.replace('Inner Current (', '').replace(')', '').lower()] = art_id
                if raw_target.lower() != clean_base.lower():
                    slug_map[raw_target.lower()] = art_id

    # Layer V: Master brochures, books and unindexed Inner Current materials
    unindexed = []
    if os.path.exists(WIKI_DIR):
        for f in sorted(os.listdir(WIKI_DIR)):
            if not f.endswith('.md') or 'MOC' in f or f == 'index.md':
                continue
            base = f[:-3]
            if base.lower() not in indexed_slugs:
                file_path = os.path.join(WIKI_DIR, f)
                fm, content, mtime, size = parse_frontmatter_and_content(file_path)
                
                # STRICT FILTER: MUST BE INNER CURRENT ONLY
                if not is_inner_current(f, content):
                    continue

                art_counter += 1
                art_id = f"art-{art_counter}"

                title = base
                tm = re.search(r'^#\s+(.+)$', content, re.M)
                if tm:
                    title = tm.group(1).strip()
                summary = ''
                qm = re.search(r'>\s*\[!quote\]\s*(.+)', content)
                if qm:
                    summary = qm.group(1).strip()

                meta_entry = {
                    "id": art_id,
                    "mocIndex": len(unindexed) + 1,
                    "filename": f,
                    "slug": base,
                    "title": title,
                    "summary": summary or 'Мастер-рукопись / брошюра контура',
                    "layer": 'V. Брошюры-манифесты и мастер-рукописи Внутреннего Тока',
                    "layerId": 'layer-new',
                    "dataFile": f"data/wiki/articles/{art_id}.json",
                    "created": fm.get('created', mtime[:10]),
                    "tags": fm.get('tags', []),
                    "isNew": True
                }

                full_entry = {
                    "id": art_id,
                    "slug": base,
                    "title": title,
                    "filename": f,
                    "layer": 'V. Брошюры-манифесты и мастер-рукописи Внутреннего Тока',
                    "layerId": 'layer-new',
                    "frontmatter": fm,
                    "content": content,
                    "mtime": mtime,
                    "size": size
                }

                unindexed.append(meta_entry)
                articles_data.append(full_entry)
                slug_map[base.lower()] = art_id

    if unindexed:
        layers.append({
            "id": "layer-new",
            "title": "V. Брошюры-манифесты и мастер-рукописи Внутреннего Тока",
            "articles": unindexed
        })

    total_articles = sum(len(l["articles"]) for l in layers)
    catalog = {
        "layers": layers,
        "total": total_articles,
        "slugMap": slug_map,
        "lastScanned": datetime.now().isoformat()
    }

    # Destinations: public and dist_site
    targets = [PUBLIC_DIR, DIST_DIR]
    for target in targets:
        wiki_data_dir = os.path.join(target, 'data', 'wiki')
        articles_dir = os.path.join(wiki_data_dir, 'articles')
        
        # Clean articles directory first so no stale non-Inner Current files exist
        if os.path.exists(articles_dir):
            shutil.rmtree(articles_dir)
        os.makedirs(articles_dir, exist_ok=True)

        # Save catalog.json
        cat_file = os.path.join(wiki_data_dir, 'catalog.json')
        with open(cat_file, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)

        # Save each article
        for art in articles_data:
            art_file = os.path.join(articles_dir, f"{art['id']}.json")
            with open(art_file, 'w', encoding='utf-8') as f:
                json.dump(art, f, ensure_ascii=False)

        # Also create static API fallback at target/api/wiki/articles
        api_dir = os.path.join(target, 'api', 'wiki')
        os.makedirs(api_dir, exist_ok=True)
        try:
            with open(os.path.join(api_dir, 'articles'), 'w', encoding='utf-8') as f:
                json.dump(catalog, f, ensure_ascii=False)
        except Exception:
            pass

    print(f"✅ Generated static wiki data: {total_articles} articles across {len(layers)} layers")
    for l in layers:
        print(f"   - {l['title']}: {len(l['articles'])} articles")
    print(f" - Catalog: dist_site/data/wiki/catalog.json ({len(json.dumps(catalog))} bytes)")
    print(f" - Articles: {len(articles_data)} JSON files in dist_site/data/wiki/articles/")

if __name__ == '__main__':
    build_static_wiki()
