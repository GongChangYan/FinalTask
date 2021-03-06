## Engine接口说明

目前支持按**全文，当事人，案件类别，标准法院名称，法律法条，文首**（内含法官信息）进行搜索

分别对应**searchAllText，searchPerson，searchCaseType，searchCourt，searchLaw，searchJudge**函数

这六个函数需要的参数**target**为搜索对象，target为一个字符串
返回值为num，cost_time，和result，num为搜索结果的条数，cost_time为执行搜索花费的时间
而result为一个列表，内含最多50个dict，每个dict中含有一篇判决书，dict格式如下
{'_index': 'test',
    '_type': '\_doc',
    '\_id': '8',
    '\_score': 4.0158467,
    '\_source': { 
        '全文': '福建省晋江市案的审判员、书记员署名。 ',
        '文首': '福建省晋江市人民法院 民事裁定书 （2014）晋民初字第2732号 ', 
        '标准法院名称': '晋江市人民法院', 
        '案件类别': '民事案件', 
        '文书种类': '裁定书', 
        '审判程序': '一审案件', 
        '案件类型': '民事一审案件', 
        '当事人': '原告洪德河，律师',
        '案件基本情况':'1952年晋江县',
        '裁判分析过程': ' 本院认为，本案中：',
        '判决结果': ' 驳回原告'
        '文尾': '审判员吴陈斌', 
        '法律法条': ' + 《中华人民共和国民事诉讼法》第一百一十九条第（一）项 + 《中华人民共和国民事诉讼法》第一百一十九条'
    }
}
访问**\_source**即可得到文档，访问**_id**即可得到文档的id，这在搜索相似案件中需要用到。

searchSimilarCase和searchSimilarLaws两个函数分别可以用来查找与某案件全文相似的案件和涉及法律法条相似的案件，传入的参数id即为案件_id的值，例如例子的id为'8'

高级搜索使用的函数为fancySearch，函数参数为一个长度为6的列表，分别对应全文，当事人，案件类别，标准法院名称，法律法条，文尾六项搜索内容，
如果内容为空，对应的字符串应该为" "（仅有一个空格），但该列表的第一项，即全文的搜索内容一定不能为空

getGuideString函数可以获得传入字符串对应的引导词列表，列表最多含有10个引导词