# vofgo-social

@vofgo.tr Instagram postlarının görselleri, şablonu ve yayın kaydı.

- `template/base.html` — 1080×1350 post şablonu (açık/lacivert tema, VofGo logosu, Plus Jakarta Sans, bileşenler)
- `template/render.py` — `python3 template/render.py specs/<ad>.json posts/<ad>.png`
- `specs/` — her postun içerik dosyası (JSON)
- `posts/` — yayınlanan görseller; Metricool bu klasördeki dosyaları raw.githubusercontent.com üzerinden çeker
- `LOG.md` — yayınlanan/planlanan postların listesi (konu tekrarını önlemek için)

## Tasarım kuralları

- Izgarada açık ve lacivert zemin sırayla gider; yeni post bir öncekinin tersidir.
- Başlık kısa ve vurucu; anahtar kelime `**…**` ile vurgulanır (açıkta sarı alt çizgi, lacivertte sarı yazı).
- Alt metin en fazla 2 cümle; görsel blok ürünü sade bir arayüz parçasıyla anlatır.
- İçerik yalnızca vofgo.com'da yazan gerçek özelliklere dayanır; rakam ve iddia uydurulmaz. Örnek daire/tutarlar temsilîdir.
