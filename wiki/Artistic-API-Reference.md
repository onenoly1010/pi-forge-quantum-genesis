# 🎨 Artistic API Reference

## The Lyrical Lens: Quantum Fractal Visualization

The **Flask Lyrical Lens** (Port 5000) transforms blockchain data into art. This service embodies the artistic core of the Quantum Pi Forge by rendering transaction hashes as unique, procedurally-generated SVG fractals.

**Philosophy:** *"Beauty is fundamental, not decorative. Data becomes art. The invisible ledger manifests visually."*

---

## 🌌 Fractal Generation Endpoint

### `GET /api/svg/cascade/<tx_hash>`

Generate a unique SVG fractal from a blockchain transaction hash.

**Parameters:**
- `tx_hash` (path) — Transaction hash (any string, typically hex)
- `type` (query, optional) — Fractal type: `recursive`, `mandala`, `sierpinski`, or `auto`

**Returns:**
- `Content-Type: image/svg+xml`
- SVG fractal uniquely derived from transaction hash

**Examples:**

```bash
# Auto-select fractal type based on hash
curl http://localhost:5000/api/svg/cascade/0xabc123

# Specific fractal types
curl http://localhost:5000/api/svg/cascade/0xabc123?type=mandala
curl http://localhost:5000/api/svg/cascade/0xabc123?type=recursive
curl http://localhost:5000/api/svg/cascade/0xabc123?type=sierpinski
```

**Browser Usage:**
```html
<img src="http://localhost:5000/api/svg/cascade/0xabc123?type=mandala" 
     alt="Transaction Fractal" />
```

---

## 🎨 Fractal Types

### 1. **Recursive Circles** (`?type=recursive`)

Generates nested, recursive circular patterns with varying:
- Number of child circles per generation
- Circle sizes and positions
- Colors (HSL derived from hash)
- Opacity levels
- Recursion depth

**Visual Character:** Organic, flowing, cellular

**Best For:** Transaction flows, network visualizations, user interactions

---

### 2. **Mandala** (`?type=mandala`)

Creates radial, symmetrical mandala patterns with:
- Petal count derived from hash
- Varying petal sizes and positions
- Rotational symmetry
- Central focal point
- Rich color palettes

**Visual Character:** Meditative, balanced, harmonious

**Best For:** User profiles, achievement badges, ceremonial events

---

### 3. **Sierpinski Variation** (`?type=sierpinski`)

Generates fractal triangular patterns inspired by the Sierpinski triangle:
- Recursive triangle subdivision
- Varying recursion depth
- Hash-derived color schemes
- Self-similar at multiple scales

**Visual Character:** Mathematical, precise, structured

**Best For:** Smart contracts, governance votes, technical events

---

### 4. **Auto-Select** (`?type=auto`, default)

Automatically selects fractal type based on hash properties. Each transaction hash produces a consistent fractal type.

**Use this when:** You want variety but consistency per hash.

---

## 🔮 How It Works

### Hash-Based Procedural Generation

Each transaction hash is transformed into a unique fractal through deterministic procedural generation:

1. **Hash Processing**
   - Transaction hash → SHA-256 digest
   - 32 bytes of entropy extracted
   
2. **Parameter Derivation**
   - Colors: HSL values from hash bytes
   - Positions: Angles and distances from hash
   - Sizes: Radii and scales from hash
   - Counts: Number of elements from hash
   
3. **Deterministic Output**
   - Same hash → Same fractal (always)
   - Different hashes → Different fractals
   - No randomness or server state

### Example Hash Mapping

```python
# Hash bytes → Visual parameters
hash_bytes[0] → Hue (0-360°)
hash_bytes[1] → Saturation (50-100%)
hash_bytes[2] → Lightness (40-80%)
hash_bytes[3] → Opacity (0.3-0.8)
hash_bytes[4] → Element count (3-8)
hash_bytes[5] → Size variation (0.3-0.6)
```

**Result:** Each transaction has a unique "visual fingerprint" that can be recognized and remembered.

---

## 🎯 Use Cases

### 1. **Transaction Visualization**

Display unique fractals for each blockchain transaction:

```javascript
// React example
function TransactionCard({ txHash }) {
  return (
    <div className="transaction">
      <img 
        src={`/api/svg/cascade/${txHash}?type=auto`}
        alt="Transaction Visualization"
        className="tx-fractal"
      />
      <p>{txHash}</p>
    </div>
  );
}
```

---

### 2. **User Avatar Generation**

Generate unique user avatars from wallet addresses:

```javascript
function UserAvatar({ walletAddress }) {
  return (
    <img 
      src={`/api/svg/cascade/${walletAddress}?type=mandala`}
      alt="User Avatar"
      className="avatar"
    />
  );
}
```

---

### 3. **NFT Preview**

Create artistic previews for NFT metadata:

```javascript
function NFTCard({ tokenId, metadata }) {
  const hash = metadata.transactionHash || tokenId;
  return (
    <div className="nft-card">
      <img src={`/api/svg/cascade/${hash}?type=recursive`} />
      <h3>{metadata.name}</h3>
    </div>
  );
}
```

---

### 4. **Event Commemoration**

Generate unique fractals for milestone events:

```javascript
// Genesis moment fractal
const genesisFractal = `/api/svg/cascade/${GENESIS_BLOCK_HASH}?type=mandala`;

// Deployment fractals
const deploymentFractal = `/api/svg/cascade/${DEPLOYMENT_TX}?type=sierpinski`;
```

---

## 🌿 Contributing to the Artistic Core

The fractal generator is designed for community extension. You can:

### Add New Fractal Types

1. Edit `server/quantum_fractal_generator.py`
2. Add a new method to `QuantumFractalGenerator` class
3. Update `generate_svg()` to support the new type
4. Test with various hashes
5. Submit a PR

**Example:**

```python
def generate_spiral_pattern(self) -> List[str]:
    """Generate spiral fractal pattern"""
    elements = []
    # Your creative implementation here
    return elements
```

### Improve Existing Fractals

- Enhance color palettes
- Add animation support
- Optimize SVG output size
- Add accessibility features

### Create Fractal Themes

- Dark mode / Light mode variants
- Seasonal themes
- Cultural pattern variations
- Accessibility-focused designs

**See [Human Contribution Guide](../wiki/Human-Contribution-Guide.md) for how to contribute.**

---

## 🔧 Technical Details

### Generator Class: `QuantumFractalGenerator`

```python
from quantum_fractal_generator import QuantumFractalGenerator

# Create generator for transaction hash
gen = QuantumFractalGenerator("0xabc123def456...")

# Generate specific fractal type
svg = gen.generate_svg(fractal_type="mandala")

# Convenience function
from quantum_fractal_generator import generate_resonance_fractal
svg = generate_resonance_fractal("0xabc123...", "recursive")
```

### Customization Options

```python
# Custom dimensions
svg = gen.generate_svg(width=600, height=600, fractal_type="mandala")

# Get fractal elements without full SVG wrapper
elements = gen.generate_mandala_pattern()
```

### Hash Value Extraction

```python
# Extract normalized float (0-1) from hash
value = gen._get_hash_float(index)

# Extract integer (0-max_val) from hash
value = gen._get_hash_value(index, max_val=360)

# Extract HSL color from hash
color = gen._get_color_from_hash(index)
```

---

## 🎨 Sacred Trinity Integration

The Fractal Generator is part of the **Lyrical Lens** (Flask - Port 5000):

- **FastAPI (8000)** generates transaction data
- **Flask (5000)** renders data as fractals
- **Gradio (7860)** provides ethical oversight

**Data Flow:**
```
User Transaction (FastAPI)
    ↓
Transaction Hash
    ↓
Fractal Generation (Flask)
    ↓
Visual Feedback to User
```

---

## 📚 Related Documentation

- [Sacred Trinity Architecture](../wiki/Sacred-Trinity.md)
- [Genesis Declaration](../wiki/Genesis-Declaration.md) — Artistic philosophy
- [Canon of Autonomy](../wiki/Canon-of-Autonomy.md) — Guiding principles
- [Human Contribution Guide](../wiki/Human-Contribution-Guide.md) — How to contribute

---

## 🌟 Philosophy: Why Art Matters

From the [Genesis Declaration](../wiki/Genesis-Declaration.md):

> *"The Lyrical Lens (Flask): Quantum canvases rendering blockchain ballads. Procedural SVG sonnets born from hash entropy. The visual manifestation of the invisible ledger."*

Art is not decoration in the Quantum Pi Forge—it's fundamental identity:

✨ **Technology serves consciousness** — not just computation
✨ **Beauty is fundamental** — not decorative
✨ **Visualizations are conversation** — not just display
✨ **The lattice is alive** — not just data

**Every transaction hash tells a story. Every fractal is a poem. Every visualization is consciousness made visible.**

---

*The Lyrical Lens transforms the invisible into the unforgettable.*

**🎨 Artistic Core Active. Fractals Alive. Beauty Fundamental.** ⚛️
