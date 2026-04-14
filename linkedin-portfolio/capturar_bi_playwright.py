"""
Captura screenshots de todas as abas do BI Dashboard e telas do Planka
usando Playwright — salva como BMP via Pillow
"""

import sys
import io
import time
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# -------------------------------------------------
# Tenta importar Pillow para conversão PNG -> BMP
# -------------------------------------------------
try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("Pillow nao encontrado — salvando como PNG (renomeando para .bmp)")

BASE   = Path(r'C:\Users\Cliente\Desktop\Engineering-Lab\linkedin-portfolio\Print do Projeto')
BI_URL = 'file:///C:/Users/Cliente/Desktop/Engineering-Lab/linkedin-portfolio/bi-dashboard/index.html'
PLANKA = 'http://localhost:3333'

BASE.mkdir(exist_ok=True)

def salvar(page, nome_sem_ext):
    """Faz screenshot da página inteira e salva como BMP."""
    png_bytes = page.screenshot(full_page=False)
    dest = BASE / f'{nome_sem_ext}.bmp'
    if HAS_PILLOW:
        from PIL import Image
        import io as _io
        img = Image.open(_io.BytesIO(png_bytes))
        img.save(str(dest), 'BMP')
    else:
        dest.write_bytes(png_bytes)          # salva PNG com extensão .bmp
    print(f'SALVO -> {dest.name}')

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=['--start-maximized'])
    ctx     = browser.new_context(viewport={'width': 1920, 'height': 1080}, no_viewport=True)
    page    = ctx.new_page()

    # -------------------------------------------------------
    # BI Dashboard — Overview do Portfólio
    # -------------------------------------------------------
    print("\n=== BI Dashboard ===")
    page.goto(BI_URL, wait_until='networkidle')
    page.wait_for_timeout(1500)

    # Clica em "Dashboard Geral" (nav-item 0 = overview)
    page.evaluate("document.querySelector('.nav-item').click()")
    page.wait_for_timeout(800)
    salvar(page, '08_BI_Portfolio_Overview')

    # -------------------------------------------------------
    # Itera pelos 5 projetos × 6 abas cada
    # -------------------------------------------------------
    projetos = [
        ('PRJ-001', 'PRJ001_SaindoZero'),
        ('PRJ-002', 'PRJ002_ArtemisII'),
        ('PRJ-003', 'PRJ003_PortalRH'),
        ('PRJ-004', 'PRJ004_DataLake'),
        ('PRJ-005', 'PRJ005_AppMobile'),
    ]
    abas = [
        ('visao-geral',  'VisaoGeral'),
        ('kpis',         'KPIs'),
        ('okrs',         'OKRs'),
        ('roi',          'ROI'),
        ('tradeoff',     'TradeOff'),
        ('burndown',     'Previsibilidade'),
    ]

    for idx, (prj_id, prj_slug) in enumerate(projetos):
        print(f"\n--- {prj_id} ---")
        # Clica no projeto no sidebar via JS (idx+1 pula o "Dashboard Geral")
        page.evaluate(f"""
            const items = document.querySelectorAll('.nav-item');
            if (items[{idx + 1}]) items[{idx + 1}].click();
        """)
        page.wait_for_timeout(900)

        for tab_id, tab_slug in abas:
            # Clica na aba via JS (mais confiável que seletor de texto)
            page.evaluate(f"""
                const btns = document.querySelectorAll('.tab-btn');
                btns.forEach(b => {{
                    if (b.getAttribute('onclick') && b.getAttribute('onclick').includes('{tab_id}')) {{
                        b.click();
                    }}
                }});
            """)
            page.wait_for_timeout(700)
            nome = f'{prj_id}_{tab_slug}'
            salvar(page, nome)

    # -------------------------------------------------------
    # Planka — Lista de Projetos
    # -------------------------------------------------------
    print("\n=== Planka ===")
    try:
        page.goto(PLANKA, wait_until='domcontentloaded', timeout=10000)
        page.wait_for_timeout(3000)
        salvar(page, '09_Planka_Lista_Projetos')

        # Tenta clicar no primeiro projeto
        first_board = page.locator('.BoardItem_name__1a2b3, [class*="BoardItem"], [class*="board"]').first
        if first_board.is_visible(timeout=3000):
            first_board.click()
            page.wait_for_timeout(3000)
            salvar(page, '10_Planka_Board_PRJ001')
    except Exception as e:
        print(f"Planka nao acessivel: {e}")

    browser.close()

print("\n\nTodos os prints salvos em:", BASE)
import os
for f in sorted(BASE.glob('*.bmp')):
    size_mb = round(f.stat().st_size / 1024 / 1024, 2)
    print(f"  {f.name:50s}  {size_mb} MB")
