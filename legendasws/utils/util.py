def searchcut(source, startsearch, endsearch, startpos=0):
    start = 0

    if startsearch:
        start = source.find(startsearch, startpos)
        if start == -1:
            return {"pos": -1, "pos_end": -1, "txt": ""}
        start += len(startsearch)

    end = 0

    if endsearch:
        end = source.find(endsearch, start)

    if end == -1:
        return {"pos": -1, "pos_end": -1, "txt": ""}

    if end == 0:
        return {"pos": start, "pos_end": end, "txt": source[start:]}

    if start == 0:
        return {"pos": start, "pos_end": end, "txt": source[:end]}

    return {"pos": start, "pos_end": end, "txt": source[start:end]}