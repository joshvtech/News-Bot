def check(args):
    if args in ["bbc news", "bbcnews", "bbc"]:
        return("bbcNews")
    elif args == "cnet":
        return("cnet")
    elif args in ["new york times", "newyorktimes", "nytimes", "nyt"]:
        return("newYorkTimes")
    elif args in ["sky news", "skynews", "sky"]:
        return("skyNews")
    elif args in ["the telegraph", "thetelegraph","telegraph"]:
        return("theTelegraph")
    else:
        return(None)
