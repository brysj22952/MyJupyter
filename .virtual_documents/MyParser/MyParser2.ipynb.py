def ����̳й�ϵ():
    from graphviz import Digraph
    dot = Digraph()
    # �ڵ�����
    dot.node('IMatch',xlabel='������Match����')
    dot.node('Symbol',xlabel='��Ƿ�')
    dot.node('Terminal',xlabel='�ս��')
    dot.node('MultiSymbol',xlabel='���ϱ�Ƿ�������һ�������б�')
    dot.node('AndSymbol',xlabel='�븴�ϱ�Ƿ�')
    dot.node('OrSymbol',xlabel='�򸴺ϱ�Ƿ�')
    dot.node('NonTerminal',xlabel='���ս��,����һ�������ɳ�֮Ϊ����ı�Ƿ�')
    dot.node('Starter',xlabel='��ʼ��')
    # �̳й�ϵ����
    dot.edge('IMatch','Symbol')
    dot.edge('Symbol','Terminal')
    dot.edge('Symbol','MultiSymbol')
    dot.edge('MultiSymbol','AndSymbol')
    dot.edge('MultiSymbol','OrSymbol')
    dot.edge('OrSymbol','NonTerminal')
    dot.edge('NonTerminal','Starter')
    # ��ʾͼ��
    dot

#����̳й�ϵ()


from printobject import pp
from types import MethodType 


from typing import List, Tuple

# ƥ��֮��ʣ��Ĵ�ƥ��Ľ����������������(True,[(2,3),(5,6)])����һ���ʾ�Ƿ�ƥ��ɹ�����2���ʾƥ��Ľ���������ж����ƥ����
# ÿһ��ƥ�����һ���ʾ��ʼ��������2���ʾ����
ParseResults = Tuple[bool,List[Tuple[int,int]]]


class IMatch:
    # ��ʾ��������ԭʼ�ַ���
    Text :str = None

    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        '''
        �����������Դ��������ַ�������ƥ�䣬����ƥ��Ľ��
        startIndex����ƥ���ַ�������ʼ����
        length����ƥ���ַ����ĳ���
        isFullMatch����ʾ�Ƿ���Ҫ��ȫƥ�䣬�����ȫƥ�䣬������ַ���ƥ���꣬�ŷ��سɹ���ֻƥ�䲿�֣���ƥ��ʧ��
        ����ֵ��ParseResults���ͣ������ж��ʣ��Ĵ�ƥ����
        '''
        pass
    pass


class Symbol(IMatch): 
    # ����&����
    def __and__(self, dst):
        # ��������Ƿ�����ϲ���һ��
        def _��ϲ�(s1,s2):
            if type(s2)==AndSymbol:
                s1.symbolList.extend(s2.symbolList)
            else:
                s1.symbolList.append(s2)
        newSymbol = AndSymbol()
        _��ϲ�(newSymbol,self)
        _��ϲ�(newSymbol,dst)
        return newSymbol
    
    # ����|����
    def __or__(self, dst):
        # ��������Ƿ�����ϲ���һ��
        def _��ϲ�(s1,s2):
            if type(s2)==OrSymbol:
                s1.symbolList.extend(s2.symbolList)
            else:
                s1.symbolList.append(s2)
        newSymbol = OrSymbol()
        _��ϲ�(newSymbol,self)
        _��ϲ�(newSymbol,dst)
        return newSymbol


def MultiMatch(li: list, isFullMatch: bool, symbol: Symbol = None, startIndex: int = None, length: int = None) -> ParseResults:
    if len(li) <= 0: return (False,None)
    lastSuccess = False
    lastResult = []
    for item in li:
        if symbol get_ipython().getoutput("= None:")
            # ��ʾ����ƥ��
            res = symbol.Match(item[0], item[1], isFullMatch)
        else:
            # ��ʾ�����ƥ��
            res = item.Match(startIndex, length, isFullMatch)
        # ���ƥ��ʧ�ܣ������
        if res[0]==False: continue
        # ���ƥ��ɹ�
        lastSuccess = True
        # �ϲ�ÿ��ƥ����
        lastResult.extend(res[1])
    # ƥ����ȥ��
    lastResult = list(set(lastResult))
    # �������ս��
    return (lastSuccess,lastResult)


class Terminal(Symbol):pass


class MultiSymbol(Symbol):
    def __init__(self):
        super().__init__()
        # ������Ŷ����б���Щ���Ŷ���Ĺ�ϵ�����ڶ��������
        self.symbolList: List[Symbol] = []


class OrSymbol(MultiSymbol):
    '''���ϱ�Ƿ������б��еı�Ƿ�֮���ǻ�Ĺ�ϵ�����Բ��ö�ƥ�亯������ƥ��'''
    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        return MultiMatch(self.symbolList, isFullMatch, startIndex=startIndex, length=length)


class AndSymbol(MultiSymbol):
    '''���ϱ�Ƿ������б��еı�Ƿ�֮������Ĺ�ϵ�����Բ��ö�ƥ�亯������ƥ��'''
    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        if len(self.symbolList) <= 1: return (False,None)
        # ��һ�����������Ƚ��г�ʼ��
        preResult = [(startIndex,length)]
        # �ȴ���ǰ��ģ����һ����������
        for symbol in self.symbolList[:-1]:
            res = MultiMatch(preResult,False,symbol)
            if res[0]==False: return (False,None)
            preResult = res[1]
        # �ٴ������һ��
        return MultiMatch(preResult,isFullMatch,self.symbolList[-1])


class NonTerminal(OrSymbol): 
    def __iadd__(self,dst):
        self.symbolList.append(dst)
        return self


class Starter(NonTerminal):
    def Run(self, txt: str) -> int:
        '''
        txt��Ҫƥ����ı�
        ����ƥ��ɹ��Ĵ��������Ϊ0����ʾû��ƥ��ɹ����������1����ʾ�ж���ɹ���ƥ��
        '''
        IMatch.Text = txt
        res = self.Match(0,len(IMatch.Text),True)
        return res[0]


class A(Terminal):
    def Match(self, startIndex: int, length: int, isFullMatch: bool) -> ParseResults:
        if length <= 0: return (False,None)
        
        # ����ϸ�ƥ�䣬ֻ��ƥ�䵥�ַ�
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



