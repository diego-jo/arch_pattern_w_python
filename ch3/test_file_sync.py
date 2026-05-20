from pathlib import Path
import shutil
import tempfile

from file_sync import sync


def test_when_file_exists_in_source_but_not_in_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        # source = "./source"
        # dest = "./dest"

        content = "### this is a md file"
        (Path(source) / "file.md").write_text(content)

        sync(source, dest)

        expected_path = Path(dest) / "file.md"
        assert expected_path.exists()
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_when_file_exists_in_source_but_with_different_name_in_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "### this is a md file"
        (Path(source) / "file.md").write_text(content)
        (Path(dest) / "other.md").write_text(content)

        sync(source, dest)

        expected_other_file = Path(dest) / "other.md"
        expected_renamed_file = Path(dest) / "file.md"

        assert expected_renamed_file.exists()
        assert not expected_other_file.exists()
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_when_file_exists_in_destination_but_not_in_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "### this is a md file"
        (Path(dest) / "file.md").write_text(content)

        sync(source, dest)

        expected_path = Path(dest) / "file.md"
        assert not expected_path.exists()
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
