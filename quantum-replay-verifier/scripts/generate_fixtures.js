'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const {
  hashObject,
  signTransaction,
  verifyTransaction
} = require('../src/crypto');

const {
  executeBatch
} = require('../src/reducer');

const REPO_DIR = path.resolve(__dirname, '..');
const DATA_DIR = path.join(REPO_DIR, 'data');

/*
 * Deterministic Ed25519 private key.
 *
 * PKCS#8 DER prefix for Ed25519 private key:
 *   302e020100300506032b657004220420
 *
 * The final 32 bytes are the fixed seed. This makes fixture generation
 * byte-stable across runs while still exercising real Ed25519 signing.
 */
const ED25519_PKCS8_DER_PREFIX = '302e020100300506032b657004220420';
const FIXED_ED25519_SEED =
  '000102030405060708090a0b0c0d0e0f' +
  '101112131415161718191a1b1c1d1e1f';

const privateKey = crypto.createPrivateKey({
  key: Buffer.from(ED25519_PKCS8_DER_PREFIX + FIXED_ED25519_SEED, 'hex'),
  format: 'der',
  type: 'pkcs8'
});

const publicKey = crypto.createPublicKey(privateKey);

const publicKeyPem = publicKey.export({
  type: 'spki',
  format: 'pem'
});

const privateKeyPem = privateKey.export({
  type: 'pkcs8',
  format: 'pem'
});

const policy = {
  name: 'quantum-replay-verifier-policy',
  version: '1'
};

const policyHash = hashObject(policy);

const genesis = {
  policy_hash: policyHash,
  chain_context: {
    network: 'quantum-pi-forge-local',
    epoch: '000001',
    block_height: '00000048'
  },
  identities: {
    'did:oinio:kris': {
      public_key_pem: publicKeyPem,
      nonce: '00000000'
    }
  },
  memory: {},
  permissions: {},
  receipts: []
};

const tx = {
  tx_id: 'tx-000001',
  actor: 'did:oinio:kris',
  action: 'WRITE_MEMORY_COMMIT',
  nonce: '00000001',
  payload: {
    memory_key: 'forge.genesis.intent',
    value_hash: '0x' + 'a'.repeat(64),
    visibility: 'private'
  }
};

tx.signature = signTransaction(tx, privateKeyPem);

const signedBatch = {
  batch_id: 'batch-000049',
  policy_hash: policyHash,
  chain_context: {
    network: 'quantum-pi-forge-local',
    epoch: '000001',
    block_height: '00000049'
  },
  transactions: [tx]
};

const expected = executeBatch(
  genesis,
  signedBatch,
  verifyTransaction
);

const mutated = JSON.parse(JSON.stringify(signedBatch));

mutated.transactions[0].payload.value_hash =
  '0x' + 'b'.repeat(64);

fs.mkdirSync(DATA_DIR, { recursive: true });

fs.writeFileSync(
  path.join(DATA_DIR, 'genesis_state.json'),
  JSON.stringify(genesis, null, 2) + '\n'
);

fs.writeFileSync(
  path.join(DATA_DIR, 'signed_inputs.json'),
  JSON.stringify(signedBatch, null, 2) + '\n'
);

fs.writeFileSync(
  path.join(DATA_DIR, 'mutated_inputs.json'),
  JSON.stringify(mutated, null, 2) + '\n'
);

fs.writeFileSync(
  path.join(DATA_DIR, 'expected_outputs.json'),
  JSON.stringify({
    final_state_root: expected.final_state_root
  }, null, 2) + '\n'
);
