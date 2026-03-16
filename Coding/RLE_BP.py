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
runs = list(encode_stream(values))
print(runs)



def decoder(runs):
    for run in runs:
        run = run.strip()

        if run.startswith("RLE[") and run.endswith("]"):
            inside = run[4:-1]   # 例如 "5,8"
            value_str, count_str = inside.split(",")
            value = int(value_str)
            count = int(count_str)

            for _ in range(count):
                yield value

        elif run.startswith("BP[") and run.endswith("]"):
            inside = run[3:-1]   # 例如 "1,2,3"
            if inside:           # 防止空 BP[]
                for x in inside.split(","):
                    yield int(x)

        else:
            raise ValueError(f"Invalid run: {run}")

print(list(decoder(runs)))