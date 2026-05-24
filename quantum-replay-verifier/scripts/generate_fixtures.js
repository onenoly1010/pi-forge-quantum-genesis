'use strict';

const fs = require('node:fs');
const crypto = require('node:crypto');

const {
  hashObject,
  signTransaction,
  verifyTransaction
} = require('../src/crypto');

const {
  executeBatch
} = require('../src/reducer');

const {
  publicKey,
  privateKey
} = crypto.generateKeyPairSync('ed25519');

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

tx.signature = signTransaction(
  tx,
  privateKeyPem
);

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

const mutated = JSON.parse(
  JSON.stringify(signedBatch)
);

mutated.transactions[0].payload.value_hash =
  '0x' + 'b'.repeat(64);

fs.writeFileSync(
  'data/genesis_state.json',
  JSON.stringify(genesis, null, 2)
);

fs.writeFileSync(
  'data/signed_inputs.json',
  JSON.stringify(signedBatch, null, 2)
);

fs.writeFileSync(
  'data/mutated_inputs.json',
  JSON.stringify(mutated, null, 2)
);

fs.writeFileSync(
  'data/expected_outputs.json',
  JSON.stringify({
    final_state_root:
      expected.final_state_root
  }, null, 2)
);
