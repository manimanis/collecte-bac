import os
from random import randint
from . import folder_funcs as ff


def generate_text(nblignes, nbmots):
    return "\n".join(" ".join("".join(chr(randint(33, 122)) for _ in range(randint(3, 16))) for _ in range(nbmots)) for _ in range(nblignes))

def run():
    currdir = os.path.dirname(os.path.dirname(__file__))
    test_dirname = "test_dir"
    testdir = os.path.join(currdir, test_dirname)


    testdir1 = os.path.join(testdir, "test1")
    if not os.path.exists(testdir1):
        startnum = randint(10**5, 10**6-10)
        for i in range(10):
            tdir = os.path.join(testdir1, f"{startnum+i}")
            ff.create_folder(tdir)
            for j in range(2):
                fpath = os.path.join(tdir, f"file{j+1:02d}.txt")
                with open(fpath, "w") as f:
                    texte = generate_text(randint(3, 10), randint(3, 10))
                    f.write(texte)


    testdir2 = os.path.join(testdir, "test2")
    if not os.path.exists(testdir2):
        startnum = randint(10**5, 10**6-10)
        for i in range(10):
            tdir = os.path.join(testdir2, f"{startnum+i}")
            ff.create_folder(tdir)
            for j in range(2):
                fpath = os.path.join(tdir, f"file{j+1:02d}.txt")
                with open(fpath, "w") as f:
                    texte = generate_text(randint(3, 10), randint(3, 10))
                    f.write(texte)
                if randint(0, 1) == 1:
                    dummydir = os.path.join(tdir, f"dir{randint(1, 10):02d}")
                    ff.create_folder(dummydir)
                    fpath = os.path.join(dummydir, "anotherfile.txt")
                    with open(fpath, "w") as f:
                        texte = generate_text(randint(3, 10), randint(3, 10))
                        f.write(texte)


if __name__ == "__main__":
    run()