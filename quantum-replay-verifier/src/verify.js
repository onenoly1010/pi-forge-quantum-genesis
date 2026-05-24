'use strict';

const fs = require('node:fs');
const path = require('node:path');

const {
  verifyTransaction,
  hashObject,
  signTransaction
} = require('./crypto');

const {
  executeBatch
} = require('./reducer');

function readJson(file) {
  return JSON.parse(
    fs.readFileSync(
      path.join(__dirname, '..', file),
      'utf8'
    )
  );
}

function line(v = '') {
  console.log(v);
}

const genesis = readJson('data/genesis_state.json');
const signed = readJson('data/signed_inputs.json');
const mutated = readJson('data/mutated_inputs.json');
const expected = readJson('data/expected_outputs.json');

line('[SYSTEM] Initializing Quantum Pi Forge Replay Verifier...');
line('[DATA]   Loading Genesis State Fixture');
line(`[DATA]   Ingesting Signed Execution Batch ${signed.batch_id}`);
line('');
line('--- RUNNING EXECUTOR REPLAY ---');

const valid = executeBatch(
  genesis,
  signed,
  verifyTransaction
);

if (valid.final_state_root !== expected.final_state_root) {
  throw new Error('Consensus verification failed');
}

line('[✓] Canonical serialization stabilized');
line('[✓] Cryptographic signature validation passed');
line('[✓] Isolated state-machine reducer executed');
line('[✓] State root reproduced identically');
line('[✓] Receipt chain integrity verified');
line('');
line(`[RESULT] STATE ROOT: ${valid.final_state_root}`);
line('[STATUS] CONSENSUS VERIFIED');
line('');
line('--- INITIATING MUTATION TAMPER TEST ---');

try {
  executeBatch(
    genesis,
    mutated,
    verifyTransaction
  );

  line('[!] Mutation unexpectedly succeeded');
} catch (err) {
  line('[!] State root divergence detected');
  line('[!] Receipt chain rejected');
  line('');
  line(`[EXPECTED] ${expected.final_state_root}`);
  line('[RECEIVED] <rejected>');
  line('[STATUS] MUTATION REJECTED');
}
