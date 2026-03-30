import os
import tempfile

from parade.print.renderer import render_ephemeris_pdf


class TestRenderEphemerisPdf:
    def test_creates_pdf_file(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 2, path)
            assert os.path.exists(path)
            assert os.path.getsize(path) > 0
        finally:
            os.unlink(path)

    def test_single_year_creates_one_page(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 1, path)
            page_count = _count_pdf_pages(path)
            assert page_count == 1
        finally:
            os.unlink(path)

    def test_two_years_creates_one_page(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 2, path)
            page_count = _count_pdf_pages(path)
            assert page_count == 1
        finally:
            os.unlink(path)

    def test_three_years_creates_two_pages(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 3, path)
            page_count = _count_pdf_pages(path)
            assert page_count == 2
        finally:
            os.unlink(path)

    def test_six_years_creates_three_pages(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 6, path)
            page_count = _count_pdf_pages(path)
            assert page_count == 3
        finally:
            os.unlink(path)

    def test_pdf_contains_year_numbers(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 2, path)
            content = _read_pdf_text(path)
            assert "2026" in content
            assert "2027" in content
        finally:
            os.unlink(path)

    def test_pdf_contains_month_names(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 1, path)
            content = _read_pdf_text(path)
            assert "Jan" in content
            assert "Dec" in content
        finally:
            os.unlink(path)

    def test_pdf_contains_page_numbers(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            render_ephemeris_pdf(2026, 4, path)
            content = _read_pdf_text(path)
            assert "[1/2]" in content
            assert "[2/2]" in content
        finally:
            os.unlink(path)


def _count_pdf_pages(path: str) -> int:
    with open(path, "rb") as f:
        data = f.read()
    return data.count(b"/Type /Page") - data.count(b"/Type /Pages")


def _read_pdf_text(path: str) -> str:
    import base64
    import re
    import zlib

    with open(path, "rb") as f:
        data = f.read()

    texts = []

    # Extract from content streams (ASCII85Decode + FlateDecode)
    # Find stream objects: they have a pattern like ">>\nstream\ndata~>\nendstream\n"
    idx = 0
    while True:
        # Find ">>\nstream\n" which marks the start of actual stream content
        stream_idx = data.find(b">>\nstream\n", idx)
        if stream_idx == -1:
            break

        # Actual stream data starts after ">>\nstream\n"
        stream_start = stream_idx + 10  # len(">>\nstream\n")

        # Find the end of the stream
        end_idx = data.find(b"~>", stream_start)
        if end_idx == -1:
            idx = stream_idx + 1
            continue

        # Extract the ASCII85-encoded stream
        ascii85_data = data[stream_start:end_idx]

        # Decode ASCII85
        try:
            decoded = base64.a85decode(ascii85_data)
        except Exception:
            idx = end_idx + 1
            continue

        # Decompress with zlib
        try:
            decompressed = zlib.decompress(decoded)
        except Exception:
            idx = end_idx + 1
            continue

        # Extract text from parentheses in PDF text operations
        # Pattern: (text) Tj or similar
        text_matches = re.findall(rb"\(([^)]*)\)", decompressed)
        for t in text_matches:
            try:
                decoded_text = t.decode("latin-1", errors="ignore")
                if decoded_text.strip() and decoded_text not in texts:
                    texts.append(decoded_text)
            except Exception:
                pass

        idx = end_idx + 1

    return " ".join(texts)
