"""Helper used by the problem files. Each problem: our own words, our own solution, our own tests."""
ALL = []

def P(slug, title, lc, diff, topic, story, trick, hints, sol, tests, time, space, **kw):
    d = dict(slug=slug, title=title, lc=lc, diff=diff, topic=topic, story=story.strip(), trick=trick.strip(),
             hints=hints, solution=sol.strip('\n'), tests=tests, time=time, space=space)
    d.update(kw)
    ALL.append(d)
