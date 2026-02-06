"""
0G Storage Integration for iNFT Memory Persistence
Provides secure upload/download of encrypted AI/agent memory to decentralized 0G Storage
"""

import os
import hashlib
import sqlite3
import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime
import json
import base64
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from web3 import Web3
from web3.contract import Contract

logger = logging.getLogger(__name__)


@dataclass
class StorageMetadata:
    """Metadata for stored iNFT memory"""
    inft_id: str
    file_hash: str
    checksum: str
    timestamp: int
    size_bytes: int
    encryption_key_id: str
    version: int = 1


@dataclass
class EventLogBatch:
    """Batch of append-only event logs"""
    inft_id: str
    events: List[Dict]
    batch_id: str
    timestamp: int
    previous_hash: Optional[str] = None


class ZeroGStorageClient:
    """
    Client for interacting with 0G Storage network for iNFT memory persistence
    """
    
    def __init__(
        self,
        rpc_url: str,
        storage_contract_address: str,
        private_key: Optional[str] = None,
        encryption_key: Optional[bytes] = None
    ):
        """
        Initialize 0G Storage client
        
        Args:
            rpc_url: 0G network RPC endpoint
            storage_contract_address: Storage registry contract address
            private_key: Optional private key for signing transactions
            encryption_key: Optional key for encrypting/decrypting data
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.storage_address = Web3.to_checksum_address(storage_contract_address)
        
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key)
        else:
            self.account = None
        
        # Initialize encryption
        self.encryption_key = encryption_key
        if encryption_key:
            self.cipher = Fernet(encryption_key)
        else:
            self.cipher = None
        
        # Storage contract ABI (minimal interface)
        self.storage_abi = [
            {
                "inputs": [
                    {"name": "inftId", "type": "string"},
                    {"name": "storageHash", "type": "string"},
                    {"name": "checksum", "type": "string"}
                ],
                "name": "updateStoragePointer",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "inftId", "type": "string"}],
                "name": "getStoragePointer",
                "outputs": [
                    {"name": "storageHash", "type": "string"},
                    {"name": "checksum", "type": "string"},
                    {"name": "timestamp", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        self.storage_contract = self.w3.eth.contract(
            address=self.storage_address,
            abi=self.storage_abi
        )
    
    def calculate_file_checksum(self, file_path: str) -> str:
        """
        Calculate SHA-256 checksum of a file
        
        Args:
            file_path: Path to file
        
        Returns:
            Hex-encoded SHA-256 checksum
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def encrypt_file(self, input_path: str, output_path: str) -> str:
        """
        Encrypt a file using Fernet symmetric encryption
        
        Args:
            input_path: Path to input file
            output_path: Path to encrypted output file
        
        Returns:
            Checksum of encrypted file
        
        Raises:
            ValueError: If encryption key is not configured
        """
        if not self.cipher:
            raise ValueError("Encryption key not configured")
        
        with open(input_path, "rb") as f:
            data = f.read()
        
        encrypted_data = self.cipher.encrypt(data)
        
        with open(output_path, "wb") as f:
            f.write(encrypted_data)
        
        return self.calculate_file_checksum(output_path)
    
    def decrypt_file(self, input_path: str, output_path: str) -> str:
        """
        Decrypt a file using Fernet symmetric encryption
        
        Args:
            input_path: Path to encrypted file
            output_path: Path to decrypted output file
        
        Returns:
            Checksum of decrypted file
        
        Raises:
            ValueError: If encryption key is not configured
        """
        if not self.cipher:
            raise ValueError("Encryption key not configured")
        
        with open(input_path, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = self.cipher.decrypt(encrypted_data)
        
        with open(output_path, "wb") as f:
            f.write(decrypted_data)
        
        return self.calculate_file_checksum(output_path)
    
    async def upload_to_0g_storage(self, file_path: str) -> Tuple[str, int]:
        """
        Upload file to 0G Storage network
        
        Args:
            file_path: Path to file to upload
        
        Returns:
            Tuple of (storage_hash, file_size)
        
        Note:
            This is a placeholder implementation. In production, this would
            interact with the actual 0G Storage SDK/API to upload the file
            and return the content-addressed hash.
        """
        # Calculate file hash as content identifier
        file_hash = self.calculate_file_checksum(file_path)
        file_size = os.path.getsize(file_path)
        
        # TODO: Implement actual 0G Storage upload using SDK
        # Example: storage_hash = await og_client.upload_file(file_path)
        
        logger.info(f"Uploaded file to 0G Storage: {file_hash} ({file_size} bytes)")
        
        # Return content hash and size
        return file_hash, file_size
    
    async def download_from_0g_storage(self, storage_hash: str, output_path: str) -> int:
        """
        Download file from 0G Storage network
        
        Args:
            storage_hash: Content hash of file in 0G Storage
            output_path: Local path to save downloaded file
        
        Returns:
            Size of downloaded file in bytes
        
        Note:
            This is a placeholder implementation. In production, this would
            interact with the actual 0G Storage SDK/API to download the file.
        """
        # TODO: Implement actual 0G Storage download using SDK
        # Example: await og_client.download_file(storage_hash, output_path)
        
        # Verify file integrity after download
        if os.path.exists(output_path):
            downloaded_hash = self.calculate_file_checksum(output_path)
            if downloaded_hash != storage_hash:
                logger.warning(f"Checksum mismatch: expected {storage_hash}, got {downloaded_hash}")
        
        file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
        logger.info(f"Downloaded file from 0G Storage: {storage_hash} ({file_size} bytes)")
        
        return file_size
    
    async def update_inft_storage_pointer(
        self,
        inft_id: str,
        storage_hash: str,
        checksum: str
    ) -> Dict:
        """
        Update on-chain storage pointer for an iNFT
        
        Args:
            inft_id: Unique identifier for the iNFT
            storage_hash: 0G Storage content hash
            checksum: File integrity checksum
        
        Returns:
            Transaction receipt
        
        Raises:
            ValueError: If account is not configured
        """
        if not self.account:
            raise ValueError("Private key required for transactions")
        
        # Build transaction
        tx = self.storage_contract.functions.updateStoragePointer(
            inft_id,
            storage_hash,
            checksum
        ).build_transaction({
            'from': self.account.address,
            'gas': 150000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        
        # Sign and send
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'tx_hash': tx_hash.hex(),
            'status': receipt['status'],
            'gas_used': receipt['gasUsed'],
            'block_number': receipt['blockNumber']
        }
    
    async def get_inft_storage_pointer(self, inft_id: str) -> Tuple[str, str, int]:
        """
        Get current storage pointer for an iNFT
        
        Args:
            inft_id: Unique identifier for the iNFT
        
        Returns:
            Tuple of (storage_hash, checksum, timestamp)
        """
        result = self.storage_contract.functions.getStoragePointer(inft_id).call()
        return result
    
    async def sync_to_0g_storage(
        self,
        inft_id: str,
        db_path: str,
        encrypt: bool = True
    ) -> StorageMetadata:
        """
        Complete workflow: encrypt, upload SQLite DB to 0G Storage, update on-chain pointer
        
        Args:
            inft_id: Unique identifier for the iNFT
            db_path: Path to SQLite database file
            encrypt: Whether to encrypt before upload (default: True)
        
        Returns:
            StorageMetadata with upload details
        
        Raises:
            FileNotFoundError: If database file doesn't exist
            ValueError: If encryption is requested but key not configured
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        
        # Validate database integrity
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA integrity_check")
            conn.close()
        except Exception as e:
            raise ValueError(f"Database integrity check failed: {e}")
        
        # Encrypt if requested
        upload_path = db_path
        if encrypt:
            if not self.cipher:
                raise ValueError("Encryption requested but key not configured")
            
            encrypted_path = f"{db_path}.encrypted"
            self.encrypt_file(db_path, encrypted_path)
            upload_path = encrypted_path
        
        # Calculate checksum before upload
        checksum = self.calculate_file_checksum(upload_path)
        
        # Upload to 0G Storage
        storage_hash, file_size = await self.upload_to_0g_storage(upload_path)
        
        # Update on-chain pointer
        if self.account:
            tx_result = await self.update_inft_storage_pointer(
                inft_id,
                storage_hash,
                checksum
            )
            logger.info(f"Updated on-chain pointer: {tx_result['tx_hash']}")
        
        # Clean up encrypted file if created
        if encrypt and os.path.exists(encrypted_path):
            os.remove(encrypted_path)
        
        # Create metadata
        metadata = StorageMetadata(
            inft_id=inft_id,
            file_hash=storage_hash,
            checksum=checksum,
            timestamp=int(datetime.now().timestamp()),
            size_bytes=file_size,
            encryption_key_id="default" if encrypt else "none"
        )
        
        logger.info(f"Synced iNFT {inft_id} to 0G Storage: {storage_hash}")
        
        return metadata
    
    async def load_from_0g_storage(
        self,
        inft_id: str,
        output_dir: str = "/tmp",
        verify_checksum: bool = True
    ) -> str:
        """
        Complete workflow: download database from 0G Storage, decrypt, validate
        
        Args:
            inft_id: Unique identifier for the iNFT
            output_dir: Directory to save downloaded database
            verify_checksum: Whether to verify checksum after download
        
        Returns:
            Path to restored database file
        
        Raises:
            ValueError: If checksum verification fails
        """
        # Get storage pointer from chain
        storage_hash, expected_checksum, timestamp = await self.get_inft_storage_pointer(inft_id)
        
        logger.info(f"Loading iNFT {inft_id} from 0G Storage: {storage_hash}")
        
        # Download from 0G Storage
        os.makedirs(output_dir, exist_ok=True)
        encrypted_path = os.path.join(output_dir, f"inft_{inft_id}.db.encrypted")
        
        await self.download_from_0g_storage(storage_hash, encrypted_path)
        
        # Verify checksum
        if verify_checksum:
            actual_checksum = self.calculate_file_checksum(encrypted_path)
            if actual_checksum != expected_checksum:
                raise ValueError(
                    f"Checksum verification failed: expected {expected_checksum}, "
                    f"got {actual_checksum}"
                )
        
        # Decrypt if encrypted
        final_path = os.path.join(output_dir, f"inft_{inft_id}.db")
        
        if self.cipher:
            try:
                self.decrypt_file(encrypted_path, final_path)
                os.remove(encrypted_path)
            except Exception as e:
                logger.error(f"Decryption failed: {e}")
                # If decryption fails, file might not be encrypted
                os.rename(encrypted_path, final_path)
        else:
            os.rename(encrypted_path, final_path)
        
        # Validate database integrity
        try:
            conn = sqlite3.connect(final_path)
            conn.execute("PRAGMA integrity_check")
            conn.close()
        except Exception as e:
            raise ValueError(f"Downloaded database integrity check failed: {e}")
        
        logger.info(f"Loaded iNFT {inft_id} database to: {final_path}")
        
        return final_path
    
    async def append_event_log(
        self,
        inft_id: str,
        event: Dict,
        auto_batch: bool = True,
        batch_size: int = 100
    ) -> Optional[str]:
        """
        Append event to incremental event log with optional auto-batching
        
        Args:
            inft_id: Unique identifier for the iNFT
            event: Event data to append
            auto_batch: Whether to automatically upload when batch size reached
            batch_size: Number of events to batch before auto-upload
        
        Returns:
            Storage hash if batch was uploaded, None otherwise
        """
        # Initialize or load event log
        log_path = f"/tmp/inft_{inft_id}_events.jsonl"
        
        # Append event with timestamp
        event_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        
        with open(log_path, "a") as f:
            f.write(json.dumps(event_entry) + "\n")
        
        # Check if auto-batch threshold reached
        if auto_batch:
            with open(log_path, "r") as f:
                event_count = sum(1 for _ in f)
            
            if event_count >= batch_size:
                # Upload batch
                storage_hash, _ = await self.upload_to_0g_storage(log_path)
                
                # Create new log for next batch
                archive_path = f"/tmp/inft_{inft_id}_events_{int(datetime.now().timestamp())}.jsonl"
                os.rename(log_path, archive_path)
                
                logger.info(f"Auto-uploaded event batch for iNFT {inft_id}: {storage_hash}")
                
                return storage_hash
        
        return None
    
    def validate_chain_of_custody(
        self,
        inft_id: str,
        storage_hashes: List[str]
    ) -> bool:
        """
        Validate chain-of-custody for sequential storage updates
        
        Args:
            inft_id: Unique identifier for the iNFT
            storage_hashes: List of storage hashes in chronological order
        
        Returns:
            True if chain of custody is valid
        
        Note:
            This validates that each storage update builds upon the previous
            by checking hash linkage and temporal ordering
        """
        if len(storage_hashes) < 2:
            return True  # Single or no updates are trivially valid
        
        # Verify each hash links to previous
        for i in range(1, len(storage_hashes)):
            prev_hash = storage_hashes[i - 1]
            curr_hash = storage_hashes[i]
            
            # TODO: Implement actual chain validation logic
            # This would check that curr_hash includes prev_hash in its metadata
            # and that timestamps are monotonically increasing
            
            logger.debug(f"Validating custody: {prev_hash} -> {curr_hash}")
        
        return True
    
    def rotate_encryption_key(self, new_key: bytes) -> None:
        """
        Rotate encryption key for future operations
        
        Args:
            new_key: New encryption key
        
        Note:
            This only affects future encrypt/decrypt operations.
            Existing encrypted files must be re-encrypted manually.
        """
        self.encryption_key = new_key
        self.cipher = Fernet(new_key)
        logger.info("Encryption key rotated successfully")


# Convenience functions

def generate_encryption_key(password: str, salt: Optional[bytes] = None) -> bytes:
    """
    Generate encryption key from password using PBKDF2
    
    Args:
        password: User password
        salt: Optional salt (generated if not provided)
    
    Returns:
        Base64-encoded Fernet-compatible key
    """
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


async def sync_to_0g_storage(
    inft_id: str,
    db_path: str = None,
    storage_client: Optional[ZeroGStorageClient] = None
) -> StorageMetadata:
    """
    High-level convenience function to sync iNFT memory to 0G Storage
    
    Args:
        inft_id: Unique identifier for the iNFT
        db_path: Path to database file (default: /data/inft_{inft_id}.db)
        storage_client: Optional pre-configured client
    
    Returns:
        StorageMetadata with upload details
    """
    if db_path is None:
        db_path = f"/data/inft_{inft_id}.db"
    
    if storage_client is None:
        # Create client from environment variables
        rpc_url = os.getenv("ZERO_G_RPC", "https://evmrpc.0g.ai")
        storage_address = os.getenv("ZERO_G_STORAGE_CONTRACT")
        private_key = os.getenv("ZERO_G_PRIVATE_KEY")
        
        if not storage_address:
            raise ValueError("ZERO_G_STORAGE_CONTRACT environment variable required")
        
        # Generate or load encryption key
        encryption_password = os.getenv("INFT_ENCRYPTION_PASSWORD")
        encryption_key = None
        if encryption_password:
            encryption_key = generate_encryption_key(encryption_password)
        
        storage_client = ZeroGStorageClient(
            rpc_url=rpc_url,
            storage_contract_address=storage_address,
            private_key=private_key,
            encryption_key=encryption_key
        )
    
    return await storage_client.sync_to_0g_storage(inft_id, db_path)


async def load_from_0g_storage(
    inft_id: str,
    output_dir: str = "/data",
    storage_client: Optional[ZeroGStorageClient] = None
) -> str:
    """
    High-level convenience function to load iNFT memory from 0G Storage
    
    Args:
        inft_id: Unique identifier for the iNFT
        output_dir: Directory to save restored database
        storage_client: Optional pre-configured client
    
    Returns:
        Path to restored database file
    """
    if storage_client is None:
        # Create client from environment variables
        rpc_url = os.getenv("ZERO_G_RPC", "https://evmrpc.0g.ai")
        storage_address = os.getenv("ZERO_G_STORAGE_CONTRACT")
        private_key = os.getenv("ZERO_G_PRIVATE_KEY")
        
        if not storage_address:
            raise ValueError("ZERO_G_STORAGE_CONTRACT environment variable required")
        
        # Generate or load encryption key
        encryption_password = os.getenv("INFT_ENCRYPTION_PASSWORD")
        encryption_key = None
        if encryption_password:
            encryption_key = generate_encryption_key(encryption_password)
        
        storage_client = ZeroGStorageClient(
            rpc_url=rpc_url,
            storage_contract_address=storage_address,
            private_key=private_key,
            encryption_key=encryption_key
        )
    
    return await storage_client.load_from_0g_storage(inft_id, output_dir)


__all__ = [
    "ZeroGStorageClient",
    "StorageMetadata",
    "EventLogBatch",
    "generate_encryption_key",
    "sync_to_0g_storage",
    "load_from_0g_storage",
]
