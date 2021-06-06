import re
import math
from django.shortcuts import render
import sys
sys.path.append("../")
from SearchEngine import Engine

# 接收请求数据
def search(request):
    r ={'results': []}
    r['question'] = r['character'] = r['category'] = r["court"] = r["law"] = r["judge"] = ''
    request.encoding='utf-8'
    if request.GET:
        que = request.GET.get('q')
        character = request.GET.get('character')
        category = request.GET.get('category')
        court = request.GET.get('court')
        law = request.GET.get('law')
        judge = request.GET.get('judge')
        page = request.GET.get('p')
        engine = Engine.getEngine()
        if not page:
            page = 1
        else:
            page = int(page)
        if que:
            r["question"] = que
        else:
             que = " "
        if character:
            r["character"] = character
        else:
             character = " "
        if category:
            r["category"] = category
        else:
            category = " "
        if court:
            r["court"] = court
        else:
            court = " "
        if law:
            r["law"] = law
        else:
            law = " "
        if judge:
            r["judge"] = judge
        else:
            judge = " "

        num, cost_time, ls = engine.fancySearch([que, character, category, court, law, judge])
        r['time'] = format(cost_time, '.4f')
        r['num'] = num
        for l in ls[10 * page - 10 : 10 * page]:
            d = {}
            d['url'] = '/text/?id=' + l['_id']
            d['文首'] = l['_source']['文首']
            d['全文'] = l['_source']['全文']
            r['results'].append(d)
        r['pages'] = []
        s = '/search/?q={}&character={}&category={}&court={}&law={}&judge={}&p={}'.format(r["question"], r["character"],r["category"],r["court"],r["law"],r["judge"],max(1, page -1))
        r['pages'].append({'p': '上一页', 'url': s})
        for i in range(1, int(math.ceil(num / 10.)) + 1):
            s = '/search/?q={}&character={}&category={}&court={}&law={}&judge={}&p={}'.format(r["question"], r["character"],r["category"],r["court"],r["law"],r["judge"],i)
            r['pages'].append({'p': i, 'url': s})
        s = '/search/?q={}&character={}&category={}&court={}&law={}&judge={}&p={}'.format(r["question"], r["character"],r["category"],r["court"],r["law"],r["judge"],min(page + 1, int(math.ceil(num / 10.))))
        r['pages'].append({'p': '下一页', 'url': s})
    return render(request, "search_2.html", r)