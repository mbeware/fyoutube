import json

tests = {
    "single array":'{"main":["a","b"]}',
    "single entity":'{"person":{"name":"toto","age":"30"}}',
    "multiple unqualified entities":'{"persons":[{"name":"toto", "age":"30"}, {"name":"toutoune", "age":"24"}]}',
    "multiple qualified entities":'{"persons":[{"person":{"name":"toto", "sex":"M"}}, {"person":{"name":"toutoune", "sex":"F"}}]}',
    "single array as top":'["first", "second"]',
}

class DotDict(dict):
    def __init__(self, *args, **kwargs):
        
        if type(args[0]) is list:
            largs=[]
            largs.append(*args)
            d=dict(zip(largs[0],largs[0]))
            largs[0]=d.copy()
            super().__init__(*largs, **kwargs)
        else:
            super().__init__(*args, **kwargs)
        for thekey, thevalue in self.items():
            if isinstance(thevalue, dict):
                self[thekey] = DotDict(thevalue)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        self[key] = value

    def to_dict(self):
        result = {}
        for thekey, thevalue in self.items():
            if isinstance(thevalue, DotDict):
                result[thekey] = thevalue.to_dict()
            else:
                result[thekey] = thevalue
        return result



    def _getPart(self,allkeylevels):
        # split with dots.
        # for each part, 
        # check if []
        
        token = allkeylevels[0]
        keyname = token
        keyindex = None
        if '[' in token: 
            subtokens=token.partition("[") # token[index]-> token,'[,index]  
            keyindex=subtokens[2].partition("]")[0] # index] -> index,],None
            keyname = subtokens[0]
        
        k = allkeylevels[1:]
        return keyname,keyindex,k



    def getValueFQN( self, key, default=None ):
        
        k=key.split('.')
        v=dict(self.items())
        r=None
        while k:
            keyname,keyindex,k = self._getPart(k)
            if keyindex:
                if keyindex == '#':
                    r=len(v[keyname])
                    k=[]
                elif keyname == 'Top':
                    r=list(v.values())[int(keyindex)]
                    k=None
                else:
                    v=v[keyname][int(keyindex)]
            else:
                v=v[keyname]
        if r : 
            return r
        return v



class JsonFlattener:
    def __init__( self, txt, defaultTopTopic="Top", sep='.', zeroedArrays=False ):
        self._DefaultTopTopic = defaultTopTopic
        self._ZeroedArrays    = zeroedArrays
        self._TopicSep        = sep
        self._Entries         = dict()
        self._flattenFromTop( txt )

    def getEntries( self ):
        return self._Entries

    def getEntriesCount( self ):
        return len( self._Entries )

    def listEntries( self ):
        for k in self._Entries:
            yield (k, self._Entries[ k ] )

    def getValue( self, key, default=None ):
        return self._Entries.get(key, default )

    def _addEntry( self, k, v ):
        # print( "+", k, ":=", v )
        self._Entries[k] = v

    def _firstIndex( self ):
        if self._ZeroedArrays:
            return 0
        else:
            return 1

    def _genFQName( self, rootPath, subTopic, skipSep=False ):
        Parts = []
        if rootPath:
            Parts.append( rootPath )
        # else:
        #    Parts.append( self._DefaultTopTopic )
        if subTopic:
            Parts.append( subTopic )
        if skipSep:
            return "".join( Parts )
        else:
            return self._TopicSep.join( Parts )

    def _flattenFromTop( self, txt ):
        jobj = json.loads( txt )
        self._flatten( None, jobj )

    def _flatten( self, rootPath, jobj ):
        JRoot = jobj
        #print( "<entry.top>:", type(JRoot), JRoot )
        if type( JRoot ) == list:
            self.flattenList( rootPath, JRoot )
        elif type( JRoot ) == dict:
            self.flattenDict( rootPath, JRoot )
        else: # a leaf (value)
            FQName = self._genFQName( rootPath, None )
            # print( "leaf('",FQName, "')" )
            Val = jobj[0]
            self._addEntry( FQName, Val )

    def flattenList( self, rootPath, jobj ):
        ListSize = len( jobj )
        if rootPath is None:
            rootPath = self._DefaultTopTopic
        FQNSize  = self._genFQName( rootPath, "[#]", skipSep=True )
        self._addEntry( FQNSize, ListSize )

        Index = self._firstIndex()

        for item in jobj:
            # print( "List[{}]: {} {}".format( Index, type(item), item ) )
            FQName = self._genFQName( rootPath, "[{}]".format( Index ), skipSep=True )
            if type( item ) == list:
                self.flattenList( FQName, item )
            elif type( item ) == dict:
                self.flattenDict( FQName, item )
            else: # a leaf (value)
                self._addEntry( FQName, item )
            Index += 1

    def flattenDict( self, rootPath, jobj ):
        Index = self._firstIndex()
        for k in jobj:
            sub = jobj[ k ]
            # print( "Dict[{}].{}: {} {}".format( Index, k, type(sub), sub ) )

            FQName = self._genFQName( rootPath, k )

            if type( sub ) == list:
                self.flattenList( FQName, sub )
            elif type( sub ) == dict:
                self.flattenDict( FQName, sub )
            else: # a leaf (value)
                self._addEntry( FQName, sub )
            Index += 1




s=tests["multiple qualified entities"]

F = JsonFlattener( s )
biga = {}
for k,v in F.listEntries():
    k=k.replace('#','૪')
    k=k.replace('[','𐴱')
    k=k.replace(']','𐴱')
    k=k.replace('.','·')
    biga[k]=v

d = DotDict(biga)


print(f"{d.persons𐴱1𐴱·person·name}={F.getValue('persons[1].person.name')}")
print(f"{d.persons𐴱2𐴱·person·name}={F.getValue('persons[1].person.name')}")
print(f"{d.persons𐴱૪𐴱}={F.getValue('persons[#]')}")
print(f"{F.getValue('persons[2]')}")
     
      
print(f'{d=}')
print(f'{F._Entries=}')


tests = {

    "single array":'{"main":["a","b"]}',
    "single entity":'{"person":{"name":"toto","age":"30"}}',
    "multiple unqualified entities":'{"persons":[{"name":"toto", "age":"30"}, {"name":"toutoune", "age":"24"}]}',
    "multiple qualified entities":'{"persons":[{"person":{"name":"toto", "sex":"M"}}, {"person":{"name":"toutoune", "sex":"F"}}]}',
    "single array as top":'["first", "second"]',
    "special character":'{"persons":[{"person":{"name":"t[oto", "sex":"M]"}}, {"person":{"name":"tou.toune", "sex":"#F"}}]}',
}

t="single array"

print(t)
s=tests[t]

ff = json.loads(s)
print(f"{ff=}")

d2 = DotDict(ff)

print(f"{d2.getValueFQN('main')=}")
print(f"{d2.getValueFQN('main[0]')=}")
print(f"{d2.getValueFQN('main[1]')=}")


t="single entity"

print(t)
s=tests[t]

ff = json.loads(s)
print(f"{ff=}")

d2 = DotDict(ff)

print(f"{d2.getValueFQN('person')=}")
print(f"{d2.getValueFQN('person.name')=}")
print(f"{d2.getValueFQN('person.age')=}")


t="multiple unqualified entities"
print(t)
s=tests[t]
ff = json.loads(s)
print(f"{ff=}")

d2 = DotDict(ff)

print(f"{d2.getValueFQN('persons')=}")
print(f"{d2.getValueFQN('persons[#]')=}")
print(f"{d2.getValueFQN('persons[0]')=}")
print(f"{d2.getValueFQN('persons[0].name')=}")
print(f"{d2.getValueFQN('persons[0].age')=}")
print(f"{d2.getValueFQN('persons[1]')=}")
print(f"{d2.getValueFQN('persons[1].name')=}")
print(f"{d2.getValueFQN('persons[1].age')=}")


t="multiple qualified entities"
print(t)
s=tests[t]


ff = json.loads(s)
print(f"{ff=}")

d2 = DotDict(ff)

print(f"{d2.getValueFQN('persons')=}")
print(f"{d2.getValueFQN('persons[0]')=}")
print(f"{d2.getValueFQN('persons[0].person')=}")
print(f"{d2.getValueFQN('persons[0].person.name')=}")
print(f"{d2.getValueFQN('persons[0].person.sex')=}")

print(f"{d2.getValueFQN('persons[1]')=}")
print(f"{d2.getValueFQN('persons[1].person')=}")
print(f"{d2.getValueFQN('persons[1].person.name')=}")
print(f"{d2.getValueFQN('persons[1].person.sex')=}")


t="single array as top"
print(t)
s=tests[t]
ff = json.loads(s)
print(f"{ff=}")

d2 = DotDict(ff)
print(f"{d2.getValueFQN('first')=}")
print(f"{d2.getValueFQN('second')=}")

print(f"{d2.getValueFQN('Top[0]')=}")
print(f"{d2.getValueFQN('Top[1]')=}")


t="special character"
print(t)
s=tests[t]


ff = json.loads(s)
print(f"{ff=}")

d2 = DotDict(ff)

print(f"{d2.getValueFQN('persons')=}")
print(f"{d2.getValueFQN('persons[0]')=}")
print(f"{d2.getValueFQN('persons[0].person')=}")
print(f"{d2.getValueFQN('persons[0].person.name')=}")
print(f"{d2.getValueFQN('persons[0].person.sex')=}")

print(f"{d2.getValueFQN('persons[1]')=}")
print(f"{d2.getValueFQN('persons[1].person')=}")
print(f"{d2.getValueFQN('persons[1].person.name')=}")
print(f"{d2.getValueFQN('persons[1].person.sex')=}")


 


