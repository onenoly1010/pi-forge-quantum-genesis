'use strict';

const crypto = require('node:crypto');
const { canonicalSerialize } = require('./serialization');

function sha256Hex(input) {
  return (
    '0x' +
    crypto
      .createHash('sha256')
      .update(input)
      .digest('hex')
  );
}

function hashObject(obj) {
  return sha256Hex(
    Buffer.from(canonicalSerialize(obj), 'utf8')
  );
}

function unsignedTransaction(tx) {
  const clone = { ...tx };
  delete clone.signature;
  return clone;
}

function signTransaction(tx, privateKeyPem) {
  const payload = Buffer.from(
    canonicalSerialize(unsignedTransaction(tx)),
    'utf8'
  );

  return (
    '0x' +
    crypto.sign(null, payload, privateKeyPem).toString('hex')
  );
}

function verifyTransaction(tx, publicKeyPem) {
  const payload = Buffer.from(
    canonicalSerialize(unsignedTransaction(tx)),
    'utf8'
  );

  const signature = Buffer.from(
    tx.signature.slice(2),
    'hex'
  );

  return crypto.verify(
    null,
    payload,
    publicKeyPem,
    signature
  );
}

module.exports = {
  sha256Hex,
  hashObject,
  signTransaction,
  verifyTransaction
};
