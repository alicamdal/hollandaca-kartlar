# Ömer'in kelime kartları

Türkçe–Hollandaca noktalı yazma ve boyama kartları. Basılı sayfalardaki QR kodlar bu siteyi açar:
**https://alicamdal.github.io/hollandaca-kartlar/**

- `?s=N` → PDF'in N. sayfasının kelimeleri. Dokununca telefonun Hollandaca sesiyle okunur (Web Speech API, nl-NL).
- `kelime-kartlari.pdf` → yazdırılacak PDF (A4, siyah-beyaz).
- `kaynak/` → PDF'i ve siteyi yeniden üretmek için script (`make_trace.py`) ve şablon.

Resimler: [OpenMoji](https://openmoji.org) – CC BY-SA 4.0. Yazı tipi: Kalam (SIL OFL).

## Yeni sayfa / yeni PDF ekleme kuralı

Basılı kağıtlardaki QR kodlar `?s=<sayfa no>` adresini açar. Bu yüzden:

1. **Var olan sayfa numaraları asla değişmez.** 1–30 arası sayfaların içeriği ve sırası sabit kalır.
2. Yeni konular `kaynak/make_trace.py` içindeki `TOPICS` listesinin **sonuna** eklenir. Yeni sayfalar 31, 32, … numaralarını alır.
3. Yeni PDF sadece yeni sayfaları içerir (ör. `kelime-kartlari-2.pdf`). Web sitesi ise tüm sayfaları içeren birleşik `pages.json` ile yeniden üretilir.
4. Var olan bir sayfadaki kelime yanlışsa aynı sayfa numarasında düzeltilir. Kelime eklemek gerekiyorsa yeni sayfa açılır.
