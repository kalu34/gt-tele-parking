import random
import string

def generate_random_string():
    # Generate 3 random uppercase letters
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    # Generate 3 random digits
    numbers = ''.join(random.choices(string.digits, k=3))
    
    # Combine letters and numbers
    random_string = letters + numbers
    
    return random_string

# Example usage
if __name__ == "__main__":
    print(generate_random_string())