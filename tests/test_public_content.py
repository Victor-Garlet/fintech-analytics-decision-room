from pathlib import Path
import unittest

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIRECTORY = PROJECT_ROOT / "content" / "posts"
VISUALS_DIRECTORY = PROJECT_ROOT / "content" / "visuals"

INTRO = "I'm using Wise's public disclosures and synthetic data to simulate how a Senior Data Analyst could work through a fintech problem from question to decision."
DISCLOSURE = "This is an independent simulation inspired by Wise's public disclosures. I am not affiliated with Wise. All transaction-level data and project findings are synthetic; any company-level figures are sourced from public reports."


class PublicContentTestCase(unittest.TestCase):
    def test_eight_posts_follow_the_release_contract(self):
        posts = sorted(POSTS_DIRECTORY.glob("episode_*.md"))
        self.assertEqual(len(posts), 8)

        for episode, path in enumerate(posts, start=1):
            text = path.read_text(encoding="utf-8")
            post = text.split("## Post copy\n\n", maxsplit=1)[1]
            self.assertIn(f"**30 Days Inside a European Fintech [{episode}/8]**", post)
            self.assertEqual(post.count(INTRO), 1)
            self.assertEqual(post.count(DISCLOSURE), 1)
            self.assertNotIn("—", post)
            self.assertGreaterEqual(len(post), 1700)
            self.assertLessEqual(len(post), 2400)

    def test_eight_visuals_use_the_linkedin_portrait_ratio(self):
        visuals = sorted(VISUALS_DIRECTORY.glob("episode_*.png"))
        self.assertEqual(len(visuals), 8)

        for path in visuals:
            with Image.open(path) as image:
                self.assertEqual(image.size, (1800, 2250))

    def test_editorial_calendar_keeps_publication_on_hold(self):
        calendar = (PROJECT_ROOT / "content" / "editorial_calendar.md").read_text(encoding="utf-8")
        self.assertEqual(calendar.count("Hold for approval"), 8)


if __name__ == "__main__":
    unittest.main()
