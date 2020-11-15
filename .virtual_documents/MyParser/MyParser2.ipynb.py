def 对象继承关系():
    from graphviz import Digraph
    dot = Digraph()
    # 节点描述
    dot.node('IMatch',xlabel='定义了Match函数')
    dot.node('Symbol',xlabel='标记符')
    dot.node('Terminal',xlabel='终结符')
    dot.node('MultiSymbol',xlabel='复合标记符，管理一个符号列表')
    dot.node('AndSymbol',xlabel='与复合标记符')
    dot.node('OrSymbol',xlabel='或复合标记符')
    dot.node('NonTerminal',xlabel='非终结符,包含一个或多个可称之为规则的标记符')
    dot.node('Starter',xlabel='开始符')
    # 继承关系描述
    dot.edge('IMatch','Symbol')
    dot.edge('Symbol','Terminal')
    dot.edge('Symbol','MultiSymbol')
    dot.edge('MultiSymbol','AndSymbol')
    dot.edge('MultiSymbol','OrSymbol')
    dot.edge('OrSymbol','NonTerminal')
    dot.edge('NonTerminal','Starter')
    # 显示图像
    dot

#对象继承关系()


from printobject import pp
from types import MethodType 


from typing import List, Tuple

# 匹配之后，剩余的待匹配的结果类型描述，形如(True,[(2,3),(5,6)])，第一项表示是否匹配成功，第2项表示匹配的结果，可能有多个待匹配项
# 每一个匹配项第一项表示起始索引，第2项表示长度
ParseResults = Tuple[bool,List[Tuple[int,int]]]


class IMatch:
    # 表示待解析的原始字符串
    Text :str = None

    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        '''
        功能描述：对待解析的字符串进行匹配，返回匹配的结果
        startIndex：待匹配字符串的起始索引
        length：待匹配字符串的长度
        isFullMatch：表示是否需要完全匹配，如果完全匹配，则必须字符串匹配完，才返回成功，只匹配部分，则匹配失败
        返回值：ParseResults类型，可能有多个剩余的待匹配项
        '''
        pass
    pass


class Symbol(IMatch): 
    # 重载&函数
    def __and__(self, dst):
        # 把两个标记符对象合并到一起
        def _与合并(s1,s2):
            if type(s2)==AndSymbol:
                s1.symbolList.extend(s2.symbolList)
            else:
                s1.symbolList.append(s2)
        newSymbol = AndSymbol()
        _与合并(newSymbol,self)
        _与合并(newSymbol,dst)
        return newSymbol
    
    # 重载|函数
    def __or__(self, dst):
        # 把两个标记符对象合并到一起
        def _或合并(s1,s2):
            if type(s2)==OrSymbol:
                s1.symbolList.extend(s2.symbolList)
            else:
                s1.symbolList.append(s2)
        newSymbol = OrSymbol()
        _或合并(newSymbol,self)
        _或合并(newSymbol,dst)
        return newSymbol


def MultiMatch(li: list, isFullMatch: bool, symbol: Symbol = None, startIndex: int = None, length: int = None) -> ParseResults:
    if len(li) <= 0: return (False,None)
    lastSuccess = False
    lastResult = []
    for item in li:
        if symbol get_ipython().getoutput("= None:")
            # 表示多结果匹配
            res = symbol.Match(item[0], item[1], isFullMatch)
        else:
            # 表示多符号匹配
            res = item.Match(startIndex, length, isFullMatch)
        # 如果匹配失败，则继续
        if res[0]==False: continue
        # 如果匹配成功
        lastSuccess = True
        # 合并每个匹配结果
        lastResult.extend(res[1])
    # 匹配结果去重
    lastResult = list(set(lastResult))
    # 返回最终结果
    return (lastSuccess,lastResult)


class Terminal(Symbol):pass


class MultiSymbol(Symbol):
    def __init__(self):
        super().__init__()
        # 管理符号对象列表，这些符号对象的关系依赖于对象的类型
        self.symbolList: List[Symbol] = []


class OrSymbol(MultiSymbol):
    '''复合标记符对象列表中的标记符之间是或的关系，可以采用多匹配函数进行匹配'''
    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        return MultiMatch(self.symbolList, isFullMatch, startIndex=startIndex, length=length)


class AndSymbol(MultiSymbol):
    '''复合标记符对象列表中的标记符之间是与的关系，可以采用多匹配函数进行匹配'''
    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        if len(self.symbolList) <= 1: return (False,None)
        # 上一个处理结果，先进行初始化
        preResult = [(startIndex,length)]
        # 先处理前面的，最后一个单独处理
        for symbol in self.symbolList[:-1]:
            res = MultiMatch(preResult,False,symbol)
            if res[0]==False: return (False,None)
            preResult = res[1]
        # 再处理最后一个
        return MultiMatch(preResult,isFullMatch,self.symbolList[-1])


class NonTerminal(OrSymbol): 
    def __iadd__(self,dst):
        self.symbolList.append(dst)
        return self


class Starter(NonTerminal):
    def Run(self, txt: str) -> int:
        '''
        txt：要匹配的文本
        返回匹配成功的次数，如果为0，表示没有匹配成功，如果大于1，表示有多个成功的匹配
        '''
        IMatch.Text = txt
        res = self.Match(0,len(IMatch.Text),True)
        return res[0]


class A(Terminal):
    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        if length <= 0: return (False,None)
        
        # 如果严格匹配，只能匹配单字符
        if isFullMatch==True and length > 1: return (False,None)
        
        if IMatch.Text[startIndex] get_ipython().getoutput("= 'a': return (False,None)")
        return (True,[(startIndex+1,length-1)])


def Run():
    s=Starter()
    a = A()
    s += a | a&a
    res = s.Run('aa')
    assert(res==True)


Run()



