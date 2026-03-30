import os

import pytest

from parade.print.cli import _default_filename, main


class TestDefaultFilename:
    def test_basic(self):
        assert _default_filename(2026, 6) == "parade_2026_6y.pdf"

    def test_single_year(self):
        assert _default_filename(2026, 1) == "parade_2026_1y.pdf"

    def test_large_count(self):
        assert _default_filename(2030, 12) == "parade_2030_12y.pdf"


class TestPrintCli:
    def test_generates_pdf_with_default_name(self, capsys, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        main(["--start", "2026", "--years", "2"])
        captured = capsys.readouterr()
        expected = "parade_2026_2y.pdf"
        assert expected in captured.out
        assert (tmp_path / expected).exists()

    def test_generates_pdf_with_custom_output(self, capsys, tmp_path):
        output = str(tmp_path / "custom.pdf")
        main(["--start", "2026", "--years", "2", "--output", output])
        assert os.path.exists(output)

    def test_rejects_zero_years(self):
        with pytest.raises(SystemExit):
            main(["--start", "2026", "--years", "0"])

    def test_rejects_negative_years(self):
        with pytest.raises(SystemExit):
            main(["--start", "2026", "--years", "-1"])

    def test_missing_start_exits(self):
        with pytest.raises(SystemExit):
            main(["--years", "2"])

    def test_missing_years_exits(self):
        with pytest.raises(SystemExit):
            main(["--start", "2026"])
