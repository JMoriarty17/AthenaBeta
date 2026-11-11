"""Indikator_Strategis.xlsx -> data/indikator.json.
Pertama kali dari CSV:  python tools/build_indikator.py --csv FOLDER_CSV   (membuat workbook, lalu JSON)
Selanjutnya cukup edit workbook, lalu: python tools/build_indikator.py"""
import sys, re, json, pathlib, pandas as pd
here = pathlib.Path(__file__).parent; X = here / 'Indikator_Strategis.xlsx'; OUT = here.parent / 'data' / 'indikator.json'
# kelompok, judul, sheet, tipe (line|bar|hbar|pyramid), kolom, satuan, kpi, catatan
META = [
 ('kependudukan','Jumlah Penduduk','KP_Penduduk','line','Jumlah Penduduk','ribu jiwa',1,''),
 ('kependudukan','Penduduk menurut Kelompok Umur dan Jenis Kelamin','KP_Piramida','pyramid','Laki-Laki,Perempuan','ribu jiwa',0,''),
 ('kependudukan','Penduduk 2025 menurut Kecamatan','KP_Kecamatan','hbar','Penduduk','ribu jiwa',0,''),
 ('kemiskinan','Persentase Penduduk Miskin','KM','line','Persentase Penduduk Miskin','persen',1,''),
 ('kemiskinan','Jumlah Penduduk Miskin','KM','line','Jumlah Penduduk Miskin','ribu jiwa',1,''),
 ('kemiskinan','Garis Kemiskinan','KM','line','Garis Kemiskinan','Rp per kapita per bulan',0,''),
 ('kemiskinan','Indeks Kedalaman dan Keparahan Kemiskinan','KM','line','Indeks Kedalaman,Indeks Keparahan','indeks',0,''),
 ('ketenagakerjaan','Tingkat Partisipasi Angkatan Kerja (TPAK)','KT_TPAK','line','TPAK','persen',1,''),
 ('ketenagakerjaan','Angkatan Kerja menurut Jenis Kelamin (2024)','KT_AK','bar','Laki-Laki,Perempuan','orang',0,'Tahun data perlu dikonfirmasi'),
 ('ketenagakerjaan','Bukan Angkatan Kerja menurut Jenis Kelamin (2024)','KT_BAK','bar','Laki-Laki,Perempuan','orang',0,'Tahun data perlu dikonfirmasi'),
 ('ipm','Indeks Pembangunan Manusia (IPM)','IPM','line','IPM','indeks',1,''),
 ('ipm','Umur Harapan Hidup (UHH)','IPM','line','UHH','tahun',1,''),
 ('ipm','Harapan dan Rata-rata Lama Sekolah','IPM','line','HLS,RLS','tahun',0,''),
 ('ipm','Pengeluaran per Kapita Disesuaikan (PPK)','IPM','line','PPK','ribu rupiah per tahun',0,'Satuan perlu dikonfirmasi'),
 ('pdrb','PDRB Atas Dasar Harga Berlaku','PDRB','line','PDRB ADHB','miliar rupiah',1,''),
 ('pdrb','PDRB Atas Dasar Harga Konstan 2010','PDRB','line','PDRB ADHK 2010','miliar rupiah',0,''),
 ('pdrb','Laju Pertumbuhan PDRB','PDRB','bar','Laju Pertumbuhan','persen',1,'')]
def dari_csv(d):
    d = pathlib.Path(d); r = lambda n: pd.read_csv(d / n, sep=None, engine='python', encoding='utf-8-sig')
    km = r('KM_-_GK__JP__Persentase.csv').merge(r('KM_-_Indeks_Kedalaman_dan_Keparahan.csv'), on='Tahun')
    ipm = r('IPM_-_IPM.csv')
    for n in ('UHH', 'PPK', 'HLS_RLS'): ipm = ipm.merge(r(f'IPM_-_{n}.csv'), on='Tahun')
    pdrb = None
    for n, c in (('Harga_Berlaku', 'PDRB ADHB'), ('Harga_Konstan_2010', 'PDRB ADHK 2010'), ('Laju_Pertumbuhan_PDRB_AD', 'Laju Pertumbuhan')):
        t = r(f'PDRB_-_{n}.csv'); t.columns = ['Tahun', c]; pdrb = t if pdrb is None else pdrb.merge(t, on='Tahun')
    k = r('Indikator_Strategis.csv')
    kel = pd.DataFrame({'id': ['kependudukan', 'kemiskinan', 'ketenagakerjaan', 'ipm', 'pdrb'], 'nama': [n.replace('Prroduk', 'Produk') for n in k['Name']], 'gambar': k['Gambar']})
    S = {'Kelompok': kel, 'Meta': pd.DataFrame(META, columns=['kelompok', 'judul', 'sheet', 'tipe', 'kolom', 'satuan', 'kpi', 'catatan']),
         'KP_Penduduk': r('KP_-_Jumlah_Penduduk.csv'), 'KP_Piramida': r('KP_-_Jumlah_Penduduk_Menurut_Kelompok_Umur_dan_Jenis_Kelamin__1_.csv').drop(columns='P2'),
         'KP_Kecamatan': r('KP_-_Penduduk_2025_Berdasarkan_Daera.csv'), 'KM': km, 'KT_TPAK': r('KT_-_TPAK.csv'), 'KT_AK': r('KT_-_Angkatan_Kerja.csv'),
         'KT_BAK': r('KT_-_Bukan_Angkatan_Kerja.csv'), 'IPM': ipm, 'PDRB': pdrb}
    with pd.ExcelWriter(X) as w:
        for n, df in S.items(): df.to_excel(w, sheet_name=n, index=False)
def build():
    x = pd.read_excel(X, sheet_name=None); meta = x['Meta'].fillna(''); out = []
    for _, k in x['Kelompok'].iterrows():
        m = re.search(r'/d/([\w-]+)', str(k['gambar'])); G = []; S = []
        for _, g in meta[meta.kelompok == k['id']].iterrows():
            df = x[g['sheet']]; cols = [c.strip() for c in g['kolom'].split(',')]; xs = [str(v) for v in df.iloc[:, 0]]
            ser = [dict(n=c, d=[None if pd.isna(v) else round(float(v), 4) for v in df[c]]) for c in cols]
            if g['tipe'] == 'hbar':
                o = sorted(range(len(xs)), key=lambda i: -(ser[0]['d'][i] or 0)); xs = [xs[i] for i in o]; ser[0]['d'] = [ser[0]['d'][i] for i in o]
            G.append(dict(j=g['judul'], u=g['satuan'], t=g['tipe'], c=g['catatan'], x=xs, s=ser))
            if int(g['kpi'] or 0) == 1:
                d = [(i, v) for i, v in enumerate(ser[0]['d']) if v is not None]
                S.append(dict(n=cols[0], v=d[-1][1], t=xs[d[-1][0]], u=g['satuan'], d=round(d[-1][1] - d[-2][1], 4) if len(d) > 1 else None))
        out.append(dict(id=k['id'], nama=k['nama'], g=m.group(1) if m else '', sorotan=S, grafik=G))
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(len(out), 'kelompok,', sum(len(o['grafik']) for o in out), 'grafik')
if '--csv' in sys.argv: dari_csv(sys.argv[sys.argv.index('--csv') + 1])
build()
