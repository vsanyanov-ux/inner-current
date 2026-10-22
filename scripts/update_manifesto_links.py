import os

def update_manifesto_files():
    targets = [
        ("dist_site/manifesto.html", "books/manifesto.pdf", "Скачать PDF", "Скачать Манифест в PDF", "ru"),
        ("public/manifesto.html", "books/manifesto.pdf", "Скачать PDF", "Скачать Манифест в PDF", "ru"),
        ("dist_site/en/manifesto.html", "/books/manifesto_en.pdf", "Download PDF", "Download Manifesto PDF", "en"),
        ("public/en/manifesto.html", "/books/manifesto_en.pdf", "Download PDF", "Download Manifesto PDF", "en"),
    ]

    for path, pdf_link, btn_label, hero_label, lang in targets:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        # Update navbar button if reader is present
        if "index.html#reader" in html and pdf_link not in html:
            if lang == "ru":
                old_nav = """          <a href="index.html#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">
            <span>📖</span> <span>Ридер</span>
          </a>"""
            else:
                old_nav = """          <a href="/en/#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">
            <span>📖</span> <span>Reader</span>
          </a>"""

            new_nav = f"""          <a href="{pdf_link}" download class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20" title="{hero_label}">
            <span>📥</span> <span>{btn_label}</span>
          </a>"""

            if old_nav in html:
                html = html.replace(old_nav, new_nav, 1)
                print(f"Updated nav in {path}")

        # Update Hero CTA buttons
        marker_ru = '<div class="text-xs text-slate-400 mt-0.5 font-medium">Свободный открытый код</div>'
        marker_en = '<div class="text-xs text-slate-400 mt-0.5 font-medium">Free Open Source</div>'
        marker = marker_ru if lang == "ru" else marker_en

        if f'href="{pdf_link}"' not in html and marker in html:
            cta_block = f"""      <!-- Download CTA -->
      <div class="mt-8 flex flex-wrap items-center justify-center gap-3">
        <a href="{pdf_link}" download class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-400 hover:to-amber-300 text-slate-950 font-bold text-xs sm:text-sm transition flex items-center gap-2 shadow-lg shadow-amber-500/20">
          <span>📥</span> <span>{hero_label}</span>
        </a>
        <a href="#reading" class="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 font-semibold text-xs sm:text-sm transition flex items-center gap-2">
          <span>📜</span> <span>{"Читать онлайн" if lang == "ru" else "Read Online"}</span>
        </a>
      </div>"""

            target_block = "      </div>\n    </div>\n  </header>"
            replacement_block = f"      </div>\n{cta_block}\n    </div>\n  </header>"
            if target_block in html:
                html = html.replace(target_block, replacement_block, 1)
                print(f"Added Hero CTA in {path}")

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    update_manifesto_files()
