import unittest

from update import EL_TRECE_REFERRER, EL_TRECE_URL, patch_playlist


class PatchPlaylistTests(unittest.TestCase):
    def test_replaces_only_el_trece(self):
        source = (
            '#EXTM3U x-tvg-url="https://example.test/guide.xml"\n'
            '#EXTINF:-1 tvg-id="Other.ar@SD" group-title="Argentina",Other TV\n'
            'https://example.test/other.m3u8\n'
            '#EXTINF:-1 tvg-id="ElTrece.ar@SD" group-title="Argentina",El Trece (1080p)\n'
            '#EXTVLCOPT:http-referrer=https://old.example\n'
            'http://15.204.246.24:8080/eltreceHD/index.m3u8\n'
            '#EXTINF:-1 tvg-id="Another.ar@SD" group-title="Argentina",Another TV\n'
            'https://example.test/another.m3u8\n'
        )

        result = patch_playlist(source)

        self.assertIn("https://example.test/other.m3u8", result)
        self.assertIn("https://example.test/another.m3u8", result)
        self.assertIn(
            f"#EXTVLCOPT:http-referrer={EL_TRECE_REFERRER}\r\n{EL_TRECE_URL}",
            result,
        )
        self.assertNotIn("http://15.204.246.24:8080/eltreceHD/index.m3u8", result)
        self.assertNotIn("https://old.example", result)

    def test_fails_if_el_trece_disappears(self):
        source = (
            "#EXTM3U\n"
            '#EXTINF:-1 tvg-id="Other.ar@SD",Other TV\n'
            "https://example.test/other.m3u8\n"
        )
        with self.assertRaises(RuntimeError):
            patch_playlist(source)

    def test_fails_if_multiple_el_trece_entries_exist(self):
        source = (
            "#EXTM3U\n"
            '#EXTINF:-1 tvg-id="ElTrece.ar@SD",El Trece\n'
            "https://example.test/a.m3u8\n"
            '#EXTINF:-1 tvg-id="ElTrece.ar@HD",El Trece\n'
            "https://example.test/b.m3u8\n"
        )
        with self.assertRaises(RuntimeError):
            patch_playlist(source)


if __name__ == "__main__":
    unittest.main()
