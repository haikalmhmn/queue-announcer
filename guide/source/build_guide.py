"""Build guide.html (bilingual Queue Announcer staff guide) from base styles + content below.

Usage: python3 guide/source/build_guide.py
Then print guide.html to PDF with Playwright (see the staff-guide-pdf standard).
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = "1.4.1"
CREATED = "6 Nov 2026"
NAME = "Queue Announcer"

BASE_CSS = open(os.path.join(HERE, "base.css"), encoding="utf-8").read()
ICONS = open(os.path.join(HERE, "icons.svg"), encoding="utf-8").read()

EXTRA_CSS = """
/* Foodle additions: Malay lines, outlined markers, Key boxes */
.ms { display: block; font-weight: 400; color: var(--muted); font-size: 8.6pt; font-style: italic; margin-top: .4mm; line-height: 1.35; }
.intro .ms { font-size: 10pt; margin-top: 2mm; }
h3 .ms, h2 .ms { display: inline; font-size: 10pt; margin-left: 2mm; }
.mark { position: absolute; border: 2px solid var(--red); border-radius: 2mm; pointer-events: none; }
.mark.round { border-radius: 50%; }
.mark.dash { border-style: dashed; }
.keybox { border: 1.5px solid #D5D9E0; border-radius: 3.5mm; padding: 4mm 4.5mm; background: #FAFBFC; display: flex; flex-direction: column; gap: 3mm; }
.keybox .kt { font-size: 8.3pt; letter-spacing: .07em; text-transform: uppercase; color: var(--muted); font-weight: 700; padding-bottom: 2mm; border-bottom: 1px solid var(--line); }
.keybox .legend { gap: 2.6mm; }
.keybox .legend li { align-items: start; font-size: 10pt; }
.keybox .legend .dot { margin-top: .3mm; }
.keybox.row .cols { display: grid; gap: 3mm 6mm; }
.tip .ms { display: inline; }
.tip span { line-height: 1.35; }
.fix p .ms { font-size: 8.4pt; }
.cap { margin: 0; }
.shotcap { font-size: 8.5pt; color: var(--muted); margin-top: 6mm; text-align: center; }
.shotcap .ms { font-size: 8pt; }
.page .fixes { gap: 3mm; }
.page .fix { padding: 3mm 3.5mm; }
.pin.sm { width: 4.6mm; height: 4.6mm; margin: -2.3mm 0 0 -2.3mm; font-size: 7pt; }
.q { padding: 2.8mm 3.5mm; }
.q .ms { font-size: 7.6pt; color: #8A93A2; text-transform: none; letter-spacing: 0; font-style: italic; font-weight: 400; display: inline; }
"""


def foot(page):
    right = str(page) if page <= 2 else '<a href="#contents">Contents</a> · %d' % page
    return ('<div class="foot"><span>%s · Staff guide · v%s</span>'
            '<span>Prepared by: Haikal (IT &amp; Merchant Support) · Created %s</span><span>%s</span></div>'
            % (NAME, VERSION, CREATED, right))


def ms(text):
    return '<span class="ms">%s</span>' % text


def li(n, en, my):
    return '<li><span class="dot">%s</span><span>%s%s</span></li>' % (n, en, ms(my))


def keybox(items, cols=None):
    if cols:
        groups = ''.join('<ul class="legend">%s</ul>' % ''.join(li(*it) for it in g) for g in cols)
        return ('<div class="keybox row"><span class="kt">Key · Petunjuk</span>'
                '<div class="cols" style="grid-template-columns:repeat(%d,1fr)">%s</div></div>' % (len(cols), groups))
    return ('<div class="keybox"><span class="kt">Key · Petunjuk</span><ul class="legend">%s</ul></div>'
            % ''.join(li(*it) for it in items))


def tip(icon, en, my, warn=False):
    return ('<div class="tip%s"><svg class="i"><use href="#%s"/></svg><span>%s %s</span></div>'
            % (' warn' if warn else '', icon, en, '<span class="ms" style="display:block">%s</span>' % my))


def marks(spec):
    """spec: list of (kind, left, top, width, height) in % and pins (n, left, top)."""
    out = []
    for kind, l, t, w, h in spec:
        cls = 'mark' + ('' if kind == 'box' else ' ' + kind)
        out.append('<span class="%s" style="left:%s%%;top:%s%%;width:%s%%;height:%s%%"></span>' % (cls, l, t, w, h))
    return '\n      '.join(out)


def pins(spec):
    return '\n      '.join('<span class="pin" style="left:%s%%;top:%s%%">%s</span>' % (l, t, n) for n, l, t in spec)


def shot(img, alt, mk, pn, cap=None, width=None):
    style = ' style="width:%s"' % width if width else ''
    capt = '<p class="shotcap">%s</p>' % cap if cap else ''
    return ('<div class="shot"%s><div class="frame"><img src="%s" alt="%s">\n      %s\n      %s\n    </div>%s</div>'
            % (style, img, alt, marks(mk), pins(pn), capt))


# ---------- annotations (all in % of the 400 x 568 app screen) ----------
MAIN = shot('main.jpg', 'Main screen', [
    ('box', 6.5, 2.8, 24.5, 10.6),           # 1 now calling
    ('round', 66, 3, 14, 9.9),                # 2 repeat
    ('round', 81, 3, 14, 9.9),                # 3 mute
    ('round', 82.5, 16.7, 12, 8.45),          # 4 clear
    ('dash', 3, 29.6, 94, 57.2),              # 5 letters + numbers
    ('box', 81.25, 76.2, 15.5, 9.4),          # 6 delete
    ('box', 3.25, 87.1, 18.5, 11.3),          # 7 recent
    ('box', 22.25, 87.1, 55.5, 11.3),         # 8 announce
    ('box', 78.25, 87.1, 18.5, 11.3),         # 9 settings
], [(1, 37, 8), (2, 59.5, 8), (3, 102.6, 8), (4, 102.6, 21), (5, 12, 61), (6, 102.6, 81),
    (7, 12.5, 103.4), (8, 50, 103.4), (9, 87.5, 103.4)])

RECENT = shot('recent.jpg', 'Recent screen', [
    ('box', 67.75, 12.15, 27.5, 9.5),         # 1 recall
    ('box', 6.75, 12.7, 21, 8.5),             # 2 code + time
    ('box', 3.25, 87.1, 93.5, 11.3),          # 3 back
], [(1, 102.6, 17), (2, 33, 17), (3, 50, 103.4)])

LOCKED = shot('settings-locked.jpg', 'Settings, locked', [
    ('box', 3.25, 14.96, 93.5, 9.51),         # 1 volume
    ('box', 3.25, 29.89, 93.5, 10.21),        # 2 float on top
    ('box', 72.61, 50.95, 22.64, 9.51),       # 3 unlock
    ('box', 3.25, 64.33, 93.5, 10.21),        # 4 reset
], [(1, -2.6, 19.72), (2, -2.6, 35), (3, 102.6, 55.7), (4, -2.6, 69.43)],
    cap='Locked (normal)' + ms('Berkunci (biasa)'))

PINPAD = shot('pinpad.jpg', 'PIN pad', [
    ('box', 30, 24.1, 40, 5.3),               # 5 dots
], [(5, 77, 26.7)], cap='After tapping Unlock' + ms('Selepas tekan Unlock'))

S_TOP = shot('settings.jpg', 'Settings unlocked, top', [
    ('box', 67.91, 50.95, 27.34, 9.51),       # 6 lock now
    ('box', 3.25, 68.2, 93.5, 9.51),          # 7 voice
], [(6, 102.6, 55.7), (7, -2.6, 72.96)])

S_MID = shot('settings-mid.jpg', 'Settings unlocked, middle', [
    ('box', 3.25, 16.05, 93.5, 10.21),        # 8 speed
    ('box', 3.25, 31.55, 93.5, 10.21),        # 9 say the number
    ('box', 79.25, 43.52, 16.5, 8.8),         # 10 bell switch
    ('box', 3.25, 57.96, 93.5, 9.51),         # 11 bell sound + test
    ('dash', 3.25, 72.74, 93.5, 14.5),        # 12 announcement preview
], [(8, -2.6, 21.16), (9, -2.6, 36.65), (10, 62, 47.92), (11, -2.6, 62.71), (12, -2.6, 80)])

S_BOT = shot('settings2.jpg', 'Settings unlocked, bottom', [
    ('box', 3.25, 24.99, 93.5, 10.21),        # 13 test voice
    ('box', 79.25, 36.97, 16.5, 8.8),         # 14 float at first tap
], [(13, -2.6, 30.1), (14, 62, 41.37)])

ABOUT = shot('about.jpg', 'About screen', [
    ('box', 16.5, 37.0, 66.9, 8.8),           # 1 version + created by
    ('box', 3.25, 47.8, 93.5, 12.5),          # 2 up to date
    ('box', 3.25, 73.2, 93.5, 17.9),          # 3 what's new
], [(1, 90, 41.4), (2, 102.6, 54), (3, 102.6, 82)]).replace('class="pin"', 'class="pin sm"')

ARROW = '<div class="arrow"><svg class="i"><use href="#arrow"/></svg></div>'

BODY = f"""
<!-- PAGE 1: what the guide is about -->
<section class="page">
  <div class="cover">
    <img src="logo.jpg" alt="Foodle logo">
    <div>
      <h1>Queue Announcer</h1>
      <p class="sub">Staff guide: calling out orders at the counter{ms('Panduan staf: memanggil pesanan di kaunter')}</p>
      <span class="tag">For version {VERSION} and later</span>
    </div>
  </div>

  <h2 style="font-size:15pt">What this guide is about</h2>
  <p class="intro">Queue Announcer calls out orders for you. You type the order code from the receipt, and the computer plays a bell and reads the code out loud, so customers know their food is ready. This guide shows you how to set it up and use it at the counter.
  {ms('Queue Announcer memanggil pesanan untuk anda. Taip kod pesanan daripada resit, dan komputer akan membunyikan loceng dan menyebut kod itu dengan kuat, supaya pelanggan tahu makanan mereka sudah siap. Panduan ini menunjukkan cara memasang dan menggunakannya di kaunter.')}</p>

  <div class="bubble">
    <div class="ic"><svg class="i"><use href="#bell"/></svg></div>
    <div class="lines">
      <span><b>“A, 1, 0, 5.</b> Please collect your order.”</span>
      <span style="font-size:9pt;color:#A3AAB6;font-style:italic">What customers hear · Apa yang pelanggan dengar</span>
    </div>
  </div>

  <ul class="intro-list">
    <li><svg class="i"><use href="#info"/></svg><span><b>Who it's for:</b> counter staff and supervisors.{ms('Untuk: staf kaunter dan penyelia.')}</span></li>
    <li><svg class="i"><use href="#refresh"/></svg><span><b>Version:</b> written for Queue Announcer <b>{VERSION}</b>.{ms(f'Versi: ditulis untuk Queue Announcer {VERSION}.')}</span></li>
    <li><svg class="i"><use href="#keyboard"/></svg><span><b>Language:</b> English, with Bahasa Melayu in grey under each step.{ms('Bahasa: Inggeris, dengan Bahasa Melayu (kelabu) di bawah setiap langkah.')}</span></li>
  </ul>
  {foot(1)}
</section>

<!-- PAGE 2: contents -->
<section class="page" id="contents">
  <h2 style="font-size:20pt">Contents</h2>
  <p class="intro" style="font-size:10.5pt;color:var(--soft)">Tap or click a section to jump straight to it. Every page has a <b>Contents</b> link at the bottom to come back here.{ms('Tekan atau klik bahagian untuk terus ke halaman itu. Setiap halaman ada pautan Contents di bawah untuk kembali ke sini.')}</p>
  <ul class="toc">
    <li><a href="#install"><span class="n">1</span><span class="t">Install<small>What you need and how to put it on a PC · Pemasangan</small></span><span class="dots"></span><span class="pg">P_INSTALL</span></a></li>
    <li><a href="#announce"><span class="n">2</span><span class="t">Announce an order<small>Type, announce, and what each button does · Umumkan pesanan</small></span><span class="dots"></span><span class="pg">P_ANNOUNCE</span></a></li>
    <li><a href="#recent"><span class="n">3</span><span class="t">Call again from Recent<small>Recall an order that was already called · Panggil semula</small></span><span class="dots"></span><span class="pg">P_RECENT</span></a></li>
    <li><a href="#floating"><span class="n">4</span><span class="t">Floating window<small>Keeping the announcer on top of other apps · Tetingkap terapung</small></span><span class="dots"></span><span class="pg">P_FLOATING</span></a></li>
    <li><a href="#settings"><span class="n">5</span><span class="t">Settings<small>Volume, unlocking with the PIN, and options · Tetapan</small></span><span class="dots"></span><span class="pg">P_SETTINGS</span></a></li>
    <li><a href="#fixes"><span class="n">6</span><span class="t">Quick fixes<small>What to do when something goes wrong · Penyelesaian pantas</small></span><span class="dots"></span><span class="pg">P_FIXES</span></a></li>
  </ul>
  {foot(2)}
</section>

<!-- PAGE 3: install -->
<section class="page">
  <h2 id="install"><span class="n">1</span>Install</h2>
  <h3 style="font-size:13pt">You need<span class="ms">Anda perlukan</span></h3>
  <div class="tiles big">
    <div class="tile"><div class="ib"><svg class="i"><use href="#monitor"/></svg></div><h3>Microsoft Edge</h3><p>On a computer, for the Clara voice.{ms('Di komputer, untuk suara Clara.')}</p></div>
    <div class="tile"><div class="ib"><svg class="i"><use href="#speaker"/></svg></div><h3>Speakers on</h3><p>Loud enough for the counter.{ms('Pembesar suara hidup, cukup kuat untuk kaunter.')}</p></div>
    <div class="tile"><div class="ib"><svg class="i"><use href="#wifi"/></svg></div><h3>Internet</h3><p>To start. Keeps working if it drops.{ms('Untuk mula. Masih berfungsi jika internet terputus.')}</p></div>
  </div>

  <h3 style="font-size:13pt;margin-top:4mm">Install it (one time per PC)<span class="ms">Pasang (sekali bagi setiap PC)</span></h3>
  <div class="flow three big">
    <div class="card">
      <span class="num">1</span>
      <div class="pic text"><svg class="i" style="color:#00C7B1"><use href="#monitor"/></svg><span class="url">haikalmhmn<br>.github.io/<br>queue-announcer</span></div>
      <p class="cap">Open the link in Edge{ms('Buka pautan dalam Edge')}</p>
    </div>
    {ARROW}
    <div class="card">
      <span class="num">2</span>
      <div class="pic text"><span class="menu"><span>⋯</span>›<span>Apps</span>›<span>Install this site as an app</span></span></div>
      <p class="cap">Install it{ms('Pasang aplikasi')}</p>
    </div>
    {ARROW}
    <div class="card">
      <span class="num">3</span>
      <div class="pic" style="background:#fff;box-shadow:0 0 0 1px #E3E6EB"><img src="logo.jpg" alt="" style="width:24mm;margin:3mm auto"></div>
      <p class="cap">Open from the desktop icon{ms('Buka dari ikon di desktop')}</p>
    </div>
  </div>
  {tip('refresh', '<b>Updates install themselves.</b> No need to reinstall.', 'Kemas kini dipasang sendiri. Tidak perlu pasang semula.')}
  {foot(3)}
</section>

<!-- PAGE 4: announce, steps -->
<section class="page">
  <h2 id="announce"><span class="n">2</span>Announce an order</h2>
  <div class="flow three">
    <div class="card">
      <span class="num">1</span>
      <div class="pic"><img src="crop-code.jpg" alt=""></div>
      <p class="cap">Type the code<small>From the receipt</small>{ms('Taip kod daripada resit')}</p>
    </div>
    {ARROW}
    <div class="card">
      <span class="num">2</span>
      <div class="pic"><img src="crop-actions.jpg" alt=""></div>
      <p class="cap">Tap Announce{ms('Tekan "Announce"')}</p>
    </div>
    {ARROW}
    <div class="card">
      <span class="num">3</span>
      <div class="pic"><img src="crop-speaking.jpg" alt=""></div>
      <p class="cap">Bell, then the voice<small>Wait until it finishes</small>{ms('Loceng, kemudian suara. Tunggu hingga selesai.')}</p>
    </div>
  </div>
  <div class="shotrow" style="grid-template-columns:66mm 1fr;align-items:start">
    {MAIN}
    {keybox([
        (1, 'Now calling', 'Pesanan yang sedang dipanggil'),
        (2, '<b>Repeat</b> last order', 'Ulang pesanan terakhir'),
        (3, '<b>Mute</b> (red = sound off)', 'Senyap (merah = bunyi mati)'),
        (4, '<b>✕</b> clear the code', 'Padam semua kod'),
        (5, 'Letters and numbers', 'Huruf dan nombor'),
        (6, '<b>⌫</b> delete one', 'Padam satu aksara'),
        (7, '<b>Recent</b> orders', 'Pesanan terkini'),
        (8, '<b>Announce</b>', 'Umumkan'),
        (9, '<b>Settings</b>', 'Tetapan'),
    ])}
  </div>
  <div class="tips" style="margin-top:4mm">
    {tip('clock', '<b>One at a time.</b> Type the next code while it speaks.', 'Satu pada satu masa. Taip kod seterusnya semasa ia bercakap.')}
    {tip('del', 'Up to <b>8</b> characters, e.g. <b>T-042</b>.', 'Maksimum 8 aksara, cth. T-042.')}
    {tip('keyboard', 'Keyboard: <kbd>Enter</kbd> announce, <kbd>Esc</kbd> clear.', 'Papan kekunci: Enter umumkan, Esc padam.')}
  </div>
  {foot(4)}
</section>


<!-- PAGE 6: recent -->
<section class="page">
  <h2 id="recent"><span class="n">3</span>Call again from Recent</h2>
  <div class="shotrow" style="grid-template-columns:62mm 1fr;align-items:start">
    {RECENT}
    <div style="display:flex;flex-direction:column;gap:4mm">
      {keybox([
          (1, '<b>Recall</b> plays it again', 'Recall: panggil semula'),
          (2, 'Code, time, times called', 'Kod, masa, berapa kali dipanggil'),
          (3, '<b>Back</b> to the keypad', 'Kembali ke papan kekunci'),
      ])}
      {tip('info', 'Today only, on this PC. Swipe to scroll.', 'Hari ini sahaja, di PC ini. Leret untuk skrol.')}
    </div>
  </div>
  <h2 id="floating"><span class="n">4</span>Floating window</h2>
  <div class="diagram">
    <div class="monitor">
      <div class="other">Your other work<i></i><i style="width:80%"></i><i style="width:60%"></i></div>
      <div class="float"><i class="a"></i><i></i><i></i></div>
      <div class="tab"></div>
      <span class="lbl" style="right:26%;top:6%">Announcer (stays on top)</span>
      <span class="lbl" style="right:26%;bottom:7%">Small tab: don't close</span>
    </div>
    <div class="keys">
      <div class="key"><span class="sw" style="background:#15171C;box-shadow:0 0 0 1.2px #00C7B1"></span><span><b>First tap</b>: the announcer floats on top. Drag it where you like.{ms('Tekanan pertama: announcer terapung di atas. Seret ke mana-mana.')}</span></div>
      <div class="key"><span class="sw" style="background:#15171C"></span><span><b>Small tab</b> moves to the bottom right.{ms('Tab kecil berpindah ke bawah kanan.')}</span></div>
      <div style="padding-left:9.5mm"><img src="tab.jpg" alt="Small tab" style="width:40mm;border-radius:2mm;box-shadow:0 0 0 1px #2a2d35;display:block"></div>
      <div class="key"><span></span><span><b>Bring it back</b> returns it to the main window.{ms('Tekan "Bring it back" untuk kembali ke tetingkap utama.')}</span></div>
    </div>
  </div>
  {tip('x', "<b>Don't close the small tab</b>: it closes the announcer too. Minimize it with <b>–</b> instead.", 'Jangan tutup tab kecil: announcer juga akan tertutup. Kecilkan dengan butang – sahaja.', warn=True)}
  {foot(5)}
</section>


<!-- PAGE 8: settings, locked -->
<section class="page">
  <h2 id="settings"><span class="n">5</span>Settings</h2>
  <div style="display:grid;grid-template-columns:56mm 56mm;gap:18mm;justify-content:center;padding-top:2mm">
    {LOCKED}
    {PINPAD}
  </div>
  {keybox(None, cols=[
      [(1, '<b>Volume</b>: anyone can change it', 'Kelantangan: sesiapa boleh ubah'),
       (2, '<b>Float on top</b>: anyone can use it', 'Terapung di atas: sesiapa boleh guna')],
      [(3, '<b>Unlock</b> to change anything else', 'Tekan "Unlock" untuk ubah tetapan lain'),
       (4, '<b>Reset to default settings</b>: tap twice, no PIN', 'Tetapkan semula: tekan dua kali, tanpa PIN'),
       (5, 'Type the <b>PIN</b> from IT', 'Masukkan PIN daripada IT')],
  ])}
  <div class="tips">
    {tip('clock', 'Locks again when you leave, or after <b>2 minutes</b>.', 'Berkunci semula bila keluar, atau selepas 2 minit.')}
    {tip('x', '<b>5 wrong tries</b>: wait 30 seconds.', '5 kali salah: tunggu 30 saat.', warn=True)}
    {tip('info', "Don't know the PIN? Ask <b>IT</b>.", 'Tak tahu PIN? Tanya IT.')}
  </div>
  {foot(6)}
</section>

<!-- PAGE 9: settings, unlocked -->
<section class="page">
  <h2 style="font-size:15pt">Settings, unlocked<span class="ms">Tetapan, selepas dibuka</span></h2>
  <div style="display:grid;grid-template-columns:repeat(3,48mm);gap:10mm;justify-content:center;padding-top:2mm">
    {S_TOP}
    {S_MID}
    {S_BOT}
  </div>
  {keybox(None, cols=[
      [(6, '<b>Lock now</b>', 'Kunci sekarang'), (7, '<b>Voice</b>: Clara', 'Suara: Clara'),
       (8, '<b>Speed</b> of the words', 'Kelajuan sebutan')],
      [(9, 'Say it 1, 2 or 3 times', 'Sebut 1, 2 atau 3 kali'), (10, '<b>Bell</b> on / off', 'Loceng hidup / mati'),
       (11, 'Bell sound + <b>Test</b>', 'Bunyi loceng + uji')],
      [(12, 'What will be said', 'Apa yang akan disebut'), (13, '<b>Test voice</b>', 'Uji suara'),
       (14, 'Float at first tap', 'Terapung pada tekanan pertama')],
  ])}
  {tip('info', 'Each PC keeps its own settings. <b>Reset to default</b> brings back: volume 100%, Normal speed, said once, bell on.', 'Setiap PC simpan tetapan sendiri. Reset kembalikan: kelantangan 100%, kelajuan Normal, sebut sekali, loceng hidup.')}
  {foot(7)}
</section>

<!-- PAGE 10: quick fixes -->
<section class="page" style="gap:4.5mm">
  <h2 id="fixes"><span class="n">6</span>Quick fixes</h2>
  <div class="fixes">
    <div class="fix"><div class="ib"><svg class="i"><use href="#muted"/></svg></div><div><h3>No sound</h3><p>Mute not red? Volume up in Settings? Edge not muted in Windows <b>Volume mixer</b>?{ms('Tiada bunyi: Mute merah? Kelantangan rendah? Edge disenyapkan dalam Volume mixer?')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#bell"/></svg></div><div><h3>Bell plays, no voice</h3><p>Check Edge isn't muted, then tap <b>Repeat</b>. Check the internet.{ms('Loceng berbunyi, tiada suara: pastikan Edge tidak senyap, tekan Repeat. Semak internet.')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#robot"/></svg></div><div><h3>Voice sounds robotic</h3><p>Open from the desktop icon, not another browser. Update Edge.{ms('Suara seperti robot: buka dari ikon desktop, bukan pelayar lain. Kemas kini Edge.')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#window"/></svg></div><div><h3>No floating window</h3><p>Settings → <b>Float on top of other apps</b>. Edge on a computer only.{ms('Tiada tetingkap terapung: Settings → "Float on top of other apps". Edge di komputer sahaja.')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#x"/></svg></div><div><h3>Announcer disappeared</h3><p>The small tab was closed. Open the app again from the desktop icon.{ms('Announcer hilang: tab kecil telah ditutup. Buka semula dari ikon desktop.')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#info"/></svg></div><div><h3>Don't know the PIN</h3><p>Ask <b>IT</b>. Volume and Float on top work without it.{ms('Tak tahu PIN: tanya IT. Kelantangan dan Float on top boleh guna tanpa PIN.')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#refresh"/></svg></div><div><h3>Settings changed by mistake</h3><p>Settings → <b>Reset to default settings</b>, tap it twice.{ms('Tetapan berubah: Settings → "Reset to default settings", tekan dua kali.')}</p></div></div>
    <div class="fix"><div class="ib"><svg class="i"><use href="#refresh"/></svg></div><div><h3>Need the newest version</h3><p>Close the app fully and reopen. Check <b>About &amp; version</b>.{ms('Versi terkini: tutup app sepenuhnya dan buka semula. Semak "About &amp; version".')}</p></div></div>
  </div>
  <h2 style="font-size:15pt">Which version am I on?<span class="ms">Saya guna versi mana?</span></h2>
  <div class="shotrow" style="grid-template-columns:42mm 1fr;align-items:center">
    {ABOUT}
    {keybox([
        (1, 'Version number and who made it', 'Nombor versi dan pembuatnya'),
        (2, 'Up to date or not', 'Terkini atau tidak'),
        (3, 'What changed (older versions below)', 'Apa yang berubah (versi lama di bawah)'),
    ])}
  </div>
  <h3 style="font-size:13pt">Quick reference<span class="ms">Rujukan pantas</span></h3>
  <div class="quick">
    <div class="q"><span>Call <span class="ms">· Panggil</span></span><b>Code → Announce</b></div>
    <div class="q"><span>Again <span class="ms">· Ulang</span></span><b>Repeat · Recall</b></div>
    <div class="q"><span>Silence <span class="ms">· Senyap</span></span><b>Mute</b></div>
    <div class="q"><span>Fix typing <span class="ms">· Betulkan</span></span><b>⌫ one · ✕ all</b></div>
  </div>
  {foot(8)}
</section>

"""

PAGES = {'P_INSTALL': 3, 'P_ANNOUNCE': 4, 'P_RECENT': 5, 'P_FLOATING': 5, 'P_SETTINGS': 6, 'P_FIXES': 8}
for k, v in PAGES.items():
    BODY = BODY.replace(k, str(v))

html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<title>%s Staff Guide v%s</title>\n<style>%s%s</style>\n</head>\n<body>\n\n%s\n%s\n</body>\n</html>\n'
        % (NAME, VERSION, BASE_CSS, EXTRA_CSS, ICONS, BODY))
open(os.path.join(HERE, 'guide.html'), 'w', encoding='utf-8').write(html)
print('guide.html written')
