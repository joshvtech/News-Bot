def check(args):
    if args in ["bbcnews", "bbc news", "bbc"]:
        return("bbcNews")
    elif args == "cnet":
        return("cnet")
    elif args in ["newyorktimes", "new york times", "nytimes", "nyt"]:
        return("newYorkTimes")
    elif args in ["skynews", "sky news", "sky"]:
        return("skyNews")
    elif args in ["thetelegraph", "telegraph"]:
        return("theTelegraph")
    else:
        return(None)
