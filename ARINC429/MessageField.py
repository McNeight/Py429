'''
Created on 2 mai 2013

@author: nulysse
'''

import Exception


class Field(object):
    '''
    This classes represents a an A429 message field.
    As such it is characterized by the position and size of the field, indicated by:
        - Field LSB (note that the LSB is indexed 1, to match common data dictionaries definitions)
        - Field Size in bits
        - Name is a human readable name used for various purposes, including error reporting
    This class also offers method to pack (in that case, simply take a value and store it at the appropriate place
    with a 32 bit value) and unpack
        
    '''

    def __repr__(self):
        return '<%s.%s object at 0x%x, Field \'%s\' at bit %x of size %x>'%(self.__module__,self.__class__.__name__,id(self),self.name,self.lsb,self.size)
      
    def __init__(self,lsb,size,name):
        '''
        Constructor
        '''
        self.lsb = lsb
        
        if lsb<1:
            raise Exception.A429MsgStructureError("LSB cannot be lower than 1")
            
        self.size = size
        
        if (lsb+size)>33:
            raise Exception.A429MsgStructureError("Field cannot exceed bit 32")
        
        self.name = name
        self._mask=((2**self.size)-1)<<(self.lsb-1)
        
    def getFootPrint(self):
        '''
        Return a word with bits at 1 in the space occupied by the field
        '''
        return self._mask
        
    def unpack(self,A429word):
        """ return the value given a 32 bit ARINC 429 message value """ 
        
        if (A429word<0):
            raise Exception.A429MsgRangeError(self.name,\
                                                  0,\
                                                  A429word)
        elif (A429word>0xFFFFFFFF): 
            raise Exception.A429MsgRangeError(self.name,\
                                                  0xFFFFFFFF,\
                                                  A429word)
        else:
            return ((A429word& self._mask)>>(self.lsb-1))                                                                     
        
    def pack(self,value):
        """
        Take an integer value and return a bit array representing
        the value packed at location corresponding to the message definition
        
        Warning: a A429MsgRangeError is raised if the field is not
        large enough to store the value.
        """
        if(abs(value)>((2**self.size)-1)):
            raise Exception.A429MsgRangeError(self.name,\
                                                  ((2**self.size)-1),\
                                                  value)
        elif value<0:
            raise Exception.A429MsgRangeError(self.name,\
                                                  0,\
                                                  value)
        else:
            return value<<(self.lsb-1)

    def __eq__(self, other):
        '''
        Define the == operator to compare size, lsb and name
        '''
        if isinstance(other, Field):
            return self.lsb == other.lsb and self.size == other.size and other.name == self.name
        else:
            return NotImplemented

    def __ne__(self, other):
        '''
        Define the != operator to compare size, lsb and name
        '''
        result = self.__eq__(other)
        '''
        Define the != operator to compare size, lsb and name
        '''
        if result is NotImplemented:
            return result
        return not result

    def serialize(self, stream, serializeState = False , parentElement = None):
        '''
        Serialize Message to XML
        '''

        from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree

        if parentElement is None:
            fieldElement = Element('Field')
        else:
            fieldElement = SubElement(parentElement, 'Field')

        fieldElement.set('name',self.name)
        fieldElement.set('lsb',str(self.lsb))
        fieldElement.set('size',str(self.size))

        return fieldElement
