def encode_stream(stream):
    it = iter(stream)
    bp = []
    pending = None
    has_pending = False

    def flush_bp():
        nonlocal bp
        if bp:
            s = "BP[" + ",".join(map(str, bp)) + "]"
            bp = []
            return s
        return None

    while True:
        if has_pending:
            cur = pending
            has_pending = False
        else:
            try:
                cur = next(it)
            except StopIteration:
                break

        count = 1

        while True:
            try:
                nxt = next(it)
            except StopIteration:
                nxt = None
                end = True
                break

            if nxt == cur:
                count += 1
            else:
                pending = nxt
                has_pending = True
                end = False
                break

        is_final_run = end

        if count >= 8 or (is_final_run and count > 1):
            x = flush_bp()
            if x:
                yield x
            yield f"RLE[{cur},{count}]"
        else:
            for _ in range(count):
                bp.append(cur)
                if len(bp) == 8:
                    x = flush_bp()
                    if x:
                        yield x

    x = flush_bp()
    if x:
        yield x


values = [1,2,3,4,5,5,5,5,5,5,5,5,5,5]
print(list(encode_stream(values)))