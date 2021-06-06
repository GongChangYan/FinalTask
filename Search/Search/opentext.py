from os import lseek
from django.shortcuts import render
import sys
sys.path.append("../")
from SearchEngine import Engine
import re

def opentext(request):
    r = {'results': {}}
    engine = Engine.getEngine()
    if 'id' in request.GET:
        ls = engine.searchByID(id=request.GET.get('id'))
        l = ls['_source']
        d = {}
        d['文首'] =  l['文首']
        d['标准法院名称'] = {"text": l['标准法院名称'], "url": '/search/?court={}'.format(l['标准法院名称'])}
        d['案件类别'] =  {"text": l['案件类别'], "url": '/search/?category={}'.format(l['案件类别'])}
        d['文书种类'] = l['文书种类']
        d['当事人'] = l['当事人']
        d['案件基本情况'] = l['案件基本情况']
        d['裁判分析过程'] = l['裁判分析过程']
        d['判决结果'] = l['判决结果']
        d['文尾'] = []
        d['法律法条'] = []
        
        li = l['文尾'].strip().split(" ")
        for i in li:
            n = re.findall('(?<=审判长|审判员|书记员).*$',i.strip())
            if len(n) != 0:
                d['文尾'].append({"text": i.strip(), "url": '/search/?judge={}'.format(n[0])})
            else:
                d['文尾'].append({"text": i.strip(), "url": "" })
        
        li = l['法律法条'].strip().split("+")
        for i in li:
            d['法律法条'].append({"text": i.strip(), "url": '/search/?law={}'.format(i.strip())}) 
        
        r['results'] = d

        r['SimilarCase'] = []
        ls = engine.searchSimilarCase(id=request.GET.get('id'))
        for l in ls:
            d = {}
            d['url'] = '/text/?id=' + l['_id']
            d['文首'] = l['_source']['文首']
            d['全文'] = l['_source']['全文']
            r['SimilarCase'].append(d)
        
        r['SimilarLaws'] = []
        ls = engine.searchSimilarLaws(id=request.GET.get('id'))
        for l in ls:
            d = {}
            d['url'] = '/text/?id=' + l['_id']
            d['文首'] = l['_source']['文首']
            d['全文'] = l['_source']['全文']
            r['SimilarLaws'].append(d)
        
    return render(request, "fulltext.html", r)