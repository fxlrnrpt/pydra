"""Tests for config file loader."""

import json
import tempfile
from pathlib import Path

import pytest

from pydraconf.config_loader import find_root_dir, load_config_dirs, substitute_variables


class TestLoadConfigDirs:
    """Tests for load_config_dirs function."""

    def test_load_from_pydraconfrc(self):
        """Test loading config_dirs from .pydraconfrc."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create .pydraconfrc
            rc_file = tmppath / ".pydraconfrc"
            rc_file.write_text(json.dumps({"config_dirs": ["my_configs"]}))

            result = load_config_dirs(tmppath)
            assert result == ["my_configs"]

    def test_load_from_pyproject_toml(self):
        """Test loading config_dirs from pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create pyproject.toml
            pyproject = tmppath / "pyproject.toml"
            pyproject.write_text('[tool.pydraconf]\nconfig_dirs = ["configs_folder"]')

            result = load_config_dirs(tmppath)
            assert result == ["configs_folder"]

    def test_load_list_from_pydraconfrc(self):
        """Test loading list of config_dirs from .pydraconfrc."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create .pydraconfrc with list
            rc_file = tmppath / ".pydraconfrc"
            rc_file.write_text(json.dumps({"config_dirs": ["dir1", "dir2", "dir3"]}))

            result = load_config_dirs(tmppath)
            assert result == ["dir1", "dir2", "dir3"]

    def test_pydraconfrc_takes_precedence(self):
        """Test that .pydraconfrc takes precedence over pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create both files
            rc_file = tmppath / ".pydraconfrc"
            rc_file.write_text(json.dumps({"config_dirs": ["rc_configs"]}))

            pyproject = tmppath / "pyproject.toml"
            pyproject.write_text('[tool.pydraconf]\nconfig_dirs = ["toml_configs"]')

            result = load_config_dirs(tmppath)
            assert result == ["rc_configs"]

    def test_searches_parent_directories(self):
        """Test that it searches parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create config in parent
            rc_file = tmppath / ".pydraconfrc"
            rc_file.write_text(json.dumps({"config_dirs": ["parent_configs"]}))

            # Search from subdirectory
            subdir = tmppath / "subdir" / "nested"
            subdir.mkdir(parents=True)

            result = load_config_dirs(subdir)
            assert result == ["parent_configs"]

    def test_returns_none_if_not_found(self):
        """Test that it returns None if no config found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            result = load_config_dirs(tmppath)
            assert result is None

    def test_invalid_json_ignored(self):
        """Test that invalid JSON in .pydraconfrc is ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create invalid JSON
            rc_file = tmppath / ".pydraconfrc"
            rc_file.write_text("{invalid json")

            # Should fall back to pyproject.toml
            pyproject = tmppath / "pyproject.toml"
            pyproject.write_text('[tool.pydraconf]\nconfig_dirs = ["fallback"]')

            result = load_config_dirs(tmppath)
            assert result == ["fallback"]

    def test_missing_config_dirs_key(self):
        """Test that missing config_dirs key is handled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create .pydraconfrc without config_dirs
            rc_file = tmppath / ".pydraconfrc"
            rc_file.write_text(json.dumps({"other_key": "value"}))

            result = load_config_dirs(tmppath)
            assert result is None

    def test_pyproject_without_tool_section(self):
        """Test pyproject.toml without [tool.pydraconf] section."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create pyproject.toml without tool.pydraconf
            pyproject = tmppath / "pyproject.toml"
            pyproject.write_text('[project]\nname = "test"')

            result = load_config_dirs(tmppath)
            assert result is None

    def test_pyproject_with_tool_but_no_pydraconf(self):
        """Test pyproject.toml with [tool] but no [tool.pydraconf]."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)

            # Create pyproject.toml with other tool section
            pyproject = tmppath / "pyproject.toml"
            pyproject.write_text('[tool.other]\nkey = "value"')

            result = load_config_dirs(tmppath)
            assert result is None


class TestSubstituteVariables:
    """Tests for substitute_variables function."""

    def test_substitute_cwd(self):
        """Test substituting $CWD variable."""
        cwd = Path("/tmp/test")
        result = substitute_variables("$CWD/configs", cwd, None)
        assert result == "/tmp/test/configs"

    def test_substitute_root(self):
        """Test substituting $ROOT variable."""
        root = Path("/project/root")
        result = substitute_variables("$ROOT/configs", Path("/cwd"), root)
        assert result == "/project/root/configs"

    def test_substitute_multiple_variables(self):
        """Test substituting multiple variables in one path."""
        result = substitute_variables(
            "$ROOT/base:$CWD/local",
            Path("/tmp"),
            Path("/root"),
        )
        assert result == "/root/base:/tmp/local"

    def test_relative_path_unchanged(self):
        """Test that relative paths are not modified."""
        result = substitute_variables("configs", Path("/cwd"), Path("/root"))
        assert result == "configs"


class TestFindRootDir:
    """Tests for find_root_dir function."""

    def test_finds_pyproject_toml(self):
        """Test finding root by pyproject.toml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir).resolve()

            # Create pyproject.toml in root
            (tmppath / "pyproject.toml").write_text("[project]\nname='test'")

            # Create subdirectory
            subdir = tmppath / "subdir"
            subdir.mkdir()

            result = find_root_dir(subdir)
            assert result == tmppath

    def test_finds_pydraconfrc(self):
        """Test finding root by .pydraconfrc."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir).resolve()

            # Create .pydraconfrc in root
            (tmppath / ".pydraconfrc").write_text("{}")

            # Create subdirectory
            subdir = tmppath / "subdir"
            subdir.mkdir()

            result = find_root_dir(subdir)
            assert result == tmppath

    def test_returns_none_if_not_found(self):
        """Test returns None when no root markers found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = find_root_dir(Path(tmpdir))
            assert result is None
