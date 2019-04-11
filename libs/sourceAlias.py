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
    elif args == "wired":
        return("wired")
    elif args in ["cbs news", "cbsnews", "cbs"]:
        return("cbsNews")
    else:
        return(None)
