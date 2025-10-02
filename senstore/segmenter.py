from time import time
import os
import pysbd


class Segmenter:
    """Segment text into sentences using pysbd."""

    def __init__(self, lang="en", max_chunk_size=10000):
        # approx 10 pages max chunk
        self.lang = lang
        self.max_chunk_size = max_chunk_size
        self.nlp = pysbd.Segmenter(language=lang, clean=False)
        self.times = 0

    def chunkify(self, text: str) -> list[str]:
        """Split text into chunks of max_chunk_size."""

        chunks = [
            text[i : i + self.max_chunk_size]
            for i in range(0, len(text), self.max_chunk_size)
        ]
        # print("*** TEXT LEN:", len(text), "CHUNKS:", len(chunks))
        return chunks

    def preprocess(self, text: str) -> list[list[str]]:
        """Preprocess text by replacing newlines and special characters, then segmenting into sentences."""
        text = text.replace("\u3002", ".")  # for Chinese dot

        chunks = self.chunkify(text)

        sentss = []
        for chunk in chunks:
            chunk = " ".join(chunk.split())
            sents = self.nlp.segment(chunk)
            sentss.append(sents)
        # print('!!! TEXT:', len(text), 'CHUNKS:', len(chunks), 'SENTS:', sum(map(len, sentss)))
        assert sentss, f"No good sentences after preprocessing text of len={len(text)}"
        return sentss

    def text2sents(self, text: str) -> list[str]:
        """Segment text into sentences and return a flat list of sentences."""
        t1 = time()
        assert self.nlp is not None
        assert text, "No text to segment"
        xss = self.preprocess(text)
        sents = [x.strip() for xs in xss for x in xs if x]
        t2 = time()
        self.times += t2 - t1
        assert sents, f"No good sentences after segmenting text of len={len(text)}"
        return sents


def file2text(fname: str) -> str:
    fname = os.path.expanduser(fname)
    assert os.path.exists(fname), f"File {fname} does not exist"
    with open(fname, "r") as f:
        text = f.read()
        return text


def segment_text(text: str) -> list[str]:
    seg = Segmenter()
    return seg.text2sents(text)


def segment_file(fname: str) -> list[str]:
    seg = Segmenter()
    text = file2text(fname)
    return seg.text2sents(text)
