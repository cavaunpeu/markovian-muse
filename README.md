# markovian-muse
Generating travel-blog posts with Markov chains

### To run
Simply run ```python3 muse.py``` on the command line. You'll then be prompted to enter a ```min_date```, ```max_date```, and ```muse_length```. Your post will be printed to screen.

### Using your own posts
This project includes a ```posts.py``` file containing a Python list of posts. Each post is a dictionary with keys ```date``` and ```text``` (and a few others which aren't actually used). To use your own corpus of posts, you'll need to format your data as such. If desired, simply edit the aforementioned file itself.

