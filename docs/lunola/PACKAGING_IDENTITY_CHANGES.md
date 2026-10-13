# Packaging display identity — Lunola Forma by Pujo Setyo

## Status dan batas bukti

Implementasi source/template, bukan sertifikasi paket atau dukungan lintas platform.
Dasar keputusan: audit native identity untuk branch `brand/complete-lunola-identity`.
Perubahan dibatasi ke tujuh file produksi berikut, satu test host, dan laporan ini.
Tidak ada build aplikasi/paket, install, register/unregister, perubahan preferensi,
operasi Git/index, commit, atau push yang dijalankan oleh pekerjaan packaging ini.

## Perubahan exact dan klasifikasi

A = branding tampilan; B = tautan produk; C = metadata distribusi;
D = compatibility identity/path; E = legal/attribution; F = service eksternal.

| Path | Kategori | Perubahan |
|---|---|---|
| `build_files/cmake/packaging.cmake` | A, B, C | `PROJECT_DESCRIPTION` menjadi `Lunola Forma - Professional 3D Creation Suite, based on Blender.`; `PROJECT_VENDOR` menjadi `Pujo Setyo`; `PROJECT_CONTACT` kosong karena tidak ada email distributor terverifikasi. Tambah `CPACK_PACKAGE_NAME="Lunola Forma"` dan prefix arsip `LUNOLA_PACKAGE_ARCHIVE_NAME="lunola-forma"`. Prefix default CPack dan `add_package_archive` macOS/Unix memakai variabel baru; versi/revision/date/architecture dan override eksplisit tetap. Label pasangan `CPACK_PACKAGE_EXECUTABLES` menjadi `Lunola Forma ${MAJOR_VERSION}.${MINOR_VERSION}`; token executable tetap `blender-launcher`. `CPACK_CREATE_DESKTOP_LINKS` hanya berisi token executable tersebut, bukan pasangan label. |
| `release/windows/installer_wix/WIX.template` | A, B, F | Progress `Registering Blender` menjadi `Registering Lunola Forma`, dengan Action tetap `RegisterBlender`. Checkbox keluar menjadi `Visit the Lunola Forma project and support`, default `0` (tidak opt-in otomatis). Action `LaunchBrowser` membuka repositori resmi, bukan promosi/donasi upstream; query tracking donasi upstream dihapus. |
| `release/windows/msix/AppxManifest.xml.template` | A, C | Properties `DisplayName`, visual `DisplayName` dan tile `ShortName` menjadi `Lunola Forma [VERSION]`; `PublisherDisplayName` menjadi `Pujo Setyo`. Description menyebut Professional 3D Creation Suite, based on Blender. Suffix tampilan `[LTSORNOT]` tidak digunakan agar tidak menjanjikan LTS produk; signed `[PACKAGETYPE]` dan seluruh Identity tetap. |
| `release/windows/icons/winblender.rc` | C | Hanya `CompanyName`: `Blender Foundation` → `Pujo Setyo`. ProductName/FileDescription yang sudah Lunola Forma tetap. |
| `release/darwin/Blender.app/Contents/Info.plist` | A, C | Hanya `CFBundleName` menjadi Lunola Forma, distributor dalam `CFBundleGetInfoString` menjadi Pujo Setyo dengan token versi tetap, dan tiga privacy prompt mengganti `A Blender extension` menjadi `A Lunola Forma extension`. |
| `release/freedesktop/blender.desktop` | A | Hanya `Name=Blender` → `Name=Lunola Forma`; copy generik/terjemahan tetap. |
| `release/freedesktop/org.blender.Blender.metainfo.xml` | A, B, C, E, F | Name/summary/description menyebut Lunola Forma, based on Blender, distributed by Pujo Setyo; upstream authors/contributors tetap diakui dan tidak ada klaim endorsement. Homepage/vcs-browser/contribute menuju repositori resmi; bugtracker/help menuju `/issues`. Slot FAQ/donation/translation upstream dihapus karena bukan layanan produk. Empat screenshot upstream dan blok screenshots dihapus: tidak disajikan sebagai screenshot Lunola. Riwayat releases upstream tetap byte-identik dan kini dijelaskan eksplisit dalam deskripsi sebagai upstream Blender releases, bukan rilis Lunola Forma. |

Tujuan resmi yang diberikan untuk pekerjaan ini: `https://github.com/pujosety/Lunola-Forma`.
Issues aktif dan releases kosong menurut konteks verifikasi proyek; pekerjaan ini tidak
menambahkan tautan unduhan/release palsu, situs, email, FAQ, tutorial, atau donasi produk.
Tidak ada verifikasi jaringan baru atau submission issue dari suite host ini.

## Pengecualian preservasi — D, E, F

- **D:** `CPACK_RPM_PACKAGE_NAME` dipin ke `${PROJECT_NAME_LOWER}` (Blender →
  `blender`) agar technical RPM name tidak ikut turun dari display label berspasi.
  Perilaku default ini diperiksa pada module CPackRPM CMake lokal dan nilai config
  `blender` diverifikasi di fixture; bukan build RPM.
- **D:** install directory dan registry key Windows tetap
  `Blender Foundation/Blender ${MAJOR_VERSION}.${MINOR_VERSION}`. Namespace UUID
  dan rumus UpgradeGUID tidak diubah. Project/target names tetap.
- **D:** semua WiX action IDs, `FileKey="CM_FP_Blender.blender_launcher.exe"`,
  custom registration/unregistration commands, sequence dan kondisi tetap.
  Suite tidak menjalankan action tersebut. Nama tampilan bukan migrasi coexistence.
- **D:** MSIX signed Name/Publisher, application ID `BLENDER`, executable paths,
  architecture/version placeholders, protocol, execution alias, `.blend` association,
  resources, logos, capabilities dan dependencies tetap. PublisherDisplayName
  bukan perubahan publisher sertifikat; manifest belum siap dipublikasikan sebagai
  identitas signed Lunola tanpa review signing/coexistence terpisah.
- **D:** macOS `CFBundleExecutable`, bundle path/identifier, UTI, document declarations,
  icon names/resources dan actual version tokens tetap, termasuk label format/ikon
  `Blender File` yang bukan nama produk dalam batch ini.
- **D:** Linux desktop filename, Exec/Icon, MIME, StartupWMClass, AppStream application
  ID `org.blender.Blender` dan launchable `blender.desktop` tetap. Shared identity
  masih dapat bertabrakan dengan upstream; tidak mengklaim instalasi berdampingan aman.
- **E:** COPYRIGHT/SPDX, `PROJECT_COPYRIGHT`, LegalCopyright RC, COPYING/AUTHORS,
  GPL/metadata license dan notice upstream tidak diganti dengan nama distributor.
- **F:** selain promosi donasi/slot layanan produk yang disebut di atas, dependency,
  build-service dan API upstream tidak diarahkan ulang.
- Assets approved, ICO/PNG/BMP/ICNS dan payload logo tidak diedit oleh pekerjaan ini.
  Snap metadata, diagnostic scripts, thumbnailer-extension metadata dan seam native
  source di luar daftar bukan bagian batch ini; jangan menganggap inventaris ini
  menuntaskan semua branding installer/platform.

## Tests dan hasil nyata

Test baru: `tools/lunola/qa/test_packaging_identity.py`.

Setiap slice produksi (CPack, WiX, MSIX, macOS, desktop, RC dan AppStream) lebih dulu
memiliki test tampilan yang dijalankan dan gagal karena copy produk belum ada (RED),
lalu edit scoped dan test lulus (GREEN). Suite mengembalikan hanya edit yang diizinkan
ke bytes awal dan membandingkan SHA-256 seluruh file. Ini memeriksa bahwa semua bytes
lain — termasuk IDs, paths, association actions dan legal text — tetap. CRLF sumber
juga dipertahankan. XML WiX/MSIX dengan substitusi placeholder fixture dan AppStream
berhasil diparse; plist berhasil dibaca dengan `plistlib`.

Command dari root repo pada host bash:

```bash
LUNOLA_TEST_CMAKE='D:/DevTools/VisualStudio/2022/Community/Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe' python tools/lunola/qa/test_packaging_identity.py
```

**Hasil: 8 tests, OK, exit 0.** Tanpa executable CMake pada PATH atau environment
`LUNOLA_TEST_CMAKE`, tujuh checks tetap dijalankan dan test konfigurasi di-skip;
itu tidak setara dengan hasil delapan checks penuh di atas.

Check kedelapan benar-benar menjalankan CMake configure-only pada fixture scratch
`project(Blender LANGUAGES NONE)` tanpa `.git`; tidak mengeksekusi command Git di
packaging.cmake, tidak mengompilasi, tidak menjalankan CPack/package target atau
menginstal. CPackConfig nyata memuat product/vendor/shortcut/desktop-token/prefix
arsip yang diharapkan. Fixture versi 5.4.0 dipakai hanya sebagai input test, bukan
rilis produk. Install directory/registry key dan UUID v5 UpgradeGUID dibandingkan
terhadap formula asli untuk input fixture. Kontak kosong dihilangkan oleh serializer
CPack dan tidak lagi memuat email upstream.

## Gates yang masih tersisa

- Build/package terpisah setelah izin, inspeksi generated WiX/MSI Directory,
  Shortcut, File dan CustomAction tables: terutama memastikan file-key references
  masih cocok setelah perubahan display product name.
- Validasi schema/tool platform native (WiX/MSIX SDK, plutil, desktop-file-validate,
  appstreamcli), signing/certificate mapping dan preview software-center.
  XML/plist parse host bukan schema-validation atau bukti UI native.
- Screenshot Lunola yang benar beserta hak artwork; keputusan AppStream release
  provenance/catalog presentation sebelum distribusi. Riwayat upstream yang masih
  dipreservasi tidak boleh dianggap daftar release produk.
- Uji runtime/GUI Windows, macOS dan Linux; isolated upgrade/coexistence review,
  shortcut/menu/privacy, clean-machine release checks setelah izin. Tidak ada
  asosiasi OS atau preferensi pengguna yang diubah untuk menyelesaikan gate ini.
