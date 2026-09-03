import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
import snippets


class ExtractTests(unittest.TestCase):
    def file(self, text, dirname="step_01"):
        root = Path(tempfile.mkdtemp())
        path = root / "models" / dirname / "application.alan"
        path.parent.mkdir(parents=True); path.write_text(text)
        return root, path

    def text(self, source):
        _, path = self.file(source); chunks, _, _ = snippets.extract_file(path)
        return {n: "\n...\n".join("\n".join(c) for c in cs) for n,cs in chunks.items()}

    def test_multi_chunk_hide_skip_nested_overlap(self):
        got = self.text("//@ begin x\n\ta\n//@ hide x\n\tsecret\n\tmore\n//@ show x\n\tb\n//@ end x\n//@ begin x\n\tc\n//@ end x\n//@ begin a\nA\n//@ begin b\nB\n//@ end a\nC\n//@ end b\n//@ begin s\nA\n//@ skip s\nNO\n//@ show s\nB\n//@ end s\n")
        self.assertEqual(got["x"], "a\n...\nb\n...\nc")
        self.assertEqual(got["a"], "A\nB")
        self.assertEqual(got["b"], "B\nC")
        self.assertEqual(got["s"], "A\nB")

    def test_cut_strip_all_dedent_crlf(self):
        got = self.text("//@ all whole\r\n//@ begin x strip-comments\r\n\t  'a//b' // tail\r\n\t\r\n\tend CUT rest\r\n//@ end x cut=\"CUT\"\r\n")
        self.assertEqual(got["x"], "  'a//b'\n\nend ...")
        self.assertEqual(got["whole"], "  'a//b' // tail\n\nend CUT rest")
        self.assertFalse(got["x"].endswith("\n"))

    def test_errors(self):
        cases = [
            "//@ nope x\n", "x //@ begin x\n", "//@ begin x\n//@ begin x\n",
            "//@ end x\n", "//@ begin x\n", "//@ begin x\na\n//@ end x cut=\"z\"\n",
            "//@ begin x\n{{ hi }}\n//@ end x\n", "//@ all x\n//@ all y\n",
        ]
        for source in cases:
            with self.subTest(source=source):
                _, path = self.file(source)
                with self.assertRaises(snippets.ExtractError): snippets.extract_file(path)

    def test_duplicate(self):
        root, path = self.file("//@ begin x\na\n//@ end x\n")
        p2 = root / "models" / "step_02" / "application.alan"; p2.parent.mkdir(); p2.write_text("//@ begin x\nb\n//@ end x\n")
        with self.assertRaises(snippets.ExtractError): snippets.extract_all(root / "models")

    def test_audit_fence_and_folder(self):
        root = Path(tempfile.mkdtemp()); old = snippets.ROOT
        try:
            snippets.ROOT = root
            v = root / "pages/tutorials/model/v"; (v/"models/step_01").mkdir(parents=True); (v/"snippets").mkdir()
            (v/"models/step_01/application.alan").write_text("//@ begin one\nx\n//@ end one\n")
            (v/"snippets/one.alan").write_text("x")
            (v/"page.md").write_text("<tutorial folder: x/step_01/>\n```js\n{% include_relative snippets/one.alan %}\n```\n")
            errors, warnings = snippets.verify("v", platform=None, no_compile=True)
            self.assertEqual((errors, warnings), (0, 0))
        finally: snippets.ROOT = old

    @unittest.skipUnless(os.environ.get("ALAN_DEVENV"), "needs Alan devenv")
    def test_compiler_optional(self):
        self.assertTrue(Path(os.environ["ALAN_DEVENV"]).exists())


if __name__ == "__main__": unittest.main()
