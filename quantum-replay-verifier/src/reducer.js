'use strict';

const { hashObject } = require('./crypto');

const ACTIONS = new Set([
  'WRITE_MEMORY_COMMIT',
  'GRANT_PERMISSION'
]);

function clone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

function pad8(v) {
  return String(v).padStart(8, '0');
}

function stateRoot(state) {
  const clean = clone(state);
  delete clean.receipts;
  return hashObject(clean);
}

function receiptChainRoot(receipts) {
  return hashObject(receipts);
}

function executeBatch(priorState, batch, verifyTransaction) {
  if (batch.policy_hash !== priorState.policy_hash) {
    throw new Error('Policy gate rejected batch');
  }

  const state = clone(priorState);
  const receipts = [];

  let currentRoot = stateRoot(state);

  for (let i = 0; i < batch.transactions.length; i++) {
    const tx = batch.transactions[i];

    if (!ACTIONS.has(tx.action)) {
      throw new Error('Reducer gate rejected action');
    }

    const identity = state.identities[tx.actor];

    if (!identity) {
      throw new Error('Identity gate rejected actor');
    }

    if (!verifyTransaction(tx, identity.public_key_pem)) {
      throw new Error('Identity gate rejected signature');
    }

    const expectedNonce = pad8(
      Number(identity.nonce) + 1
    );

    if (tx.nonce !== expectedNonce) {
      throw new Error(
        `Replay gate rejected nonce: expected ${expectedNonce} got ${tx.nonce}`
      );
    }

    if (tx.action === 'WRITE_MEMORY_COMMIT') {
      state.memory[tx.payload.memory_key] = {
        value_hash: tx.payload.value_hash,
        visibility: tx.payload.visibility,
        writer: tx.actor
      };
    }

    if (tx.action === 'GRANT_PERMISSION') {
      state.permissions[tx.payload.subject] =
        state.permissions[tx.payload.subject] || [];

      if (
        !state.permissions[tx.payload.subject].includes(
          tx.payload.permission
        )
      ) {
        state.permissions[tx.payload.subject].push(
          tx.payload.permission
        );
      }
    }

    identity.nonce = tx.nonce;

    const nextRoot = stateRoot(state);

    const receipt = {
      receipt_id:
        `rcpt-${batch.chain_context.block_height}-${pad8(i + 1)}`,
      tx_id: tx.tx_id,
      actor: tx.actor,
      action: tx.action,
      status: 'accepted',
      prior_state_root: currentRoot,
      next_state_root: nextRoot,
      policy_hash: batch.policy_hash,
      deterministic_time:
        `${batch.chain_context.epoch}-${batch.chain_context.block_height}-${pad8(i + 1)}`
    };

    receipt.receipt_hash = hashObject(receipt);

    receipts.push(receipt);

    currentRoot = nextRoot;
  }

  state.receipts = receipts;

  return {
    initial_state_root: stateRoot(priorState),
    final_state_root: currentRoot,
    receipt_chain_root: receiptChainRoot(receipts),
    receipts
  };
}

module.exports = {
  executeBatch
};
