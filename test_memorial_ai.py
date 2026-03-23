#!/usr/bin/env python3
"""
Test script for OINIO Memorial AI Generator
Demonstrates the AI-powered memorial content generation capabilities
"""

import asyncio
import json
import sys
from pathlib import Path

# Add server directory to path
server_path = str(Path(__file__).parent / "server")
sys.path.insert(0, server_path)

from memorial_ai_generator import generate_complete_memorial_package, MemorialProfile

async def test_memorial_generation():
    """Test the memorial AI generation with sample profiles"""

    print("🏛️ OINIO Memorial AI Generator - Test Suite")
    print("=" * 50)

    # Test Profile 1: Grandmother
    print("\n📖 Generating memorial for Eleanor Rose (Grandmother)...")
    profile1 = MemorialProfile(
        name="Eleanor Rose",
        birth_date="March 15, 1945",
        passing_date="December 20, 2025",
        relationship="Grandmother",
        personality_traits=["kind", "wise", "loving", "strong"],
        achievements=["raised five children", "volunteered at church", "master gardener"],
        favorite_memories=["Sunday dinners", "garden walks", "grandchildren's laughter"],
        legacy_message="Love each other as I loved you"
    )

    memorial1 = await generate_complete_memorial_package(profile1, "Sarah Johnson")

    print("✅ Memorial narrative generated")
    print(f"📏 Length: {len(memorial1['narrative'])} characters")
    print(f"📝 Preview: {memorial1['narrative'][:200]}...")

    # Test Profile 2: Father
    print("\n📖 Generating memorial for Robert Chen (Father)...")
    profile2 = MemorialProfile(
        name="Robert Chen",
        birth_date="January 8, 1972",
        passing_date="November 15, 2025",
        relationship="Father",
        personality_traits=["dedicated", "hardworking", "funny", "protective"],
        achievements=["built family business", "coached little league", "community volunteer"],
        favorite_memories=["fishing trips", "family vacations", "teaching life lessons"],
        legacy_message="Work hard, love deeply, laugh often"
    )

    memorial2 = await generate_complete_memorial_package(profile2, "Michael Chen")

    print("✅ Memorial narrative generated")
    print(f"📏 Length: {len(memorial2['narrative'])} characters")
    print(f"📝 Preview: {memorial2['narrative'][:200]}...")

    # Save test results
    test_results = {
        "test_profiles": [
            {
                "profile": memorial1["profile"],
                "narrative_preview": memorial1["narrative"][:300] + "...",
                "poem_preview": memorial1["poem"][:150] + "...",
                "reflection_preview": memorial1["reflection"][:200] + "..."
            },
            {
                "profile": memorial2["profile"],
                "narrative_preview": memorial2["narrative"][:300] + "...",
                "poem_preview": memorial2["poem"][:150] + "...",
                "reflection_preview": memorial2["reflection"][:200] + "..."
            }
        ],
        "generation_timestamp": memorial1["generated_at"],
        "ai_status": "azure_ai" if hasattr(sys.modules.get('memorial_ai_generator'), 'memorial_ai') and hasattr(sys.modules['memorial_ai_generator'].memorial_ai, 'client') and sys.modules['memorial_ai_generator'].memorial_ai.client else "demo_mode"
    }

    with open("memorial_ai_test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)

    print("\n💾 Test results saved to memorial_ai_test_results.json")
    print("\n🎯 Memorial AI Test Suite Complete!")
    print("🌟 Ready to enhance the OINIO Soul System with AI-powered memorial generation")

    return test_results

if __name__ == "__main__":
    asyncio.run(test_memorial_generation())</content>
<parameter name="filePath">c:\Users\Colle\projects\pi-forge-quantum-genesis\test_memorial_ai.py