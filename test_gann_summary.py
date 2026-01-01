


from gann_tools_demo import square_of_nine_level

def test_gann_angle():
    """Test the square_of_nine_level function as angle proxy."""
    try:
        # Example: base 100, steps 45
        result = square_of_nine_level(100, 45)
        assert isinstance(result, float) or isinstance(result, int)
    except AssertionError:
        print("square_of_nine_level (angle proxy) test failed.")
        return False
    return True

def test_square_of_nine():
    """Test the square_of_nine_level function."""
    try:
        result = square_of_nine_level(144, 45)
        assert isinstance(result, float) or isinstance(result, int)
    except AssertionError:
        print("square_of_nine_level test failed.")
        return False
    return True

def test_gann_summary():
    all_passed = True
    if not test_gann_angle():
        all_passed = False
    if not test_square_of_nine():
        all_passed = False
    if all_passed:
        print("All tests passed.")

if __name__ == "__main__":
    test_gann_summary()
