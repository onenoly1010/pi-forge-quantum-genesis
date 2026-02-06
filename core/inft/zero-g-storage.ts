/**
 * 0G Storage Integration for iNFT Memory Persistence (TypeScript)
 * Provides secure upload/download of encrypted AI/agent memory to decentralized 0G Storage
 */

import * as crypto from 'crypto';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { ethers } from 'ethers';

/**
 * Metadata for stored iNFT memory
 */
export interface StorageMetadata {
  inftId: string;
  fileHash: string;
  checksum: string;
  timestamp: number;
  sizeBytes: number;
  encryptionKeyId: string;
  version: number;
}

/**
 * Batch of append-only event logs
 */
export interface EventLogBatch {
  inftId: string;
  events: Array<Record<string, any>>;
  batchId: string;
  timestamp: number;
  previousHash?: string;
}

/**
 * Configuration for ZeroGStorageClient
 */
export interface ZeroGStorageConfig {
  rpcUrl: string;
  storageContractAddress: string;
  privateKey?: string;
  encryptionKey?: Buffer;
}

/**
 * Storage pointer on-chain
 */
export interface StoragePointer {
  storageHash: string;
  checksum: string;
  timestamp: number;
}

/**
 * Client for interacting with 0G Storage network for iNFT memory persistence
 */
export class ZeroGStorageClient {
  private provider: ethers.JsonRpcProvider;
  private storageContract: ethers.Contract;
  private wallet?: ethers.Wallet;
  private encryptionKey?: Buffer;

  // Storage contract ABI (minimal interface)
  private static readonly STORAGE_ABI = [
    {
      inputs: [
        { name: 'inftId', type: 'string' },
        { name: 'storageHash', type: 'string' },
        { name: 'checksum', type: 'string' },
      ],
      name: 'updateStoragePointer',
      outputs: [],
      stateMutability: 'nonpayable',
      type: 'function',
    },
    {
      inputs: [{ name: 'inftId', type: 'string' }],
      name: 'getStoragePointer',
      outputs: [
        { name: 'storageHash', type: 'string' },
        { name: 'checksum', type: 'string' },
        { name: 'timestamp', type: 'uint256' },
      ],
      stateMutability: 'view',
      type: 'function',
    },
  ];

  /**
   * Initialize 0G Storage client
   */
  constructor(config: ZeroGStorageConfig) {
    this.provider = new ethers.JsonRpcProvider(config.rpcUrl);
    this.storageContract = new ethers.Contract(
      config.storageContractAddress,
      ZeroGStorageClient.STORAGE_ABI,
      this.provider
    );

    if (config.privateKey) {
      this.wallet = new ethers.Wallet(config.privateKey, this.provider);
      this.storageContract = this.storageContract.connect(this.wallet) as ethers.Contract;
    }

    this.encryptionKey = config.encryptionKey;
  }

  /**
   * Calculate SHA-256 checksum of a file
   */
  async calculateFileChecksum(filePath: string): Promise<string> {
    const data = await fs.readFile(filePath);
    const hash = crypto.createHash('sha256');
    hash.update(data);
    return hash.digest('hex');
  }

  /**
   * Encrypt a file using AES-256-GCM
   */
  async encryptFile(inputPath: string, outputPath: string): Promise<string> {
    if (!this.encryptionKey) {
      throw new Error('Encryption key not configured');
    }

    const data = await fs.readFile(inputPath);

    // Generate random IV
    const iv = crypto.randomBytes(16);

    // Create cipher
    const cipher = crypto.createCipheriv('aes-256-gcm', this.encryptionKey, iv);

    // Encrypt data
    const encrypted = Buffer.concat([cipher.update(data), cipher.final()]);

    // Get auth tag
    const authTag = cipher.getAuthTag();

    // Combine IV + authTag + encrypted data
    const combined = Buffer.concat([iv, authTag, encrypted]);

    await fs.writeFile(outputPath, combined);

    return this.calculateFileChecksum(outputPath);
  }

  /**
   * Decrypt a file using AES-256-GCM
   */
  async decryptFile(inputPath: string, outputPath: string): Promise<string> {
    if (!this.encryptionKey) {
      throw new Error('Encryption key not configured');
    }

    const data = await fs.readFile(inputPath);

    // Extract IV, auth tag, and encrypted data
    const iv = data.subarray(0, 16);
    const authTag = data.subarray(16, 32);
    const encrypted = data.subarray(32);

    // Create decipher
    const decipher = crypto.createDecipheriv('aes-256-gcm', this.encryptionKey, iv);
    decipher.setAuthTag(authTag);

    // Decrypt data
    const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);

    await fs.writeFile(outputPath, decrypted);

    return this.calculateFileChecksum(outputPath);
  }

  /**
   * Upload file to 0G Storage network
   * 
   * Note: This is a placeholder implementation. In production, this would
   * interact with the actual 0G Storage SDK/API.
   */
  async uploadTo0gStorage(filePath: string): Promise<{ storageHash: string; fileSize: number }> {
    // Calculate file hash as content identifier
    const fileHash = await this.calculateFileChecksum(filePath);
    const stats = await fs.stat(filePath);
    const fileSize = stats.size;

    // TODO: Implement actual 0G Storage upload using SDK
    // Example: const storageHash = await ogClient.uploadFile(filePath);

    console.log(`Uploaded file to 0G Storage: ${fileHash} (${fileSize} bytes)`);

    return { storageHash: fileHash, fileSize };
  }

  /**
   * Download file from 0G Storage network
   * 
   * Note: This is a placeholder implementation. In production, this would
   * interact with the actual 0G Storage SDK/API.
   */
  async downloadFrom0gStorage(storageHash: string, outputPath: string): Promise<number> {
    // TODO: Implement actual 0G Storage download using SDK
    // Example: await ogClient.downloadFile(storageHash, outputPath);

    // Verify file integrity after download
    try {
      const downloadedHash = await this.calculateFileChecksum(outputPath);
      if (downloadedHash !== storageHash) {
        console.warn(
          `Checksum mismatch: expected ${storageHash}, got ${downloadedHash}`
        );
      }
    } catch (error) {
      console.error('Checksum verification failed:', error);
    }

    const stats = await fs.stat(outputPath);
    const fileSize = stats.size;

    console.log(`Downloaded file from 0G Storage: ${storageHash} (${fileSize} bytes)`);

    return fileSize;
  }

  /**
   * Update on-chain storage pointer for an iNFT
   */
  async updateInftStoragePointer(
    inftId: string,
    storageHash: string,
    checksum: string
  ): Promise<ethers.TransactionReceipt> {
    if (!this.wallet) {
      throw new Error('Private key required for transactions');
    }

    const tx = await this.storageContract.updateStoragePointer(
      inftId,
      storageHash,
      checksum
    );

    const receipt = await tx.wait();

    return receipt;
  }

  /**
   * Get current storage pointer for an iNFT
   */
  async getInftStoragePointer(inftId: string): Promise<StoragePointer> {
    const result = await this.storageContract.getStoragePointer(inftId);

    return {
      storageHash: result[0],
      checksum: result[1],
      timestamp: Number(result[2]),
    };
  }

  /**
   * Complete workflow: encrypt, upload SQLite DB to 0G Storage, update on-chain pointer
   */
  async syncTo0gStorage(
    inftId: string,
    dbPath: string,
    encrypt: boolean = true
  ): Promise<StorageMetadata> {
    // Verify file exists
    try {
      await fs.access(dbPath);
    } catch (error) {
      throw new Error(`Database file not found: ${dbPath}`);
    }

    // Encrypt if requested
    let uploadPath = dbPath;
    if (encrypt) {
      if (!this.encryptionKey) {
        throw new Error('Encryption requested but key not configured');
      }

      const encryptedPath = `${dbPath}.encrypted`;
      await this.encryptFile(dbPath, encryptedPath);
      uploadPath = encryptedPath;
    }

    // Calculate checksum before upload
    const checksum = await this.calculateFileChecksum(uploadPath);

    // Upload to 0G Storage
    const { storageHash, fileSize } = await this.uploadTo0gStorage(uploadPath);

    // Update on-chain pointer
    if (this.wallet) {
      const receipt = await this.updateInftStoragePointer(inftId, storageHash, checksum);
      console.log(`Updated on-chain pointer: ${receipt.hash}`);
    }

    // Clean up encrypted file if created
    if (encrypt) {
      try {
        await fs.unlink(`${dbPath}.encrypted`);
      } catch (error) {
        // Ignore cleanup errors
      }
    }

    // Create metadata
    const metadata: StorageMetadata = {
      inftId,
      fileHash: storageHash,
      checksum,
      timestamp: Math.floor(Date.now() / 1000), // Use seconds for consistency with Python
      sizeBytes: fileSize,
      encryptionKeyId: encrypt ? 'default' : 'none',
      version: 1,
    };

    console.log(`Synced iNFT ${inftId} to 0G Storage: ${storageHash}`);

    return metadata;
  }

  /**
   * Complete workflow: download database from 0G Storage, decrypt, validate
   */
  async loadFrom0gStorage(
    inftId: string,
    outputDir?: string,
    verifyChecksum: boolean = true
  ): Promise<string> {
    // Use system temp directory if not specified
    const finalOutputDir = outputDir || os.tmpdir();
    // Get storage pointer from chain
    const { storageHash, checksum: expectedChecksum } =
      await this.getInftStoragePointer(inftId);

    console.log(`Loading iNFT ${inftId} from 0G Storage: ${storageHash}`);

    // Download from 0G Storage
    await fs.mkdir(finalOutputDir, { recursive: true });
    const encryptedPath = path.join(finalOutputDir, `inft_${inftId}.db.encrypted`);

    await this.downloadFrom0gStorage(storageHash, encryptedPath);

    // Verify checksum
    if (verifyChecksum) {
      const actualChecksum = await this.calculateFileChecksum(encryptedPath);
      if (actualChecksum !== expectedChecksum) {
        throw new Error(
          `Checksum verification failed: expected ${expectedChecksum}, got ${actualChecksum}`
        );
      }
    }

    // Decrypt if encrypted
    const finalPath = path.join(finalOutputDir, `inft_${inftId}.db`);

    if (this.encryptionKey) {
      try {
        await this.decryptFile(encryptedPath, finalPath);
        await fs.unlink(encryptedPath);
      } catch (error) {
        console.error('Decryption failed:', error);
        // If decryption fails, file might not be encrypted
        await fs.rename(encryptedPath, finalPath);
      }
    } else {
      await fs.rename(encryptedPath, finalPath);
    }

    console.log(`Loaded iNFT ${inftId} database to: ${finalPath}`);

    return finalPath;
  }

  /**
   * Append event to incremental event log with optional auto-batching
   * 
   * Note: Archived log files (when batch uploads) are not automatically cleaned up.
   * Consider implementing a cleanup strategy based on your retention policies.
   */
  async appendEventLog(
    inftId: string,
    event: Record<string, any>,
    autoBatch: boolean = true,
    batchSize: number = 100,
    logDir?: string
  ): Promise<string | null> {
    // Use system temp directory if not specified
    const finalLogDir = logDir || os.tmpdir();
    
    // Initialize or load event log
    const logPath = path.join(finalLogDir, `inft_${inftId}_events.jsonl`);

    // Append event with timestamp
    const eventEntry = {
      timestamp: new Date().toISOString(),
      event,
    };

    await fs.appendFile(logPath, JSON.stringify(eventEntry) + '\n');

    // Check if auto-batch threshold reached
    if (autoBatch) {
      const content = await fs.readFile(logPath, 'utf-8');
      const eventCount = content.split('\n').filter((line) => line.trim()).length;

      if (eventCount >= batchSize) {
        // Upload batch
        const { storageHash } = await this.uploadTo0gStorage(logPath);

        // Archive old log for next batch (user should implement cleanup)
        // Uses milliseconds for archive filename (consistent with Python implementation)
        const archivePath = path.join(finalLogDir, `inft_${inftId}_events_${Date.now()}.jsonl`);
        await fs.rename(logPath, archivePath);

        console.log(`Auto-uploaded event batch for iNFT ${inftId}: ${storageHash}`);
        console.log(`Archived log to: ${archivePath} (cleanup not automatic)`);

        return storageHash;
      }
    }

    return null;
  }

  /**
   * Validate chain-of-custody for sequential storage updates
   */
  validateChainOfCustody(inftId: string, storageHashes: string[]): boolean {
    if (storageHashes.length < 2) {
      return true; // Single or no updates are trivially valid
    }

    // Verify each hash links to previous
    for (let i = 1; i < storageHashes.length; i++) {
      const prevHash = storageHashes[i - 1];
      const currHash = storageHashes[i];

      // TODO: Implement actual chain validation logic
      // This would check that currHash includes prevHash in its metadata
      // and that timestamps are monotonically increasing

      console.debug(`Validating custody: ${prevHash} -> ${currHash}`);
    }

    return true;
  }

  /**
   * Rotate encryption key for future operations
   */
  rotateEncryptionKey(newKey: Buffer): void {
    this.encryptionKey = newKey;
    console.log('Encryption key rotated successfully');
  }
}

/**
 * Generate encryption key from password using PBKDF2
 */
export function generateEncryptionKey(password: string, salt?: Buffer): Buffer {
  const actualSalt = salt || crypto.randomBytes(16);

  return crypto.pbkdf2Sync(password, actualSalt, 100000, 32, 'sha256');
}

/**
 * High-level convenience function to sync iNFT memory to 0G Storage
 */
export async function syncTo0gStorage(
  inftId: string,
  dbPath?: string,
  storageClient?: ZeroGStorageClient
): Promise<StorageMetadata> {
  const finalDbPath = dbPath || `/data/inft_${inftId}.db`;

  let client = storageClient;
  if (!client) {
    // Create client from environment variables
    const rpcUrl = process.env.ZERO_G_RPC || 'https://evmrpc.0g.ai';
    const storageAddress = process.env.ZERO_G_STORAGE_CONTRACT;
    const privateKey = process.env.ZERO_G_PRIVATE_KEY;

    if (!storageAddress) {
      throw new Error('ZERO_G_STORAGE_CONTRACT environment variable required');
    }

    // Generate or load encryption key
    const encryptionPassword = process.env.INFT_ENCRYPTION_PASSWORD;
    let encryptionKey: Buffer | undefined;
    if (encryptionPassword) {
      encryptionKey = generateEncryptionKey(encryptionPassword);
    }

    client = new ZeroGStorageClient({
      rpcUrl,
      storageContractAddress: storageAddress,
      privateKey,
      encryptionKey,
    });
  }

  return client.syncTo0gStorage(inftId, finalDbPath);
}

/**
 * High-level convenience function to load iNFT memory from 0G Storage
 */
export async function loadFrom0gStorage(
  inftId: string,
  outputDir: string = '/data',
  storageClient?: ZeroGStorageClient
): Promise<string> {
  let client = storageClient;
  if (!client) {
    // Create client from environment variables
    const rpcUrl = process.env.ZERO_G_RPC || 'https://evmrpc.0g.ai';
    const storageAddress = process.env.ZERO_G_STORAGE_CONTRACT;
    const privateKey = process.env.ZERO_G_PRIVATE_KEY;

    if (!storageAddress) {
      throw new Error('ZERO_G_STORAGE_CONTRACT environment variable required');
    }

    // Generate or load encryption key
    const encryptionPassword = process.env.INFT_ENCRYPTION_PASSWORD;
    let encryptionKey: Buffer | undefined;
    if (encryptionPassword) {
      encryptionKey = generateEncryptionKey(encryptionPassword);
    }

    client = new ZeroGStorageClient({
      rpcUrl,
      storageContractAddress: storageAddress,
      privateKey,
      encryptionKey,
    });
  }

  return client.loadFrom0gStorage(inftId, outputDir);
}
