import gui

from regex_generator import generate_regex
from regex_explainer import explain_regex
from regex_tester import test_regex


print("=" * 45)
print("        AI REGEX GENERATOR")
print("=" * 45)

description = input("\nDescribe the regex you want:\n> ")

regex = generate_regex(description)

print("\nGenerated Regex:\n")
print(regex)

print("\nExplanation:\n")
print(explain_regex(regex))

text = input("\nEnter sample text to test:\n> ")

result = test_regex(regex, text)

print("\nResult:")
print(result)