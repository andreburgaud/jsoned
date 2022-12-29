import unittest
import lexer

JSON = """
[
  {
    "name": "Molecule Man",
    "age": 29,
    "secretIdentity": "Dan Jukes",
    "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
  },
  {
    "name": "Madame Uppercut",
    "age": 39,
    "secretIdentity": "Jane Wilson",
    "powers": [
      "Million tonne punch",
      "Damage resistance",
      "Superhuman reflexes"
    ]
  }
]
"""

JSON2 = """
{
    "name": "Molecule Man",
    "age": 29,
    "secretIdentity": "Dan Jukes",
    "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
}
"""

JSON3 = """{"numbers":["un","deux","trois"]}"""

class TestJsonLexer(unittest.TestCase):

    def test_lexer(self):
        for token_id, start, end in lexer.lexer(JSON):
            print(f">>> {token_id=}")
            print(f">>> {start=}")
            print(f">>> {end=}")


if __name__ == '__main__':
    unittest.main()