'use strict';

function canonicalSerialize(value) {
  return serialize(value);
}

function serialize(value) {
  if (value === null) return 'null';

  const t = typeof value;

  if (t === 'string') {
    return JSON.stringify(value.normalize('NFC'));
  }

  if (t === 'number') {
    if (!Number.isSafeInteger(value)) {
      throw new Error('Only safe integers allowed');
    }

    return String(value);
  }

  if (t === 'boolean') {
    return value ? 'true' : 'false';
  }

  if (Array.isArray(value)) {
    return '[' + value.map(serialize).join(',') + ']';
  }

  if (t === 'object') {
    const keys = Object.keys(value).sort();

    return (
      '{' +
      keys
        .map(
          (k) =>
            JSON.stringify(k.normalize('NFC')) +
            ':' +
            serialize(value[k])
        )
        .join(',') +
      '}'
    );
  }

  throw new Error(`Unsupported type: ${t}`);
}

module.exports = {
  canonicalSerialize
};
