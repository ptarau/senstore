from senstore.embedder import SentEmbedder
from senstore.segmenter import Segmenter, file2text


def test_segmenter(fname="~/tmp/lost-time.txt"):  # Proust's "In Search of Lost Time"
    # replace this with your own large file test
    seg = Segmenter(max_chunk_size=10000)
    text = file2text(fname)
    sents = seg.text2sents(text)
    print("SENTS:", len(sents))
    print("TIMES:", seg.times)
    # print(sents[-10:])
    # SENTS: 30610
    # TIMES: 85.23939895629883


def test_segmenter_():
    seg = Segmenter()
    print(
        seg.text2sents(
            """Dr. Cat, 3.14 years old, sits on the mat. 
         Mr. Dog, old and Texas-based, barks at her.

         """
        )
    )

    print(
        seg.text2sents(
            """
            Who cares about pi being exactly 3.14 something or not? 

            I do!

        """
        )
    )

    print("TIMES:", seg.times)


def test_embedder():
    text = """Graph-based NLP is an approach that uses graph structures 
    to represent and analyze natural language data. In this approach, words, 
    phrases, or sentences are represented as nodes in a graph, and the r
    elationships between them are represented as edges. This allows for 
    the modeling of complex relationships and dependencies in language data.   
    Graph-based NLP has several advantages over traditional NLP methods. 
    One of the main advantages is its ability to capture the global 
    structure of language data. Traditional NLP methods often rely on 
    local context, such as n-grams or bag-of-words models, which 
    can miss important relationships between words or phrases that are 
    not in close proximity. Graph-based NLP, on the other hand, can 
    capture long-range dependencies and relationships between words
    or phrases that may be far apart in the text.            
    """
    se = SentEmbedder("test_embedder")
    se.digest_text(text)
    q = "What are the advantages of graph based NLP?"
    answers = se.query(q, top_k=3)
    print("\nanswers for query:", q)
    print(answers)
    assert se.sents is not None
    for answer in answers:
        print(answer)
    se.save()

    se2 = SentEmbedder("test_embedder")
    se2.load()

    q = "How is the global structure of the text captured?"
    answers = se2.query(q, top_k=3)
    print("\nanswers for query:", q)
    for answer in answers:
        print(answer)


def test_folder():
    se = SentEmbedder("test_embedder_folder", caching=True)
    se.digest_folder("test_in/")  # replace with your own folder with .txt files
    q = "What are the advantages of graph based NLP?"
    answers = se.query(q, top_k=3)
    print("\nanswers for query:", q)
    print(answers)
    assert se.sents is not None
    for answer in answers:
        print(answer)
    se.save()

    se2 = SentEmbedder("test_embedder_folder")
    se2.load()

    q = "what are first class logic engines in BinProlog?"
    answers = se2.query(q, top_k=3)
    print("\nanswers for query:", q)
    for answer in answers:
        print(answer)


if __name__ == "__main__":
    test_segmenter_()
    test_embedder()
    test_folder()
