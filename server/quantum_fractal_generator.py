"""
Quantum Fractal Generator
Generate SVG fractals from blockchain transaction hashes

This module transforms blockchain data into artistic visualizations,
embodying the "Lyrical Lens" principle from the Sacred Trinity.
"""

import hashlib
import math
from typing import List, Tuple, Dict, Any


class QuantumFractalGenerator:
    """Generate SVG fractals from transaction hashes"""
    
    def __init__(self, tx_hash: str):
        """
        Initialize generator with transaction hash
        
        Args:
            tx_hash: Transaction hash to derive fractal from
        """
        self.tx_hash = tx_hash
        self.hash_bytes = hashlib.sha256(tx_hash.encode()).digest()
        
    def _get_hash_value(self, index: int, max_val: int = 255) -> int:
        """Extract a value from hash at given index"""
        return self.hash_bytes[index % len(self.hash_bytes)] % (max_val + 1)
    
    def _get_hash_float(self, index: int) -> float:
        """Extract a normalized float (0-1) from hash at given index"""
        return self._get_hash_value(index) / 255.0
    
    def _get_color_from_hash(self, index: int) -> str:
        """Generate HSL color from hash"""
        hue = self._get_hash_value(index, 360)
        saturation = 50 + self._get_hash_value(index + 1, 50)
        lightness = 40 + self._get_hash_value(index + 2, 40)
        return f"hsl({hue}, {saturation}%, {lightness}%)"
    
    def generate_recursive_circles(
        self, 
        center_x: float, 
        center_y: float, 
        radius: float, 
        depth: int,
        index_offset: int = 0
    ) -> List[str]:
        """
        Generate recursive circular fractal
        
        Args:
            center_x: X coordinate of circle center
            center_y: Y coordinate of circle center
            radius: Circle radius
            depth: Recursion depth remaining
            index_offset: Offset for hash value extraction
            
        Returns:
            List of SVG circle elements
        """
        if depth <= 0 or radius < 2:
            return []
        
        elements = []
        
        # Main circle
        color = self._get_color_from_hash(index_offset)
        opacity = 0.3 + (self._get_hash_float(index_offset + 3) * 0.5)
        stroke_width = 1 + (radius / 50)
        
        elements.append(
            f'<circle cx="{center_x:.2f}" cy="{center_y:.2f}" '
            f'r="{radius:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width:.2f}" '
            f'opacity="{opacity:.2f}"/>'
        )
        
        # Generate child circles
        num_children = 3 + self._get_hash_value(index_offset + 4, 5)
        child_radius = radius * (0.3 + self._get_hash_float(index_offset + 5) * 0.3)
        
        for i in range(num_children):
            angle = (2 * math.pi * i / num_children) + self._get_hash_float(index_offset + 6) * math.pi
            distance = radius * 0.6
            child_x = center_x + distance * math.cos(angle)
            child_y = center_y + distance * math.sin(angle)
            
            elements.extend(
                self.generate_recursive_circles(
                    child_x, child_y, child_radius, 
                    depth - 1, index_offset + i * 7
                )
            )
        
        return elements
    
    def generate_mandala_pattern(self) -> List[str]:
        """Generate mandala-style pattern from hash"""
        elements = []
        center = 150.0
        
        # Number of petals derived from hash
        num_petals = 6 + self._get_hash_value(0, 12)
        
        for i in range(num_petals):
            angle = (2 * math.pi * i / num_petals)
            
            # Petal size varies based on hash
            petal_size = 30 + self._get_hash_float(i * 2) * 40
            
            # Petal position
            distance = 60 + self._get_hash_float(i * 2 + 1) * 30
            x = center + distance * math.cos(angle)
            y = center + distance * math.sin(angle)
            
            color = self._get_color_from_hash(i * 3)
            opacity = 0.4 + self._get_hash_float(i * 3 + 1) * 0.4
            
            # Draw petal as ellipse
            rotate = math.degrees(angle)
            elements.append(
                f'<ellipse cx="{x:.2f}" cy="{y:.2f}" '
                f'rx="{petal_size:.2f}" ry="{petal_size * 0.5:.2f}" '
                f'fill="{color}" opacity="{opacity:.2f}" '
                f'transform="rotate({rotate:.2f} {x:.2f} {y:.2f})"/>'
            )
        
        # Central circle
        central_color = self._get_color_from_hash(100)
        elements.append(
            f'<circle cx="{center}" cy="{center}" r="20" '
            f'fill="{central_color}" opacity="0.8"/>'
        )
        
        return elements
    
    def generate_sierpinski_variation(self, size: float = 200.0) -> List[str]:
        """Generate Sierpinski triangle variation"""
        elements = []
        center = 150.0
        
        def triangle_vertices(cx: float, cy: float, size: float) -> List[Tuple[float, float]]:
            """Calculate triangle vertices"""
            height = size * math.sqrt(3) / 2
            return [
                (cx, cy - height * 2/3),  # Top
                (cx - size / 2, cy + height / 3),  # Bottom left
                (cx + size / 2, cy + height / 3),  # Bottom right
            ]
        
        def draw_sierpinski(cx: float, cy: float, size: float, depth: int, offset: int) -> None:
            """Recursively draw Sierpinski variation"""
            if depth <= 0 or size < 5:
                return
            
            vertices = triangle_vertices(cx, cy, size)
            color = self._get_color_from_hash(offset)
            opacity = 0.2 + self._get_hash_float(offset + 1) * 0.4
            
            # Draw triangle
            points = " ".join([f"{x:.2f},{y:.2f}" for x, y in vertices])
            elements.append(
                f'<polygon points="{points}" fill="none" '
                f'stroke="{color}" stroke-width="1.5" '
                f'opacity="{opacity:.2f}"/>'
            )
            
            # Recurse on smaller triangles
            new_size = size / 2
            for i, (vx, vy) in enumerate(vertices):
                draw_sierpinski(vx, vy, new_size, depth - 1, offset + i * 5)
        
        max_depth = 2 + self._get_hash_value(0, 3)
        draw_sierpinski(center, center, size, max_depth, 0)
        
        return elements
    
    def generate_svg(
        self, 
        width: int = 300, 
        height: int = 300,
        fractal_type: str = "recursive"
    ) -> str:
        """
        Generate complete SVG fractal
        
        Args:
            width: SVG width
            height: SVG height
            fractal_type: Type of fractal ("recursive", "mandala", "sierpinski")
            
        Returns:
            Complete SVG XML string
        """
        # Determine fractal type from hash if not specified
        if fractal_type == "auto":
            type_val = self._get_hash_value(0, 3)
            fractal_type = ["recursive", "mandala", "sierpinski"][type_val % 3]
        
        # Generate fractal elements
        if fractal_type == "mandala":
            elements = self.generate_mandala_pattern()
        elif fractal_type == "sierpinski":
            elements = self.generate_sierpinski_variation()
        else:  # recursive (default)
            depth = 2 + self._get_hash_value(1, 3)
            elements = self.generate_recursive_circles(150, 150, 80, depth)
        
        # Construct SVG
        svg_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'    <!-- Generated from tx: {self.tx_hash[:16]}... -->',
            f'    <!-- Fractal type: {fractal_type} -->',
            '    <rect width="100%" height="100%" fill="#0a0a1a"/>',
            '    <g id="fractal">',
        ]
        
        svg_parts.extend([f'        {elem}' for elem in elements])
        
        svg_parts.extend([
            '    </g>',
            f'    <text x="{width/2}" y="{height - 10}" text-anchor="middle" '
            f'fill="#DDA0DD" font-size="10" opacity="0.7">TX: {self.tx_hash[:12]}...</text>',
            '</svg>'
        ])
        
        return '\n'.join(svg_parts)


def generate_resonance_fractal(tx_hash: str, fractal_type: str = "auto") -> str:
    """
    Convenience function to generate fractal from transaction hash
    
    Args:
        tx_hash: Transaction hash
        fractal_type: Type of fractal to generate
        
    Returns:
        SVG XML string
    """
    generator = QuantumFractalGenerator(tx_hash)
    return generator.generate_svg(fractal_type=fractal_type)


if __name__ == "__main__":
    # Test generation
    test_hash = "0x1234567890abcdef1234567890abcdef12345678"
    
    print("Generating test fractals...")
    
    for ftype in ["recursive", "mandala", "sierpinski"]:
        svg = generate_resonance_fractal(test_hash, ftype)
        filename = f"test_fractal_{ftype}.svg"
        with open(filename, "w") as f:
            f.write(svg)
        print(f"✓ Generated {filename}")
