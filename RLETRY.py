from typing import Iterable
def encoder(stream: Iterable[int]):
    it = iter(stream)
    bp = []

    def bp_flush():
        nonlocal bp
        if bp:
            s = "BP[" + ",".join(map(str, bp)) + "]"
            bp = []
        return s

    while True:
        try:
            cur = next(it)
        except StopIteration:
            break

        count = 1

        while True:
            try:
                nxt = next(it)
            except StopIteration:
                return


            if cur == nxt:
                count += 1

            else:
                pending =

        if count >= 8 or is_last_run:
            x = bp_flush()
            yield RLE
