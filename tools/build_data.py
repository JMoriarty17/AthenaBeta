"""Ubah Daftar_Tabel_Update2.xlsx -> data/tabel.json + data/sumber.json. Jalankan: python tools/build_data.py"""
import pandas as pd, json, hashlib, re, pathlib
here = pathlib.Path(__file__).parent; out = here.parent / 'data'
df = pd.read_excel(here / 'Daftar_Tabel_Update2.xlsx').fillna('')
def bab(b):
    r, t = re.match(r'^([IVX]+)\.?\s*(.*)$', b.strip()).groups()
    return f'Bab {r}' + (f'. {t.title().replace(" Dan ", " dan ")}' if t else '')
S = df.groupby('Sumber', sort=False).agg(link=('Link', 'first'), jumlah=('Nama', 'size')).sort_values('jumlah', ascending=False)
idx = {n: i for i, n in enumerate(S.index)}; seen = {}; T = []
for r in df.itertuples():
    h = hashlib.md5(f'{r.Sumber}|{r.Bab}|{r.Nama}'.encode()).hexdigest()[:8]
    seen[h] = seen.get(h, 0) + 1
    m = re.search(r'/d/([\w-]+)', r.Gambar)
    T.append(dict(id=h + (f'-{seen[h]}' if seen[h] > 1 else ''), n=r.Nama.strip(), s=idx[r.Sumber], k=r.Kategori, b=bab(r.Bab), g=m.group(1) if m else ''))
dump = lambda p, o: p.write_text(json.dumps(o, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
dump(out / 'tabel.json', T); dump(out / 'sumber.json', [dict(nama=n, link=r.link, jumlah=int(r.jumlah)) for n, r in S.iterrows()])
print(len(T), 'tabel,', len(S), 'publikasi,', sum(1 for x in T if x['g']), 'bergambar,', sum(v - 1 for v in seen.values()), 'judul kembar (ID diberi akhiran)')
