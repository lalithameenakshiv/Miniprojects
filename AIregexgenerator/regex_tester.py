import re

def test_regex(regex, text):
    try:
        if re.fullmatch(regex, text):
            return "✅ Match Found"
        else:
            return "❌ No Match"
    except re.error:
        return "❌ Invalid Regex"