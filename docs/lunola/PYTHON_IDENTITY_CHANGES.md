# Perubahan Python UI identity — Lunola Forma

## Cakupan dan taxonomy publik

Implementasi sumber pada branch `brand/complete-lunola-identity`; baseline audit/test `f55fdf13a57992398b3b1535e5da5b879774d0cf`. Perubahan tetap **uncommitted**; tidak ada build, commit, staging, push, telemetry, attachment otomatis, perubahan konfigurasi pengguna, asosiasi OS, atau request jaringan dari pekerjaan ini.

Taxonomy publik mengikuti permintaan pengguna: **A branding, B links/routing, C metadata, D compatibility, E legal, F services**. Audit sumber memakai C=upstream, D=legal, E=compatibility; laporan ini menormalisasi C audit menjadi B/F publik, D audit menjadi E publik, E audit menjadi D/C publik. Kategori tidak menunjukkan bahwa semua literal Blender harus dihapus.

## B — Routing standalone yang aman bagi privasi

`scripts/modules/_bpy_internal/system_info/url_prefill_startup.py:main()` sekarang membaca konstanta produk `LUNOLA_BUG_REPORT_URL` dari modul pusat `_lunola_urls.py` yang dikirim bersama instalasi. `runpy.run_path` memakai path absolut relatif terhadap file script agar pemanggilan langsung tetap bekerja tanpa `bpy`, tanpa dependency pada working directory, dan tanpa menulis/mengubah `sys.path` atau konfigurasi pengguna.

Main tidak lagi memanggil `url_from_blender()`, menjalankan executable `--version`, mengambil OS/GPU, ataupun membangun query diagnostic. Ia membuka tujuan issue GitHub tanpa query/fragment; console menyebut GitHub, kebutuhan sign-in, tidak adanya system information di URL, dan kewajiban review/redaction sebelum pengguna membagikan detail. Tidak ada form submission atau upload otomatis. Endpoint ditetapkan/terverifikasi oleh pekerjaan modul pusat; suite ini memeriksa kontrak literal lokal, bukan mengklaim verifikasi jaringan baru atau keberhasilan login.

Signature `main() -> int`, `url_from_blender() -> str`, serta `__all__` tetap. `url_from_blender` tetap helper eksplisit untuk upstream; parser `^Blender (.*)`, nama executable `MacOS/Blender`, `Blender.exe`, `blender`, parameter dan real build fields tidak diganti. Helper tersebut masih menghasilkan query upstream bila **dipanggil eksplisit**; jangan menafsirkannya sebagai route produk atau route tanpa diagnostic. `url_prefill_runtime.url_from_blender` juga tetap upstream, bukan diarahkan ulang untuk semua add-on. Browser open mengikuti kontrak sebelumnya (return main 0 setelah pemanggilan); suite tidak menjamin browser terpasang atau navigasi sukses.

## A — Perubahan copy literal yang tepat

Tabel berikut adalah allowlist replacement; penggantian hanya pada file yang disebut, bukan replace global. Frasa parsial pada baris built/support/offline berlaku untuk semua kemunculan frasa tersebut dalam file, sementara placeholder, nama library dan flag tetap.

| File | Sebelum | Sesudah |
|---|---|---|
| `scripts/startup/bl_ui/space_userpref.py` | `Load Factory Blender Preferences` | `Load Factory Lunola Forma Preferences` |
| `scripts/startup/bl_ui/space_userpref.py` | `Blender Version` | `Blender Engine Version` |
| `scripts/startup/bl_ui/space_userpref.py` | `A restart of Blender is required` | `A restart of Lunola Forma is required` |
| `scripts/startup/bl_ui/space_userpref.py` | `Open blend files with this Blender version` | `Open blend files with this Lunola Forma version` |
| `scripts/startup/bl_operators/assets.py` | `Blender sub-process exited with error code {:d}` | `Lunola Forma sub-process exited with error code {:d}` |
| `scripts/startup/bl_operators/project.py` | `Project configuration is newer than this version of Blender supports` | `Project configuration is newer than this version of Lunola Forma supports` |
| `scripts/startup/bl_operators/image.py` | `and Blender has rights to launch it` | `and Lunola Forma has rights to launch it` |
| `scripts/startup/bl_operators/image_as_planes.py` | `Force reload the image if it is already opened elsewhere in Blender` | `Force reload the image if it is already opened elsewhere in Lunola Forma` |
| `scripts/addons_core/rigify/ui.py` | `Get active/selected colors from current Blender theme` | `Get active/selected colors from current Lunola Forma theme` |
| `scripts/addons_core/rigify/ui.py` | `Set the color palette to match Blender's active theme for selected and active bones` | `Set the color palette to match Lunola Forma's active theme for selected and active bones` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `If the lock was held by a Blender instance that exited unexpectedly,` | `If the lock was held by a Lunola Forma or upstream Blender instance that exited unexpectedly,` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `Launch Blender without --offline-mode` | `Launch Lunola Forma without --offline-mode` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `either wait until the operation is finished or restart Blender` | `either wait until the operation is finished or restart Lunola Forma` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `Warning! Before unlocking, ensure another instance of Blender is not running.` | `Warning! Before unlocking, ensure no Lunola Forma or upstream Blender instance is using this repository.` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `Blender was launched in offline mode, which cannot be changed at runtime` | `Lunola Forma was launched in offline mode, which cannot be changed at runtime` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `Allow Blender to access the internet.` | `Allow Lunola Forma to access the internet.` |
| `scripts/addons_core/bl_pkg/bl_extension_ops.py` | `However, Blender cannot prevent third-party add-ons from` | `However, Lunola Forma cannot prevent third-party add-ons from` |
| `scripts/modules/_bpy_internal/system_info/text_generate_runtime.py` | `= Blender {:s} System Information =` | `= Lunola Forma {:s} System Information =` |
| `scripts/modules/_bpy_internal/system_info/text_generate_runtime.py` | `title("Blender")` | `title("Blender Engine Build")` |
| `scripts/modules/_bpy_internal/system_info/text_generate_runtime.py` | `Blender was built` | `Lunola Forma was built` |
| `scripts/modules/_bpy_internal/system_info/url_prefill_startup.py` | `Follow our guide to collect this information:` | `Follow the upstream Blender guide to collect this information:` |
| `scripts/modules/_bpy_internal/system_info/url_prefill_startup.py` | `Blender did not provide any build information. Blender may be corrupt or blocked from running.` | `Lunola Forma did not provide any build information. Lunola Forma may be corrupt or blocked from running.` |
| `scripts/modules/_bpy_internal/system_info/url_prefill_startup.py` | `Please try reinstalling Blender and double check your anti-virus isn't blocking it from running.` | `Please try reinstalling Lunola Forma and double check your anti-virus isn't blocking it from running.` |
| `scripts/addons_core/bl_pkg/bl_extension_ui.py` | `Add-ons previously shipped with Blender are now available from extensions.blender.org.` | `Add-ons previously shipped with upstream Blender are now available from extensions.blender.org.` |
| `scripts/addons_core/bl_pkg/bl_extension_ui.py` | `Blender's extension repository` | `Upstream Blender extension repository` |
| `scripts/addons_core/bl_pkg/bl_extension_ui.py` | `Visit Extensions Platform` | `Visit Upstream Blender Extensions` |
| `scripts/addons_core/bl_pkg/bl_extension_ui.py` | `Internet access is required to install and update online extensions.` | `Internet access is required for the selected upstream or third-party extension repositories.` |

## A/B/D/F — Penyesuaian display di luar replacement literal

- `space_userpref.py`: doc/tracker memakai `Add-on Documentation` / `Report Add-on Bug` untuk add-on pengguna, dan `Upstream Add-on Documentation` / `Report Upstream Add-on Bug` untuk bundled core berdasarkan `user_addon` yang sudah tersedia. URL tetap `bl_info["doc_url"]` / `bl_info["tracker_url"]`; author dan metadata tidak ditulis ulang. Referensi experimental/developer diberi prefix display `Upstream: `; semua issue/project target dan komposisi URL asli tetap.
- `bl_extension_ui.py`: doc/tracker expanded-item memakai `Upstream Add-on Website` / `Upstream Add-on Feedback` hanya ketika `addon_type == ADDON_TYPE_LEGACY_CORE`; selain itu `Add-on / Extension Website` / `Add-on / Extension Feedback`. Domain dan tujuan tetap dari publisher metadata. Tombol installing extensions yang sebelumnya icon-only sekarang `Upstream Extension Manual`; locale, engine version, deep path dan anchor tetap.
- `rna_keymap_ui.py`: pilihan canonical `kc_active.name == "Blender"` dan fallback display kosong mendapat alias `Lunola Forma (Blender-compatible)`. Keyconfig lain tetap display name aslinya. Tidak menulis ke keyconfig, tidak rename preset/theme, tidak mengubah serialization. Canonical `default_config = "Blender"` tetap di `bpy/utils/__init__.py`.
- `text_generate_runtime.py`: setelah header ditambah `Lunola Forma by Pujo Setyo; based on the Blender engine.` dan `Review and redact local paths and add-on details before sharing this file.` Ini byline produk dan peringatan lokal, bukan replacement copyright Blender. Semua nilai versi/hash/build flags, direktori, daftar add-on, probe GPU/library/Cycles, serta perilaku penulisan diagnostic tetap. File diagnostic **masih dapat berisi path sensitif**; warning bukan otomatis redaction.
- `bl_extension_ops.py`: lock-warning secara eksplisit mencakup instance Lunola Forma **atau upstream Blender yang memakai repository yang sama**. Algoritma lock/unlock, polling, online/offline gating, flag `--offline-mode`, serta peringatan bahwa add-on pihak ketiga dapat mengabaikan online setting tidak dilemahkan.

## C/D/E/F — Exception yang disengaja

- Copyright/author/SPDX, seluruh `bl_info` termasuk key `blender`, engine/API/RNA/operator/module identifiers, enum/data format, preset/template names, preference property paths dan persisted configuration tetap. Statusbar berlabel **Blender Engine Version** agar tidak mengklaim nilai engine sebagai marketing version Forma.
- URL manual/API/developer-guide/extension deep links, extension API endpoint, repository matching, package IDs, `X-Blender`, user agent `Blender/...`, compatibility versions/min-max dan extension startup-sync/nonblocking-update flow tetap upstream/third-party. Tidak ada layanan atau updater Forma yang diciptakan.
- Exporter provenance glTF/Khronos, FBX, UV EPS/SVG dan translation-generated legal notices tidak direbrand. Metadata ekspor membutuhkan audit importer/provenance terpisah.
- Application templates 2D Animation, Sculpting, Storyboarding, Video Editing tetap utuh. `Blender Unit`, `.blend`/data-block descriptions dan engine-addon minimum-version messages tetap sebagai terminologi compatibility; neutralization opsional dari audit tidak dibutuhkan untuk route/display produk ini.
- Translation-source repository tooling serta Rigify feature-set publisher names/links dipertahankan. Identitas publisher/add-on tersebut bukan identitas produk utama. Tidak ada redirect massal.
- Perbaikan optional double slash pada experimental URL tidak diambil; komposisi URL dan identifier tetap. File parent `wm.py`, `space_topbar.py`, `_lunola_urls.py` dibaca tetapi tidak ditulis oleh pekerjaan ini.

## Validasi dan batas bukti

Tests ditambahkan sebelum perubahan perilaku: standalone routing RED karena main memanggil helper diagnostic; safe-copy RED pada 27 subtest replacement; alias keyconfig dan external labels RED karena label/guard belum ada; diagnostic-byline RED karena belum ada byline. Masing-masing implementasi kemudian GREEN. Pengujian regression preservation ditambahkan sebagai guard terhadap baseline audit.

Perintah dari root repository:

```text
python tools/lunola/qa/test_python_identity.py
python -B tools/lunola/qa/test_project_links.py
git -c core.safecrlf=false diff --check -- scripts ':!scripts/startup/bl_operators/wm.py' ':!scripts/startup/bl_ui/space_topbar.py' ':!scripts/modules/_lunola_urls.py'
```

Hasil: **8 host/source tests PASS**, **2 project-link tests PASS**, scoped `git diff --check` exit 0. Suite identity membutuhkan Git dan baseline commit di atas untuk guard provenance/contract. Seluruh AST file yang diubah dibandingkan dengan baseline + allowlist copy/display tepat; body main dikecualikan dari perbandingan tersebut tetapi signature tetap dibandingkan dan body diuji terpisah. Guard mencakup API, flags, preference paths, lock/gating, deep links, build fields dan notices. Source add-on metadata, service/download modules, CLI compatibility, manual mappings, exporter provenance dan empat application template juga dibandingkan dengan baseline.

Tes route menjalankan fungsi nyata dan entry `__main__` di interpreter host isolated `-I -B`; hanya sink `webbrowser.open` diintersep supaya **tidak membuka browser atau mengirim request**. `bpy` tidak dimock/import; label conditional diuji sebagai ekspresi AST saja. Ini bukti Python host/source, **bukan** Blender/Lunola runtime, GUI, installer, build baru, import keymap round-trip, pengujian lock concurrency, offline runtime, atau ketersediaan endpoint jaringan. Gate aplikasi tersebut tetap belum dijalankan.

Working tree sejak awal berisi perubahan parent dan lima gitlink `lib/*` deleted; pekerjaan ini tidak membuat atau memperbaiki state tersebut. Git menampilkan warning CRLF/LF pada diff biasa; tidak ada normalisasi newline massal atau staging dilakukan.

## File yang ditulis oleh pekerjaan ini

- `scripts/addons_core/bl_pkg/bl_extension_ops.py`
- `scripts/addons_core/bl_pkg/bl_extension_ui.py`
- `scripts/addons_core/rigify/ui.py`
- `scripts/modules/_bpy_internal/system_info/text_generate_runtime.py`
- `scripts/modules/_bpy_internal/system_info/url_prefill_startup.py`
- `scripts/modules/rna_keymap_ui.py`
- `scripts/startup/bl_operators/assets.py`
- `scripts/startup/bl_operators/image.py`
- `scripts/startup/bl_operators/image_as_planes.py`
- `scripts/startup/bl_operators/project.py`
- `scripts/startup/bl_ui/space_userpref.py`
- `tools/lunola/qa/test_python_identity.py`
- `docs/lunola/PYTHON_IDENTITY_CHANGES.md`
