def deleteCoveredPoint(self, intervals: List[List[int]], idx: int) -> List[List[int]]:
    # TODO: Implement deleteCoveredPoint logic
    count = 0
    handled = False
    ans = []
    for interval in intervals:
        if handled:
            ans.append(interval)
            continue
        start = interval[0]
        end = interval[1]
        prev = count
        count += end - start
        if count > idx:
            handled = True
            if end - start == 1:
                continue
            if idx == prev:
                ans.append([start + 1, end])
            elif idx == count - 1:
                ans.append([start, end - 1])
            else:
                ans.append([start, start + idx - prev])
                ans.append([start + idx - prev + 1, end])
        else:
            ans.append(interval)
    return ans

