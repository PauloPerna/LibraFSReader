import unittest
from ..Identifier import IsNubank

class TestIsNubank(unittest.TestCase):
    def test_is_nubank(self):
        # Test that the function returns True when the input text contains the Nubank CNPJ number
        text = "Our company's CNPJ is 18.236.120/0001-58, which is the same as Nubank's CNPJ."
        self.assertTrue(IsNubank(text))
        
        # Test that the function returns False when the input text does not contain the Nubank CNPJ number
        text = "Our company's CNPJ is 12.345.678/0001-90, which is not the same as Nubank's CNPJ."
        self.assertFalse(IsNubank(text))
        
        # Test that the function returns False when the input text is empty
        text = ""
        self.assertFalse(IsNubank(text))
        
        # Test that the function returns False when the input text is None
        text = None
        self.assertFalse(IsNubank(text))