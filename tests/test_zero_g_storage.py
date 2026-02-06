"""
Tests for 0G Storage Integration for iNFT Memory
"""

import pytest
import asyncio
import os
import sqlite3
import tempfile
from pathlib import Path
import sys

# Add server directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "server"))

from integrations.zero_g_storage import (
    ZeroGStorageClient,
    StorageMetadata,
    generate_encryption_key,
    sync_to_0g_storage,
    load_from_0g_storage,
)


class TestZeroGStorageClient:
    """Test suite for ZeroGStorageClient"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def sample_db(self, temp_dir):
        """Create a sample SQLite database"""
        db_path = os.path.join(temp_dir, "test.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create sample table and data
        cursor.execute("""
            CREATE TABLE memory (
                id INTEGER PRIMARY KEY,
                timestamp INTEGER,
                content TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO memory (timestamp, content) VALUES (?, ?)",
            (1234567890, "test memory content")
        )
        conn.commit()
        conn.close()
        
        return db_path
    
    @pytest.fixture
    def encryption_key(self):
        """Generate test encryption key"""
        return generate_encryption_key("test_password_123")
    
    @pytest.fixture
    def storage_client(self, encryption_key):
        """Create ZeroGStorageClient instance for testing"""
        return ZeroGStorageClient(
            rpc_url="https://evmrpc.0g.ai",
            storage_contract_address="0x1234567890123456789012345678901234567890",
            private_key=None,  # No transactions in unit tests
            encryption_key=encryption_key
        )
    
    def test_calculate_file_checksum(self, storage_client, sample_db):
        """Test file checksum calculation"""
        checksum = storage_client.calculate_file_checksum(sample_db)
        
        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA-256 hex length
        
        # Checksum should be consistent
        checksum2 = storage_client.calculate_file_checksum(sample_db)
        assert checksum == checksum2
    
    def test_encrypt_decrypt_file(self, storage_client, sample_db, temp_dir):
        """Test file encryption and decryption"""
        encrypted_path = os.path.join(temp_dir, "encrypted.db")
        decrypted_path = os.path.join(temp_dir, "decrypted.db")
        
        # Encrypt
        enc_checksum = storage_client.encrypt_file(sample_db, encrypted_path)
        assert os.path.exists(encrypted_path)
        assert isinstance(enc_checksum, str)
        
        # Decrypt
        dec_checksum = storage_client.decrypt_file(encrypted_path, decrypted_path)
        assert os.path.exists(decrypted_path)
        
        # Verify decrypted content matches original
        original_checksum = storage_client.calculate_file_checksum(sample_db)
        decrypted_checksum = storage_client.calculate_file_checksum(decrypted_path)
        assert original_checksum == decrypted_checksum
    
    def test_encrypt_without_key_raises_error(self, temp_dir, sample_db):
        """Test that encryption without key raises ValueError"""
        client = ZeroGStorageClient(
            rpc_url="https://evmrpc.0g.ai",
            storage_contract_address="0x1234567890123456789012345678901234567890",
            encryption_key=None  # No encryption key
        )
        
        encrypted_path = os.path.join(temp_dir, "encrypted.db")
        
        with pytest.raises(ValueError, match="Encryption key not configured"):
            client.encrypt_file(sample_db, encrypted_path)
    
    @pytest.mark.asyncio
    async def test_upload_to_0g_storage(self, storage_client, sample_db):
        """Test upload to 0G Storage (placeholder implementation)"""
        storage_hash, file_size = await storage_client.upload_to_0g_storage(sample_db)
        
        assert isinstance(storage_hash, str)
        assert len(storage_hash) == 64  # SHA-256 hex
        assert file_size > 0
        assert file_size == os.path.getsize(sample_db)
    
    @pytest.mark.asyncio
    async def test_sync_to_0g_storage(self, storage_client, sample_db, temp_dir):
        """Test complete sync workflow"""
        inft_id = "test_inft_123"
        
        # Mock account for testing without actual transactions
        # In real tests, this would use a test network
        
        metadata = await storage_client.sync_to_0g_storage(
            inft_id=inft_id,
            db_path=sample_db,
            encrypt=True
        )
        
        assert isinstance(metadata, StorageMetadata)
        assert metadata.inft_id == inft_id
        assert len(metadata.file_hash) == 64
        assert len(metadata.checksum) == 64
        assert metadata.size_bytes > 0
        assert metadata.encryption_key_id == "default"
        assert metadata.version == 1
    
    @pytest.mark.asyncio
    async def test_sync_without_encryption(self, storage_client, sample_db):
        """Test sync without encryption"""
        inft_id = "test_inft_456"
        
        metadata = await storage_client.sync_to_0g_storage(
            inft_id=inft_id,
            db_path=sample_db,
            encrypt=False
        )
        
        assert metadata.encryption_key_id == "none"
    
    @pytest.mark.asyncio
    async def test_sync_nonexistent_file_raises_error(self, storage_client):
        """Test that syncing nonexistent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            await storage_client.sync_to_0g_storage(
                inft_id="test",
                db_path="/nonexistent/file.db"
            )
    
    @pytest.mark.asyncio
    async def test_append_event_log(self, storage_client, temp_dir):
        """Test event log append functionality"""
        inft_id = "test_inft_789"
        
        # Append events without reaching batch size
        for i in range(5):
            event = {"action": f"test_action_{i}", "data": {"value": i}}
            result = await storage_client.append_event_log(
                inft_id=inft_id,
                event=event,
                auto_batch=True,
                batch_size=10
            )
            
            # Should not upload yet
            if i < 9:
                assert result is None
        
        # Verify log file exists
        log_path = f"/tmp/inft_{inft_id}_events.jsonl"
        assert os.path.exists(log_path)
        
        # Clean up
        if os.path.exists(log_path):
            os.remove(log_path)
    
    @pytest.mark.asyncio
    async def test_append_event_log_auto_batch(self, storage_client):
        """Test event log auto-batching"""
        inft_id = "test_inft_batch"
        
        # Append enough events to trigger auto-batch
        batch_size = 5
        for i in range(batch_size):
            event = {"action": f"batch_test_{i}"}
            result = await storage_client.append_event_log(
                inft_id=inft_id,
                event=event,
                auto_batch=True,
                batch_size=batch_size
            )
            
            if i == batch_size - 1:
                # Last event should trigger upload
                assert result is not None
                assert isinstance(result, str)
                assert len(result) == 64  # SHA-256 hex
    
    def test_validate_chain_of_custody(self, storage_client):
        """Test chain-of-custody validation"""
        inft_id = "test_inft_custody"
        
        # Single hash is trivially valid
        assert storage_client.validate_chain_of_custody(inft_id, ["hash1"])
        
        # Multiple hashes (placeholder implementation always returns True)
        hashes = ["hash1", "hash2", "hash3"]
        assert storage_client.validate_chain_of_custody(inft_id, hashes)
    
    def test_rotate_encryption_key(self, storage_client):
        """Test encryption key rotation"""
        old_key = storage_client.encryption_key
        new_key = generate_encryption_key("new_password_456")
        
        storage_client.rotate_encryption_key(new_key)
        
        assert storage_client.encryption_key == new_key
        assert storage_client.encryption_key != old_key
        assert storage_client.cipher is not None
    
    def test_generate_encryption_key(self):
        """Test encryption key generation"""
        password = "test_password"
        
        # Generate key without salt
        key1 = generate_encryption_key(password)
        assert isinstance(key1, bytes)
        assert len(key1) == 44  # Base64 encoded 32 bytes
        
        # Generate key with salt
        salt = b"test_salt_123456"
        key2 = generate_encryption_key(password, salt)
        assert isinstance(key2, bytes)
        
        # Same password + salt = same key
        key3 = generate_encryption_key(password, salt)
        assert key2 == key3
        
        # Different salt = different key
        salt2 = b"different_salt12"
        key4 = generate_encryption_key(password, salt2)
        assert key2 != key4


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def sample_db(self, temp_dir):
        """Create a sample SQLite database"""
        db_path = os.path.join(temp_dir, "inft_test.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE events (
                id INTEGER PRIMARY KEY,
                event_type TEXT,
                data TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO events (event_type, data) VALUES (?, ?)",
            ("test", "test data")
        )
        conn.commit()
        conn.close()
        
        return db_path
    
    @pytest.mark.asyncio
    async def test_sync_to_0g_storage_convenience(self, sample_db, monkeypatch):
        """Test high-level sync convenience function"""
        # Set environment variables
        monkeypatch.setenv("ZERO_G_RPC", "https://evmrpc.0g.ai")
        monkeypatch.setenv("ZERO_G_STORAGE_CONTRACT", "0x1234567890123456789012345678901234567890")
        monkeypatch.setenv("INFT_ENCRYPTION_PASSWORD", "test_password")
        
        inft_id = "test_convenience"
        
        # Test sync
        metadata = await sync_to_0g_storage(
            inft_id=inft_id,
            db_path=sample_db
        )
        
        assert isinstance(metadata, StorageMetadata)
        assert metadata.inft_id == inft_id
    
    def test_convenience_missing_env_var(self, monkeypatch):
        """Test that missing environment variable raises error"""
        # Clear environment variables
        monkeypatch.delenv("ZERO_G_STORAGE_CONTRACT", raising=False)
        
        with pytest.raises(ValueError, match="ZERO_G_STORAGE_CONTRACT"):
            asyncio.run(sync_to_0g_storage("test", "/tmp/test.db"))


class TestDatabaseValidation:
    """Test database integrity validation"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def valid_db(self, temp_dir):
        """Create a valid SQLite database"""
        db_path = os.path.join(temp_dir, "valid.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT)")
        cursor.execute("INSERT INTO test (data) VALUES (?)", ("test data",))
        conn.commit()
        conn.close()
        return db_path
    
    @pytest.fixture
    def corrupted_db(self, temp_dir):
        """Create a corrupted database file"""
        db_path = os.path.join(temp_dir, "corrupted.db")
        with open(db_path, "wb") as f:
            f.write(b"This is not a valid SQLite database file")
        return db_path
    
    @pytest.mark.asyncio
    async def test_sync_validates_database(self, valid_db):
        """Test that sync validates database integrity"""
        client = ZeroGStorageClient(
            rpc_url="https://evmrpc.0g.ai",
            storage_contract_address="0x1234567890123456789012345678901234567890",
            encryption_key=generate_encryption_key("test")
        )
        
        # Should not raise error for valid database
        metadata = await client.sync_to_0g_storage(
            inft_id="test",
            db_path=valid_db,
            encrypt=False
        )
        assert metadata is not None
    
    @pytest.mark.asyncio
    async def test_sync_rejects_corrupted_database(self, corrupted_db):
        """Test that sync rejects corrupted database"""
        client = ZeroGStorageClient(
            rpc_url="https://evmrpc.0g.ai",
            storage_contract_address="0x1234567890123456789012345678901234567890",
            encryption_key=generate_encryption_key("test")
        )
        
        # Should raise error for corrupted database
        with pytest.raises(ValueError, match="integrity check failed"):
            await client.sync_to_0g_storage(
                inft_id="test",
                db_path=corrupted_db,
                encrypt=False
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
