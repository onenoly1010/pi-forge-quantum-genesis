"""
Test suite for GENESIS.md references.

This test verifies that GENESIS.md is properly referenced as the foundational
archive in key documentation files across the repository.
"""

import os
import pytest
from pathlib import Path


# Get the repository root directory
REPO_ROOT = Path(__file__).parent.parent


class TestGenesisReferences:
    """Test that GENESIS.md is properly referenced in documentation."""

    def test_genesis_file_exists(self):
        """Verify GENESIS.md file exists."""
        genesis_path = REPO_ROOT / "GENESIS.md"
        assert genesis_path.exists(), f"GENESIS.md not found at {genesis_path}"
        assert genesis_path.stat().st_size > 0, "GENESIS.md is empty"

    def test_genesis_sha256_exists(self):
        """Verify GENESIS.md.sha256 file exists for integrity verification."""
        sha256_path = REPO_ROOT / "GENESIS.md.sha256"
        assert sha256_path.exists(), f"GENESIS.md.sha256 not found at {sha256_path}"
        assert sha256_path.stat().st_size > 0, "GENESIS.md.sha256 is empty"

    def test_genesis_sha256_verification(self):
        """Verify GENESIS.md SHA256 hash is valid."""
        import subprocess
        result = subprocess.run(
            ["sha256sum", "-c", "GENESIS.md.sha256"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"SHA256 verification failed: {result.stderr}"
        assert "OK" in result.stdout, "SHA256 verification did not return OK"

    def test_readme_references_genesis(self):
        """Verify README.md references GENESIS.md."""
        readme_path = REPO_ROOT / "README.md"
        assert readme_path.exists(), "README.md not found"
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        assert "GENESIS.md" in content, "README.md does not reference GENESIS.md"
        assert "Eternal Archive" in content or "foundational" in content.lower(), \
            "README.md does not use foundational language for GENESIS.md"

    def test_ecosystem_overview_references_genesis(self):
        """Verify ECOSYSTEM_OVERVIEW.md references GENESIS.md."""
        overview_path = REPO_ROOT / "ECOSYSTEM_OVERVIEW.md"
        assert overview_path.exists(), "ECOSYSTEM_OVERVIEW.md not found"
        
        with open(overview_path, 'r') as f:
            content = f.read()
        
        assert "GENESIS.md" in content, "ECOSYSTEM_OVERVIEW.md does not reference GENESIS.md"
        # Should have multiple references since it's the ecosystem overview
        genesis_count = content.count("GENESIS.md")
        assert genesis_count >= 3, \
            f"ECOSYSTEM_OVERVIEW.md should have multiple GENESIS.md references, found {genesis_count}"

    def test_architecture_references_genesis(self):
        """Verify docs/ARCHITECTURE.md references GENESIS.md."""
        arch_path = REPO_ROOT / "docs" / "ARCHITECTURE.md"
        assert arch_path.exists(), "docs/ARCHITECTURE.md not found"
        
        with open(arch_path, 'r') as f:
            content = f.read()
        
        assert "GENESIS.md" in content, "docs/ARCHITECTURE.md does not reference GENESIS.md"
        assert "../GENESIS.md" in content, \
            "docs/ARCHITECTURE.md does not use correct relative path (../GENESIS.md)"

    def test_genesis_content_has_oinio_seal(self):
        """Verify GENESIS.md contains OINIO Seal content."""
        genesis_path = REPO_ROOT / "GENESIS.md"
        
        with open(genesis_path, 'r') as f:
            content = f.read()
        
        # Check for key OINIO Seal elements
        assert "OINIO" in content, "GENESIS.md does not contain OINIO reference"
        assert "Solstice" in content, "GENESIS.md does not reference Winter Solstice"
        assert "Sovereignty" in content, "GENESIS.md does not contain Sovereignty principle"
        assert "Transparency" in content, "GENESIS.md does not contain Transparency principle"

    def test_foundational_language_in_references(self):
        """Verify documentation uses foundational language when referencing GENESIS.md."""
        files_to_check = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "ECOSYSTEM_OVERVIEW.md",
            REPO_ROOT / "docs" / "ARCHITECTURE.md"
        ]
        
        foundational_terms = [
            "foundational",
            "foundation",
            "eternal archive",
            "archive",
            "rooted in",
            "built upon"
        ]
        
        for file_path in files_to_check:
            if not file_path.exists():
                continue
                
            with open(file_path, 'r') as f:
                content = f.read().lower()
            
            # Check if GENESIS.md is mentioned
            if "genesis.md" in content:
                # At least one foundational term should appear near GENESIS.md
                has_foundational_language = any(term in content for term in foundational_terms)
                assert has_foundational_language, \
                    f"{file_path.name} references GENESIS.md but lacks foundational language"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v"])
