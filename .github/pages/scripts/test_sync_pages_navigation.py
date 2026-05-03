import sys
import textwrap
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

import sync_pages_navigation as sync


class SyncPagesNavigationTest(unittest.TestCase):
    def test_parses_index_hierarchy_and_renders_navigation_yaml(self):
        index_markdown = textwrap.dedent(
            """\
            ---
            tags: [EmbodiedAI]
            ---

            # Knowledge Base

            ## Topic A

            ### 论文摘要
            - [Paper A](summaries/paper-a.md)：summary.
            - [Paper With Colon: Part 1](summaries/paper-colon.md)：summary.

            ### 概念页
            - [Concept A](concepts/concept-a.md)：summary.

            ### 综合页
            - [Synthesis A](syntheses/synthesis-a.md)：summary.
            """
        )

        sections = sync.parse_index(index_markdown)
        self.assertEqual(
            sections,
            [
                {
                    "title": "Topic A",
                    "groups": [
                        {
                            "title": "论文摘要",
                            "items": [
                                {
                                    "title": "Paper A",
                                    "url": "/summaries/paper-a.html",
                                },
                                {
                                    "title": "Paper With Colon: Part 1",
                                    "url": "/summaries/paper-colon.html",
                                },
                            ],
                        },
                        {
                            "title": "概念页",
                            "items": [
                                {
                                    "title": "Concept A",
                                    "url": "/concepts/concept-a.html",
                                }
                            ],
                        },
                        {
                            "title": "综合页",
                            "items": [
                                {
                                    "title": "Synthesis A",
                                    "url": "/syntheses/synthesis-a.html",
                                }
                            ],
                        },
                    ],
                }
            ],
        )

        rendered = sync.render_navigation(sections)
        self.assertIn('title: "Topic A"', rendered)
        self.assertIn('title: "论文摘要"', rendered)
        self.assertIn('title: "Paper With Colon: Part 1"', rendered)
        self.assertIn('url: "/summaries/paper-colon.html"', rendered)
        self.assertIn('title: "Operation Log"', rendered)
        self.assertTrue(rendered.endswith("\n"))

    def test_validates_navigation_targets_against_wiki_files(self):
        sections = [
            {
                "title": "Topic A",
                "groups": [
                    {
                        "title": "论文摘要",
                        "items": [
                            {
                                "title": "Existing",
                                "url": "/summaries/existing.html",
                            },
                            {
                                "title": "Missing",
                                "url": "/summaries/missing.html",
                            },
                        ],
                    }
                ],
            }
        ]
        wiki_files = {Path("wiki/summaries/existing.md"), Path("wiki/log.md")}

        self.assertEqual(
            sync.find_missing_targets(sections, wiki_files),
            ["/summaries/missing.html"],
        )


if __name__ == "__main__":
    unittest.main()
