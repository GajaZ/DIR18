# coding=utf-8


class UdpPacket():
    """
    UdpPacket
    Abstract class represent packet structure used in communication protocol between dx server and
    client application
    """
    def __init__(self, procDiv=1):
        """
        constructor method
        :return:            None
        """
        self.identifier = 'YERC'        #Identifier         4 Byte      (fixed to YERC)
        self.headSize = [0x20, 0x00]    #Header part size   2 Byte      Size of header part (fixed to 0x20)
        self.dataSize = [0x00, 0x00]    #Data part size     2 Byte      Size of data part (variable)
        self.reserve1 = 3               #Reserve 1          1 Byte      Fixed to “3”
        self.procDiv = procDiv          #Processing div     1 Byte      1: robot control, 2: file control
        self.ACK = 0                    #ACK                1 Byte      0: Request, 1: Other than request
        self.reqID = 0                  #Request ID         1 Byte      Identifying ID for command session
                                                                        # (increment this ID every time the client side outputs a
                                                                        # command. In reply to this, server side answers the received
                                                                        # value.)
        self.blockNo = [0, 0, 0, 0]     #Block No.          4 Byte      Request: 0
                                                                        # Answer: add 0x8000_0000 to the last packet.
                                                                        # Data transmission other than above: add 1
                                                                        # (max: 0x7fff_ffff)
        self.reserve2 = '99999999'      #Reserve 2          8 Byte      Fixed to “99999999”

class UdpPacket_Req(UdpPacket):
    def __init__(self, subHeader, data=[], procDiv=1):
        """
        constructor method
        :param subHeader:   sub header part of packet ( depend on each request/answer )
        :param data:        data part of the packet ( optional, depend of the request/answer )
        :return:            None
        """
        UdpPacket.__init__(self)

        self.cmdNo = subHeader['cmdNo']
        self.inst = subHeader['inst']
        self.attr = subHeader['attr']
        self.service = subHeader['service']
        self.padding = subHeader['padding']

        self.dataSize[0]=len(data)
        self.data=data
    def __str__(self):
        """
        :return: string representation of the packet
        """
        #Prepare request packet
        l_str = (self.identifier +                  # Identifier 4 Byte Fixed to “YERC”
                chr( self.headSize[0] ) +           #Header part size 2Byte Size of header part (fixed to 0x20)
                chr( self.headSize[1] ) +
                chr( self.dataSize[0] ) +           #Data part size 2Byte Size of data part (variable)
                chr( self.dataSize[1] ) +
                chr( self.reserve1 ) +              #Reserve 1 1Byte Fixed to “3”
                chr( self.procDiv ) +               #Processing division 1Byte 1: robot control, 2: file control
                chr( self.ACK ) +
                                #ACK 1Byte 0: Reques 1: Other than request
                chr( self.reqID ) +                 #Request ID 1Byte Identifying ID for command session
                                                            #(increment this ID every time the client side outputs a
                                                            #command. In reply to this, server side answers the received
                                                            #value.)
                chr( self.blockNo[0]) +             #Block No. 4Byte Request: 0
                chr( self.blockNo[1]) +                  # Answer: add 0x8000_0000 to the last packet.
                chr( self.blockNo[2]) +                  # Data transmission other than above: add 1
                chr( self.blockNo[3]) +                  # (max: 0x7fff_ffff)
                self.reserve2  +                    #Reserve 2          8 Byte       Fixed to “99999999”

                chr( self.cmdNo[0] ) +
                chr( self.cmdNo[1] ) +
                chr( self.inst[0] ) +
                chr( self.inst[1] ) +
                chr( self.attr ) +
                chr( self.service ) +
                chr( self.padding[0] ) +
                chr( self.padding[1] )
            )


        if (isinstance(self.data, str)):
            #data is string
            l_str = (l_str + self.data)
        else:
            for i in range(self.dataSize[0]):
                l_str = (l_str +
                    chr(self.data[i]) )



        return (l_str)

class UdpPacket_Ans(UdpPacket):
     def __init__(self, ans_str, l_procDiv):

        UdpPacket.__init__(self, l_procDiv)

        self.identifier = ans_str[0:4]
        self.headSize[0] = ord(ans_str[4])
        self.headSize[1] = ord(ans_str[5])
        self.dataSize[0] = ord(ans_str[6])
        self.dataSize[1] = ord(ans_str[7])
        self.reserve1 = ord(ans_str[8])
        self.procDiv = ord(ans_str[9])
        self.ACK = ord(ans_str[10])
        self.reqID = ord(ans_str[11])
        self.blockNo[0] = ord(ans_str[12])
        self.blockNo[1] = ord(ans_str[13])
        self.blockNo[2] = ord(ans_str[14])
        self.blockNo[3] = ord(ans_str[15])
        self.reserve2 = ans_str[16:24]

        self.service = ord(ans_str[24])
        self.status = ord(ans_str[25])
        self.add_status_size = ord(ans_str[26])
        self.padding1 = ord(ans_str[27])
        self.add_status=[0,0]
        self.add_status[0] = ord(ans_str[28])
        self.add_status[1] = ord(ans_str[29])
        self.padding2=[0,0]
        self.padding2[0] = ord(ans_str[30])
        self.padding2[1] = ord(ans_str[31])


        size = 4 * self.dataSize[1] * 256 + self.dataSize[0]
        self.data = [0] * size
        for i in range(size):
            self.data[i] = ord(ans_str[32 + i])