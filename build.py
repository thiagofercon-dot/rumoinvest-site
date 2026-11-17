import json, glob, os
root = os.path.dirname(os.path.abspath(__file__))
arts = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(root, 'content', '*.json'))) if not f.endswith('imagens-pendentes.json')]
slugs = [a['slug'] for a in arts]
assert len(slugs) == len(set(slugs)), 'slugs repetidos'
for a in arts:
    for k in ('slug','title','subtitle','category','date','body'):
        assert k in a, f"{a.get('slug')}: falta {k}"
    if a.get('image'):
        assert os.path.exists(os.path.join(root, a['image'])), f"capa ausente: {a['image']}"
qf = os.path.join(root, 'data', 'cotacoes.json')
q = json.load(open(qf, encoding='utf-8')) if os.path.exists(qf) else {'updated': '', 'items': []}
dump = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
tpl = open(os.path.join(root, 'template.html'), encoding='utf-8').read()
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(tpl.replace('__QUOTES__', dump(q)).replace('__DATA__', dump(arts)))
print(len(arts), 'matérias -> index.html')
