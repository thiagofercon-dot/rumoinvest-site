#!/usr/bin/env python3
"""Gera o site RumoInvest como páginas HTML separadas (uma URL por matéria),
pré-renderizadas para o Google, com sitemap.xml e robots.txt.
Uso: python3 build_static.py   ->   pasta ./site"""
import json, glob, os, shutil, threading, http.server, socketserver, functools, re
from playwright.sync_api import sync_playwright

SITE = 'https://rumoinvest.com'   # <- troque aqui se o domínio final for outro
root = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(root, 'site')
CATS = ['mercado', 'dividendos', 'fiis', 'renda-fixa', 'acoes', 'educacao']
SECS = ['mercado', 'dividendos', 'renda-fixa', 'renda-variavel', 'educacao']

arts = []
for f in sorted([x for x in glob.glob(os.path.join(root, 'content', '*.json')) if 'pendentes' not in x]):
    a = json.load(open(f, encoding='utf-8'))
    for k in ('slug', 'title', 'subtitle', 'category', 'date', 'body'):
        assert k in a, f'{os.path.basename(f)}: falta {k}'
    assert a['category'] in CATS, a['slug']
    arts.append(a)

tpl = open(os.path.join(root, 'template.html'), encoding='utf-8').read()
qf = os.path.join(root, 'data', 'cotacoes.json')
tpl = tpl.replace('__QUOTES__', json.dumps(json.load(open(qf, encoding='utf-8')), ensure_ascii=False))

def rep(old, new):
    global tpl
    assert old in tpl, 'trecho não encontrado no template: ' + old[:60]
    tpl = tpl.replace(old, new, 1)

# 1) dados num arquivo único (cache) em vez de embutidos em cada página
rep('const ARTICLES = __DATA__;', 'const ARTICLES = window.__ARTS;')
rep('<script>', '<script src="assets/data.js"></script>\n<script>')
# 2) rota por caminho (window.__ROUTE) em vez de #hash
rep("function route(){setTimeout(gaView,0);let hsh=(location.hash||'#inicio').slice(1);",
    "function route(){setTimeout(gaView,0);let hsh=location.hash?location.hash.slice(1):(window.__ROUTE!==undefined&&window.__ROUTE!==''?window.__ROUTE:'inicio');")
# 3) links reais (sem #) e SEO com canonical / og:url / og:image
rep("window.addEventListener('hashchange',route);route();",
    """function fixLinks(){document.querySelectorAll('a[href^="#"]').forEach(a=>{const g=a.getAttribute('href').slice(1);
if(g===''||g==='inicio')a.setAttribute('href','./');
else if(g.startsWith('materia-'))a.setAttribute('href','materia/'+g.slice(8)+'/');
else if(g.startsWith('secao-'))a.setAttribute('href','secao/'+g.slice(6)+'/');
else if(g.startsWith('busca-'))a.setAttribute('href','busca/?t='+g.slice(6));});}
route();fixLinks();""")
rep("const md=document.querySelector('meta[name=description]');",
    """const SITE=window.__SITE||'';const url=SITE+(window.__PATH||'/');let cl=document.querySelector('link[rel=canonical]');if(!cl){cl=document.createElement('link');cl.rel='canonical';document.head.append(cl);}cl.href=url;
metaSet('meta[property="og:url"]','property','og:url',url);if(a&&a.image)metaSet('meta[property="og:image"]','property','og:image',SITE+'/'+a.image);
const md=document.querySelector('meta[name=description]');""")

def shell(route, path, depth):
    base = '<base href="' + '../' * depth + '">' if depth else ''
    inj = f'{base}<script>window.__ROUTE={json.dumps(route)};window.__PATH={json.dumps(path)};window.__SITE={json.dumps(SITE)};</script>'
    return tpl.replace('<head>', '<head>\n' + inj, 1)

if os.path.exists(out):
    shutil.rmtree(out)
os.makedirs(out)
shutil.copytree(os.path.join(root, 'assets'), os.path.join(out, 'assets'))
open(os.path.join(out, 'assets', 'data.js'), 'w', encoding='utf-8').write(
    'window.__ARTS=' + json.dumps(arts, ensure_ascii=False).replace('</', '<\\/') + ';')

pages = [('', '', '/', 0)]
for c in SECS:
    pages.append((f'secao-{c}', f'secao/{c}/', f'/secao/{c}/', 2))
for a in arts:
    pages.append((f'materia-{a["slug"]}', f'materia/{a["slug"]}/', f'/materia/{a["slug"]}/', 2))

def write(rel, html):
    p = os.path.join(out, rel, 'index.html') if rel else os.path.join(out, 'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(html)

# 4) pré-renderização com navegador headless (o conteúdo já vem no HTML)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(Q, directory=out)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(('127.0.0.1', 0), handler)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

# página de busca por assunto (conteúdo montado no navegador: /busca/?t=assunto)
write('busca', shell('', '/busca/', 2).replace('window.__ROUTE=""', "window.__ROUTE='busca-'+(new URLSearchParams(location.search).get('t')||'')"))

# primeiro grava os "esqueletos" para o navegador abrir
for route, rel, path, depth in pages:
    write(rel, shell(route if route else None, path, depth) if route else shell('', path, depth))

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(f'http://127.0.0.1:{port}/index.html')
    pg.wait_for_selector('#app *')
    for route, rel, path, depth in pages:
        url = f'http://127.0.0.1:{port}/' + (rel if rel else 'index.html')
        pg.goto(url)
        pg.wait_for_selector('#app *')
        pg.wait_for_timeout(150)
        html = pg.content()
        write(rel, '<!DOCTYPE html>\n' + re.sub(r'^<!DOCTYPE html>\s*', '', html, flags=re.I))
    br.close()
srv.shutdown()
print('erros JS:', errs)

# 5) 404, sitemap e robots
open(os.path.join(out, '404.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Página não encontrada — RumoInvest</title><meta name="robots" content="noindex"></head>'
    '<body style="font-family:Arial,sans-serif;text-align:center;padding:60px;color:#16213a"><h1>Página não encontrada</h1>'
    '<p>Esse endereço não existe mais ou foi digitado errado.</p><p><a href="/">Voltar para o RumoInvest</a></p></body></html>')
urls = [(f'{SITE}/', max(a['date'] for a in arts), '1.0')]
for c in SECS:
    g = {'renda-variavel': ['fiis','acoes']}.get(c, [c])
    urls.append((f'{SITE}/secao/{c}/', max([a['date'] for a in arts if a['category'] in g] or [arts[-1]['date']]), '0.7'))
for a in arts:
    urls.append((f'{SITE}/materia/{a["slug"]}/', a['date'], '0.8'))
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'<url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>\n' for u, d, p in urls) + '</urlset>\n'
open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
open(os.path.join(out, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /busca/\n\nSitemap: {SITE}/sitemap.xml\n')
open(os.path.join(out, '.htaccess'), 'w').write('ErrorDocument 404 /404.html\nDirectoryIndex index.html\n<IfModule mod_expires.c>\nExpiresActive On\nExpiresByType image/jpeg "access plus 1 month"\n</IfModule>\n')
n = sum(len(f) for _, _, f in os.walk(out))
print(f'{len(arts)} matérias, {len(pages)} páginas, {n} arquivos em {out}')
