import os
from random import randint
import folder_funcs as ff


def generate_text(nblignes, nbmots):
    return "\n".join(" ".join("".join(chr(randint(33, 122)) for _ in range(randint(3, 16))) for _ in range(nbmots)) for _ in range(nblignes))

currdir = os.path.dirname(__file__)
test_dirname = "test_dir"
testdir = os.path.join(currdir, test_dirname)


testdir1 = os.path.join(testdir, "test1")
startnum = randint(10**5, 10**6-10)
for i in range(10):
    tdir = os.path.join(testdir1, f"{startnum+i}")
    ff.create_folder(tdir)
    for j in range(2):
        fpath = os.path.join(tdir, f"file{j+1:02d}.txt")
        with open(fpath, "w") as f:
            texte = generate_text(randint(3, 10), randint(3, 10))
            f.write(texte)