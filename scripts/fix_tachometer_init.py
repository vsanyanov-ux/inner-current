# -*- coding: utf-8 -*-
"""
Fix Tachometer initial needle position on page refresh in public/trainer.html and dist_site/trainer.html.
1. Update static SVG elements in #tach-needle-group to point at 75 (angle = +45 deg).
2. Wire tach_render call directly into DOMContentLoaded.
3. Call updateTachNeedleGeometry(45) on script load.
"""
import os
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_TRAINER = os.path.join(ROOT_DIR, 'public', 'trainer.html')
DIST_TRAINER = os.path.join(ROOT_DIR, 'dist_site', 'trainer.html')

OLD_NEEDLE_SVG = '''                  <!-- Dynamic Tachometer Needle (CLEAN - NO CIRCLE AT TIP) -->
                  <g id="tach-needle-group">
                    <polygon id="tach-needle-counter" points="146.5,140 153.5,140 150,154" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/>
                    <polygon id="tach-needle-beam" points="146.5,140 153.5,140 151,22 149,22" fill="url(#tach-needle-gradient)" filter="url(#tach-needle-glow)"/>
                    <line id="tach-needle-spine" x1="150" y1="140" x2="150" y2="22" stroke="#ffffff" stroke-width="0.8" opacity="0.9"/>
                    
                    <circle id="tach-needle-tip-glow" cx="150" cy="22" r="3" fill="#38bdf8" filter="url(#tach-needle-glow)"/>
                    <circle id="tach-needle-tip-core" cx="150" cy="22" r="1.2" fill="#ffffff"/>

                    <circle cx="150" cy="140" r="12" fill="#0b1329" stroke="#38bdf8" stroke-width="2.5" filter="url(#tach-needle-glow)"/>
                    <circle cx="150" cy="140" r="5.5" fill="#38bdf8"/>
                    <circle cx="150" cy="140" r="2" fill="#ffffff"/>
                  </g>'''

NEW_NEEDLE_SVG = '''                  <!-- Dynamic Tachometer Needle (CLEAN - NO CIRCLE AT TIP, DEFAULT I=75) -->
                  <g id="tach-needle-group">
                    <polygon id="tach-needle-counter" points="147.5,137.5 152.5,142.5 140.1,149.9" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/>
                    <polygon id="tach-needle-beam" points="147.5,137.5 152.5,142.5 234.1,57.3 232.7,55.9" fill="url(#tach-needle-gradient)" filter="url(#tach-needle-glow)"/>
                    <line id="tach-needle-spine" x1="150" y1="140" x2="233.4" y2="56.6" stroke="#ffffff" stroke-width="0.8" opacity="0.9"/>
                    
                    <circle id="tach-needle-tip-glow" cx="233.4" cy="56.6" r="3" fill="#38bdf8" filter="url(#tach-needle-glow)"/>
                    <circle id="tach-needle-tip-core" cx="233.4" cy="56.6" r="1.2" fill="#ffffff"/>

                    <circle cx="150" cy="140" r="12" fill="#0b1329" stroke="#38bdf8" stroke-width="2.5" filter="url(#tach-needle-glow)"/>
                    <circle cx="150" cy="140" r="5.5" fill="#38bdf8"/>
                    <circle cx="150" cy="140" r="2" fill="#ffffff"/>
                  </g>'''

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update static SVG needle to point at 75
    if OLD_NEEDLE_SVG in content:
        content = content.replace(OLD_NEEDLE_SVG, NEW_NEEDLE_SVG)
        print(f"Updated static SVG needle points in {file_path}")
    else:
        # Try regex if spacing differs
        pattern = r'<g id="tach-needle-group">[\s\S]*?</g>'
        new_g = NEW_NEEDLE_SVG.strip().replace('<!-- Dynamic Tachometer Needle (CLEAN - NO CIRCLE AT TIP, DEFAULT I=75) -->\n', '')
        content = re.sub(pattern, new_g, content, count=1)
        print(f"Updated static SVG needle via regex in {file_path}")

    # 2. Fix DOMContentLoaded call
    dom_target = '''      switchTab(initialTab);
      gauge_render();
    });'''
    dom_replacement = '''      switchTab(initialTab);
      gauge_render();
      if (typeof tach_render === 'function') {
        const sliderTach = document.getElementById('slider-tach-i');
        const initialI = sliderTach ? parseInt(sliderTach.value, 10) || 75 : 75;
        tach_render(initialI);
      }
    });'''
    if dom_target in content:
        content = content.replace(dom_target, dom_replacement)
        print(f"Injected tach_render into DOMContentLoaded in {file_path}")

    # 3. Add immediate script-load initialization
    immediate_init = '''
    // Immediate script-load Tachometer positioning (I = 75, angle = 45 deg)
    try {
      updateTachNeedleGeometry(45);
      if (typeof updateCoupledVerdict === 'function') updateCoupledVerdict();
    } catch (e) {}
'''
    if 'updateTachNeedleGeometry(45);' not in content:
        content = content.replace('window.tach_render = tach_render;', 'window.tach_render = tach_render;\n' + immediate_init)
        print(f"Added immediate script-load initialization in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {file_path}")

def main():
    fix_file(PUBLIC_TRAINER)
    fix_file(DIST_TRAINER)

if __name__ == '__main__':
    main()
