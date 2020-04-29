from collections import Counter
import unittest

def is_valid_password(password, require_double_group=False):
    password_str = str(password)
    if sorted(password_str) != list(password_str):
        return False
    # Since digits are ascending, we can use Counter to check repeats directly.
    digit_counts = Counter(password_str)
    if require_double_group:
        return any(count == 2 for count in digit_counts.values())
    else:
        return any(count > 1 for count in digit_counts.values())

def main():
    with open("day04.txt") as input_file:
        lower, upper  = [int(x) for x in input_file.read().split("-")]
    num_passwords = 0
    num_passwords_strict = 0
    for num in range(lower, upper+1):
        if is_valid_password(num):
            num_passwords += 1
        if is_valid_password(num, require_double_group=True):
            num_passwords_strict += 1
    print("Part one passwords: {}".format(num_passwords))
    print("Part two passwords: {}".format(num_passwords_strict))

if __name__ == '__main__':
    main()

class TestIsValidPassword(unittest.TestCase):
    def test_is_valid_password(self):
        self.assertTrue(is_valid_password(111123))
        self.assertTrue(is_valid_password(111111))
        self.assertFalse(is_valid_password(223450))
        self.assertFalse(is_valid_password(123789))
    
    def test_is_valid_password_require_double_group(self):
        self.assertTrue(is_valid_password(112233, require_double_group=True))
        self.assertFalse(is_valid_password(123444, require_double_group=True))
        self.assertTrue(is_valid_password(111122, require_double_group=True))
        self.assertFalse(is_valid_password(222234, require_double_group=True))
        self.assertTrue(is_valid_password(122444, require_double_group=True))
