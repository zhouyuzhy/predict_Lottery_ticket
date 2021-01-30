

def crossesOver(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed over that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1) - 1] <= stream2:
            return 0
        else:
            if stream1[len(stream1) - 2] > stream2:
                return 0
            elif stream1[len(stream1) - 2] < stream2:
                return 1
            else:
                x = 2
                while stream1[len(stream1) - x] == stream2:
                    x = x + 1
                if stream1[len(stream1) - x] < stream2:
                    return 1
                else:
                    return 0
    # Check if stream1 has crossed over stream2
    else:
        if stream1[len(stream1) - 1] <= stream2[len(stream2) - 1]:
            return 0
        else:
            if stream1[len(stream1) - 2] > stream2[len(stream2) - 2]:
                return 0
            elif stream1[len(stream1) - 2] < stream2[len(stream2) - 2]:
                return 1
            else:
                x = 2
                while stream1[len(stream1) - x] == stream2[len(stream2) - x]:
                    x = x + 1
                if stream1[len(stream1) - x] < stream2[len(stream2) - x]:
                    return 1
                else:
                    return 0


def crossesUnder(stream1, stream2):
    # If stream2 is an int or float, check if stream1 has crossed under that fixed number
    if isinstance(stream2, int) or isinstance(stream2, float):
        if stream1[len(stream1) - 1] >= stream2:
            return 0
        else:
            if stream1[len(stream1) - 2] < stream2:
                return 0
            elif stream1[len(stream1) - 2] > stream2:
                return 1
            else:
                x = 2
                while stream1[len(stream1) - x] == stream2:
                    x = x + 1
                if stream1[len(stream1) - x] > stream2:
                    return 1
                else:
                    return 0
    # Check if stream1 has crossed under stream2
    else:
        if stream1[len(stream1) - 1] >= stream2[len(stream2) - 1]:
            return 0
        else:
            if stream1[len(stream1) - 2] < stream2[len(stream2) - 2]:
                return 0
            elif stream1[len(stream1) - 2] > stream2[len(stream2) - 2]:
                return 1
            else:
                x = 2
                while stream1[len(stream1) - x] == stream2[len(stream2) - x]:
                    x = x + 1
                if stream1[len(stream1) - x] > stream2[len(stream2) - x]:
                    return 1
                else:
                    return 0

