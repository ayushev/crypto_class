import urllib2
import sys

ct      =     ['f20bdba6ff29eed7b046d1df9fb70000',
               '58b1ffb4210a580f748b4ac714c001bd',
               '4a61044426fb515dad3f21f18aa577c0',
               'bdf302936266926ff37dbf7035d5eeb4']

iv      =     ct[0]
#m0      =     '546865204d6167696320576f72647320'
ct_0    =     ct[1]
#m1      =     '6172652053717565616d697368204f73'
ct_1    =     ct[2]
#m2      =     '73696672616765090909090909090909'
ct_2    =     ct[3]
TARGET =      'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        #q = ''.join('{:02x}'.format(q))
        target = TARGET + urllib2.quote(q)    # Create query URL
        #print target
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            #print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

    def make_pad(self, hex_pad_byte):
        str_obpad = "{:02x}".format(hex_obpad);
        i = 0
        padding = ''
        while (i < hex_obpad):
            padding = padding + str_obpad
            i = i + 1
        return padding
        
    
    
if __name__ == "__main__":
#   print m0.decode("hex") + m1.decode("hex") + m2.decode("hex")
    po = PaddingOracle()
    block_i = 0
    blocks  = ''
    pt      = ''
    pt_i    = ''
    for block_i in range(3):
        blocks += ct[block_i]
        pt_i    = ''
        for hex_obpad in range(1,17):
            padding =  po.make_pad(hex_obpad)
            hex_guess = 0x00
            for hex_guess in range(0xff):
                pt_i_guess = ''.join('{:02x}'.format(hex_guess)) + pt_i
                compl_guess = int(pt + pt_i_guess,16) ^ int(padding,16)
                new_query = int(blocks ,16) ^ compl_guess
                hex_chq = ''.join('{:02x}'.format(new_query))
                new_query = hex_chq + ct[block_i + 1]
                if po.query(new_query) == True:
                    pt_i = pt_i_guess
                    print pt_i.decode("hex")
                    break
        pt      = pt + pt_i
        print "Cuurently discovered plaintext = \"{0}\"".format(pt.decode("hex"))
    print "Plain text discovered = \"{0}\"".format(pt.decode("hex"))
