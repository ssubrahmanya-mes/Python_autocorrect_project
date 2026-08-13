import re
import pkg_resources
from symspellpy import SymSpell, Verbosity

class TextCorrector:
    _instance = None

    def __new__(cls):
        """Singleton pattern to avoid reloading dictionary on every request."""
        if cls._instance is None:
            cls._instance = super(TextCorrector, cls).__new__(cls)
            cls._instance._initialize_symspell()
        return cls._instance

    def _initialize_symspell(self):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dictionary_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )
        bigram_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_bigramdictionary_en_243_342.txt"
        )
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
        self.sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)

    def correct_text(self, input_text: str) -> dict:
        """Corrects full sentences/paragraphs and tracks corrections."""
        if not input_text.strip():
            return {"corrected_text": "", "corrections": []}

        # Compound sentence correction
        suggestions = self.sym_spell.lookup_compound(
            input_text, max_edit_distance=2, ignore_non_words=True
        )
        corrected_sentence = suggestions[0].term if suggestions else input_text

        # Extract words for diff comparison
        orig_words = re.findall(r'\b\w+\b', input_text)
        corr_words = re.findall(r'\b\w+\b', corrected_sentence)

        corrections = []
        for orig, corr in zip(orig_words, corr_words):
            if orig.lower() != corr.lower():
                corrections.append({"original": orig, "corrected": corr})

        return {
            "corrected_text": corrected_sentence,
            "corrections": corrections
        }