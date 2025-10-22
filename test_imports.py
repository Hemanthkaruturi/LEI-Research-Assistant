"""Simple test to verify all imports work correctly."""

try:
    # Test backend imports
    from backend.services.gleif_service import GLEIFService
    from backend.services.gemini_service import GeminiService
    from backend.lei_lookup import LEILookup

    print("✓ All backend imports successful")

    # Test that classes can be instantiated (without API calls)
    gleif = GLEIFService()
    print("✓ GLEIFService instantiated")

    # Test name normalization function
    lei_lookup = LEILookup("fake_key_for_test")
    normalized = lei_lookup._normalize_name("Google Inc.")
    assert normalized == "google", f"Expected 'google', got '{normalized}'"
    print("✓ Name normalization working correctly")

    print("\n✅ All tests passed! The application structure is correct.")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install dependencies: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
