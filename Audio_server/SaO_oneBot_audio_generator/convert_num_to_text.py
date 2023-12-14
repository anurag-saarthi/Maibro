import re
import time
import datetime
class SymbolParser(object):
    def readNumber(self, number,language):
        numLiterals = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
                6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine'}
        numHindi = {0:' ',1:'एक',2:'दो',3:'तीन',4:'चार',5:'पांच',  #0:'शून्य'
                        6:'छह',7:'सात',8:'आठ',9:'नौ',10:'दस',11:'ग्यारह',12:'बारह',13:'तेरह',
                        14:'चोदह',15:'पंद्रह',16:'सोलह',17:'सत्त्रह',18:'अट्ठारह',19:'उन्नीस',20:'बीस',
                        21:'इक्कीस',22:'बाइस',23:'तेईस',24:'चौबीस',25:'पच्चीस',26:'छब्बीस',27:'सत्ताइस',
                        28:'अट्ठाइस',29:'उन्तीस',30:'तीस',31:'इकतीस',32:'बत्तीस',33:'तैतीस',34:'चौतीस',
                        35:'पैतीस',36:'छत्तीस',37:'सैतीस',38:'अड़तीस',39:'उन्तालीस',40:'चालीस',41:'इकतालीस',
                        42:'बयालीस',43:'तिरतालिस',44:'चौवालीस',45:'पैतालीस',46:'छयालीस',47:'सैतालिस',
                        48:'अड़तालीस',49:'उनचास',50:'पचास',51:'इक्क्यावन',52:'बावन',53:'तिरपन',54:'चौवन',
                        55:'पचपन',56:'छप्पन',57:'सत्तावन',58:'अट्ठावन',59:'उनसठ',60:'साठ',61:'इकसठ',62:'बासठ',
                        63:'तिरसठ',64:'चौसठ',65:'पैंसठ',66:'छयासठ',67:'सड़सठ',68:'अड़सठ',69:'उनहत्तर',70:'सत्तर',
                        71:'इकहत्तर',72:'बहत्तर',73:'तिरहत्तर',74:'चौहत्तर',75:'पिचहत्तर',76:'छियत्तर',77:'सतत्तर',
                        78:'अठहत्तर',79:'उन्हासी',80:'अस्सी',81:'इक्यासी',82:'बयासी',83:'तिरासी',84:'चौरासी',
                        85:'पिचासी',86:'छयासी',87:'सत्तासी',88:'अट्ठासी',89:'नवासी',90:'नब्बे',91:'इक्यानवे',
                        92:'बानवे',93:'तिरानवे',94:'चौरानवे',95:'पिच्यानवे',96:'छियानवे',97:'सत्तानवे',98:'अट्ठानवे',
                        99:'निन्यानवे',100:'सौ'}
        numEnglish = { 0 : ' ', 1 : ' one', 2 : ' two', 3 : ' three', 4 : ' four',  #0 : ' zero',
                    5 : ' five',6 : ' six', 7 : ' seven', 8 : ' eight', 9 : ' nine', 
                    10 : ' ten',11 : ' eleven', 12 : ' twelve', 13 : ' thirteen', 14 : ' fourteen',
                    15 : ' fifteen', 16 : ' sixteen', 17 : ' seventeen', 18 : ' eighteen',19 : ' nineteen', 
                    20 : ' twenty',21: ' twenty one', 22: ' twenty two', 23: ' twenty three', 24: ' twenty four', 25: ' twenty five', 
                    26: ' twenty six', 27: ' twenty seven', 28: ' twenty eight', 29: ' twenty nine', 30: ' thirty', 
                    31: ' thirty one', 32: ' thirty two', 33: ' thirty three', 34: ' thirty four', 35: ' thirty five', 
                    36: ' thirty six', 37: ' thirty seven', 38: ' thirty eight', 39: ' thirty nine', 40: ' forty', 
                    41: ' forty one', 42: ' forty two', 43: ' forty three', 44: ' forty four', 45: ' forty five', 
                    46: ' forty six', 47: ' forty seven', 48: ' forty eight', 49: ' forty nine', 50: ' fifty', 51: ' fifty one', 
                    52: ' fifty two', 53: ' fifty three', 54: ' fifty four', 55: ' fifty five', 56: ' fifty six', 57: ' fifty seven', 
                    58: ' fifty eight', 59: ' fifty nine', 60: ' sixty', 61: ' sixty one', 62: ' sixty two', 63: ' sixty three', 
                    64: ' sixty four', 65: ' sixty five', 66: ' sixty six', 67: ' sixty seven', 68: ' sixty eight', 69: ' sixty nine', 
                    70: ' seventy', 71: ' seventy one', 72: ' seventy two', 73: ' seventy three', 74: ' seventy four', 
                    75: ' seventy five', 76: ' seventy six', 77: ' seventy seven', 78: ' seventy eight', 79: ' seventy nine', 
                    80: ' eighty', 81: ' eighty one', 82: ' eighty two', 83: ' eighty three', 84: ' eighty four', 85: ' eighty five', 
                    86: ' eighty six', 87: ' eighty seven', 88: ' eighty eight', 89: ' eighty nine', 90: ' ninety', 91: ' ninety one', 
                    92: ' ninety two', 93: ' ninety three', 94: ' ninety four', 95: ' ninety five', 96: ' ninety six', 97: ' ninety seven', 
                    98: ' ninety eight',99:" ninety nine",100:' hundred' }
        numOdia={0:' ',1:'ଏକ',2:'ଦୁଇ',3:'ତିନି',4:'ଚାରି',5:'ପାଞ୍ଚ',  #0:'ଶୁନ୍ୟ'
                6:'ଛଅ',7:'ସାତ',8:'ଆଠ',9:'ନଅ',10:'ଦଶ',11:'ଏଗାର',12:'ବାର',13:'ତେର',
                14:'ଚଉଦ',15:'ପନ୍ଦର',16:'ଷୋହଳ',17:'ସତର',18:'ଅଠର',19:'ଉଣେଇଶ',20:'କୋଡ଼ିଏ',
                21:'ଏକୋଇଶ',22:'ବାଇଶ',23:'ତେଇଶ',24:'ଚବିଶ',25:'ପଚିଶ',26:'ଛବିଶ',27:'ସତେଇଶ',
                28:'ଅଠେଇଶ',29:'ଅଣତିରିଶ',30:'ତିରିଶ',31:'ଏକତିରିଶ',32:'ବତିଶ',33:'ତେତିଶ',34:'ଚଉତରିଶ',
                35:'ପଇଁତିରିଶ',36:'ଛତିଶ',37:'ସଇଁତିରିଶ',38:'ଅଠତିରିଶ',39:'ଅଣଚାଳିଶ',40:'ଚାଳିଶ',41:'ଏକଚାଳିଶ',
                42:'ବୟାଳିଶ',43:'ତେୟାଳିଶ',44:'ଚଉରାଳିଶ',45:'ପଇଁଚାଳିଶ',46:'ଛୟାଳିଶ',47:'ସତଚାଳିଶ',
                48:'ଅଠଚାଳିଶ',49:'ଅଣଚାଶ',50:'ପଚାଶ',51:'ଏକାବନ',52:'ବାବନ',53:'ତେପନ',54:'ଚଉବନ',
                55:'ପଞ୍ଚାବନ',56:'ଛପନ',57:'ସତାବନ',58:'ଅଠାବନ',59:'ଅଣଷଠି',60:'ଷାଠିଏ',61:'ଏକଷଠି',62:'ବାଷଠି',
                63:'ତେଷଠି',64:'ଚଉଷଠି',65:'ପଞ୍ଚଷଠି',66:'ଛଷଠି',67:'ଶତଷଠି',68:'ଅଠଷଠି',69:'ଅଣସ୍ତରି',70:'ସତୁରୀ',
                71:'ଏକସ୍ତରୀ',72:'ବାସ୍ତରୀ',73:'ତେସ୍ତରୀ',74:'ଚଉସ୍ତରୀ',75:'ପଞ୍ଚସ୍ତରୀ',76:'ଛସ୍ତରୀ',77:'ସତସ୍ତରୀ',
                78:'ଅଠସ୍ତରୀ',79:'ଅଣାଅଶୀ',80:'ଅଶୀ',81:'ଏକାଅଶୀ',82:'ବୟାଅଶୀ',83:'ତେୟାଅଶୀ',84:'ଚଉରାଅଶୀ',
                85:'ପଞ୍ଚାଅଶୀ',86:'ଛୟାଅଶୀ',87:'ସତାଅଶୀ',88:'ଅଠାଅଶୀ',89:'ଅଣାନବେ',90:'ନବେ',91:'ଏକାନବେ',
                92:'ବୟାନବେ',93:'ତେୟାନବେ',94:'ଚଉରାନବେ',95:'ପଞ୍ଚାନବେ',96:'ଛୟାନବେ',97:'ସତନାବେ',98:'ଅଠାନବେ',
                99:'ଅନେଶ୍ୱତ',100:'ଶହେ'}
        numMalayalam={0:' ',1:'ഒന്ന്',2:'രണ്ട്',3:'മൂന്ന്',4:'നാല്',5:'അഞ്ച്',6:'ആറ്',7:'ഏഴ്',    #0:'പുജ്യം',
                8:'എട്ട്',9:'ഒന്‍പത്',10:'പത്ത്',11:'പതിനൊന്ന്',12:'പന്ത്രണ്ട്',13:'പതിമൂന്ന്',14:'പതിനാല്',
                15:'പതിനഞ്ച്',16:'പതിനാറ്',17:'പതിനേഴ്',18:'പതിനെട്ട്',19:'പത്തൊന്‍പത്',20:'ഇരുപത്',
                21:'ഇരുപത്തിയൊന്ന്',22:'ഇരുപത്തിരണ്ട്',23:'ഇരുപത്തിമൂന്ന്',24:'ഇരുപത്തിനാല്',
                25:'ഇരുപത്തിയഞ്ച്',26:'ഇരുപത്തിയാറ്',27:'ഇരുപത്തിയേഴ്',28:'ഇരുപത്തിയെട്ട്',29:'ഇരുപത്തിയൊന്‍പത്',
                30:'മുപ്പത്',31:'മുപ്പത്തിയൊന്ന്',32:'മുപ്പത്തിരണ്ട്',33:'മുപ്പത്തിമൂന്ന്',34:'മുപ്പത്തിനാല്',35:'മുപ്പത്തിയഞ്ച്',
                36:'മുപ്പത്തിയാറ്',37:'മുപ്പത്തിയേഴ്',38:'മുപ്പത്തിയെട്ട്',39:'മുപ്പത്തിയൊന്‍പത്',40:'നാല്‍പത്',41:'നാല്‍പ്പത്തിയൊന്ന്',
                42:'നാല്‍പ്പത്തിരണ്ട്',43:'നാല്‍പ്പത്തിമൂന്ന്',44:'നാല്‍പ്പത്തിനാല്',45:'നാല്‍പ്പത്തിയഞ്ച്',46:'നാല്‍പ്പത്തി ആറ്',
                47:'നാല്‍പ്പത്തി ഏഴ്',48:'നാല്‍പ്പത്തി എട്ട്',49:'നാല്‍പ്പത്തി ഒന്‍പത്',50:'അമ്പത്',51:'അമ്പത്തി ഒന്ന്',
                52:' അമ്പത്തി രണ്ട്',53:'അമ്പത്തി മൂന്ന്',54:'അമ്പത്തി നാല്',55:' അമ്പത്തി അഞ്ച്',56:' അമ്പത്തി ആറ്',
                57:' അമ്പത്തി ഏഴ്',58:' അമ്പത്തി എട്ട്',59:'അമ്പത്തി ഒമ്പത്',60:'അറുപത്',61:'അറുപത്തി ഒന്ന്',
                62:'അറുപത്തി രണ്ട്',63:'അറുപത്തി മൂന്ന്',64:'അറുപത്തി നാല്',65:'അറുപത്തി അഞ്ച്',66:'അറുപത്തി ആറ്',
                67:'അറുപത്തി ഏഴ്',68:'അറുപത്തി എട്ട്',69:'അറുപത്തി ഒമ്പത്',70:'എഴുപത്',71:'എഴുപത്തി ഒന്ന്',
                72:'എഴുപത്തി രണ്ട്',73:'എഴുപത്തി മൂന്ന്',74:'എഴുപത്തി നാല്',75:'എഴുപത്തി അഞ്ച്',76:'എഴുപത്തി ആറ്',
                77:'എഴുപത്തി ഏഴ്',78:'എഴുപത്തി എട്ട്',79:'എഴുപത്തി ഒമ്പത്',80:'എണ്‍പത്',81:'എണ്‍പത്തി ഒന്ന്',
                82:'എണ്‍പത്തി രണ്ട്',83:'എണ്‍പത്തി മൂന്ന്',84:'എണ്‍പത്തി നാല്',85:'എണ്‍പത്തി അഞ്ച്',
                86:'എണ്‍പത്തി ആറ്',87:'എണ്‍പത്തി ഏഴ്',88:'എണ്‍പത്തി എട്ട്',89:'എണ്‍പത്തി ഒമ്പത്',
                90:'തൊണ്ണൂറ്',91:'തൊണ്ണൂറ്റി ഒന്ന്',92:'തൊണ്ണൂറ്റി രണ്ട്',93:'തൊണ്ണൂറ്റി മൂന്ന്',
                94:'തൊണ്ണൂറ്റി നാല്',95:'തൊണ്ണൂറ്റി അഞ്ച്',96:'തൊണ്ണൂറ്റി ആറ്',97:'തൊണ്ണൂറ്റി ഏഴ്',
                98:'തൊണ്ണൂറ്റി എട്ട്',99:'തൊണ്ണൂറ്റി ഒമ്പത്',100:'നൂറ്'}
        numGujarati={0:' ',1:'એક',2:'બે',3:'ત્રણ',4:'ચાર',5:'પાંચ',6:'છ',7:'સાત',8:'આઠ',9:'નવ',    #0:'શૂન્ય',
                10:'દસ',11:'અગિયાર',12:'બાર',13:'તેર',14:'ચૌદ',15:'પંદર',16:'સોળ',17:'સતર',18:'અઢાર',19:'ઓગણીસ',
                20:'વીસ',21:'એકવીસ',22:'બાવીસ',23:'તેવીસ',24:'ચોવીસ',25:'પચ્ચીસ',26:'છવીસ',27:'સત્તાવીસ',28:'અઠ્ઠાવીસ',
                29:'ઓગણત્રીસ',30:'ત્રીસ',31:'એકત્રીસ',32:'બત્રીસ',33:'તેત્રીસ',34:'ચોત્રીસ',35:'પાંત્રીસ',36:'છત્રીસ',37:'સડત્રીસ',
                38:'અડત્રીસ',39:'ઓગણચાલીસ',40:'ચાલીસ',41:'એકતાલીસ',42:'બેતાલીસ',43:'તેતાલીસ',44:'ચુંમાલીસ',45:'પિસ્તાલીસ',
                46:'છેતાલીસ',47:'સુડતાલીસ',48:'અડતાલીસ',49:'ઓગણપચાસ',50:'પચાસ',51:'એકાવન',52:'બાવન',53:'ત્રેપન',54:'ચોપન',
                55:'પંચાવન',56:'છપ્પન',57:'સત્તાવન',58:'અઠ્ઠાવન',59:'ઓગણસાઠ',60:'સાઈઠ',61:'એકસઠ',62:'બાસઠ',63:'ત્રેસઠ',64:'ચોસઠ',
                65:'પાંસઠ',66:'છાસઠ',67:'સડસઠ',68:'અડસઠ',69:'અગણોસિત્તેર',70:'સીત્તેર',71:'એકોતેર',72:'બોતેર',73:'તોતેર',74:'ચુમોતેર',
                75:'પંચોતેર',76:'છોતેર',77:'સીત્યોતેર',78:'ઇઠ્યોતેર',79:'ઓગણાએંસી',80:'એંસી',81:'એક્યાસી',82:'બ્યાસી',83:'ત્યાસી',
                84:'ચોર્યાસી',85:'પંચાસી',86:'છ્યાસી',87:'સિત્યાસી',88:'ઈઠ્યાસી',89:'નેવ્યાસી',90:'નેવું',91:'એકાણું',92:'બાણું',
                93:'ત્રાણું',94:'ચોરાણું',95:'પંચાણું',96:'છન્નું',97:'સત્તાણું',98:'અઠ્ઠાણું',99:'નવ્વાણું',100:'સો'}
        numBengali={0:' ',1:'এক',2:'দুই',3:'তিন',4:'চার',5:'পাঁচ',6:'ছয়',7:'সাত',8:'আট',9:'নয়',10:'দশ',11:'এগার',   #0:'শূন্য',
                12:'বার',13:'তের',14:'চৌদ্দ',15:'পনের',16:'ষোল',17:'সতের',18:'আঠার',19:'ঊনিশ',20:'বিশ',21:'একুশ',22:'বাইশ',
                23:'তেইশ',24:'চব্বিশ',25:'পঁচিশ',26:'ছাব্বিশ',27:'সাতাশ',28:'আঠাশ',29:'ঊনত্রিশ',30:'ত্রিশ',31:'একত্রিশ',32:'বত্রিশ',
                33:'তেত্রিশ',34:'চৌত্রিশ',35:'পঁয়ত্রিশ',36:'ছত্রিশ',37:'সাঁইত্রিশ',38:'আটত্রিশ',39:'ঊনচল্লিশ',40:'চল্লিশ',41:'একচল্লিশ',
                42:'বিয়াল্লিশ',43:'তেতাল্লিশ',44:'চুয়াল্লিশ',45:'পঁয়তাল্লিশ',46:'ছেচল্লিশ',47:'সাতচল্লিশ',48:'আটচল্লিশ',49:'ঊনপঞ্চাশ',
                50:'পঞ্চাশ',51:'একান্ন',52:'বায়ান্ন',53:'তিপ্পান্ন',54:'চুয়ান্ন',55:'পঞ্চান্ন',56:'ছাপ্পান্ন',57:'সাতান্ন',58:'আটান্ন',
                59:'ঊনষাট',60:'ষাট',61:'একষট্টি',62:'বাষট্টি',63:'তেষট্টি',64:'চৌষট্টি',65:'পঁয়ষট্টি',66:'ছেষট্টি',67:'সাতষট্টি',
                68:'আটষট্টি',69:'ঊনসত্তর',70:'সত্তর',71:'একাত্তর',72:'বাহাত্তর',73:'তিয়াত্তর',74:'চুয়াত্তর',75:'পঁচাত্তর',76:'ছিয়াত্তর',
                77:'সাতাত্তর',78:'আটাত্তর',79:'ঊনআশি',80:'আশি',81:'একাশি',82:'বিরাশি',83:'তিরাশি',84:'চুরাশি',85:'পঁচাশি',
                86:'ছিয়াশি',87:'সাতাশি',88:'আটাশি',89:'ঊননব্বই',90:'নব্বই',91:'একানব্বই',92:'বিরানব্বই',93:'তিরানব্বই',94:'চুরানব্বই',
                95:'পঁচানব্বই',96:'ছিয়ানব্বই',97:'সাতানব্বই',98:'আটানব্বই',99:'নিরানব্বই',100:'এক শো'}
        numTelugu={0:' ',1:'ఒకటి',2:'రెండు',3:'మూడు',4:'నాలుగు',5:'అయిదు',6:'ఆరు',7:'ఏడు',    #0:'సున్న',
                8:'ఎనిమిది',9:'తొమ్మిది',10:'పది',11:'పదకొండు',12:'పన్నెండు',13:'పదమూడు',14:'పధ్నాలుగు',
                15:'పదునయిదు',16:'పదహారు',17:'పదిహేడు',18:'పధ్ధెనిమిది',19:'పందొమ్మిది',20:'ఇరవై',
                21:'ఇరవై ఒకటి',22:'ఇరవై రెండు',23:'ఇరవై మూడు',24:'ఇరవై నాలుగు',25:'ఇరవై అయిదు',
                26:'ఇరవై ఆరు',27:'ఇరవై ఏడు',28:'ఇరవై ఎనిమిది',29:'ఇరవై తొమ్మిది',30:'ముప్పై',
                31:'ముప్పై ఒకటి',32:'ముప్పై రెండు',33:'ముప్పై మూడు',34:'ముప్పై నాలుగు',35:'ముప్పై ఐదు',
                36:'ముప్పై ఆరు',37:'ముప్పై ఏడు',38:'ముప్పై ఎనిమిది',39:'ముప్పై తొమ్మిది',40:'నలభై',
                41:'నలభై ఒకటి',42:'నలభై రెండు',43:'నలభై మూడు',44:'నలభై నాలుగు',45:'నలభై అయిదు',
                46:'నలభై ఆరు',47:'నలభై ఏడు',48:'నలభై ఎనిమిది',49:'నలభై తొమ్మిది',50:'యాభై',
                51:'యాభై ఒకటి',52:'యాభై రెండు',53:'యాభై మూడు',54:'యాభై నాలుగు',55:'యాభై అయిదు',
                56:'యాభై ఆరు',57:'యాభై ఏడు',58:'యాభై ఎనిమిది',59:'యాభై తొమ్మిది',60:'అరవై',
                61:'అరవై ఒకటి',62:'అరవై రెండు',63:'అరవై మూడు',64:'అరవై నాలుగు',65:'అరవై అయిదు',
                66:'అరవై ఆరు',67:'అరవై ఏడు',68:'అరవై ఎనిమిది',69:'అరవై తొమ్మిది',70:'డెబ్బై',
                71:'డెబ్బై ఒకటి',72:'డెబ్బై రెండు',73:'డెబ్బై మూడు',74:'డెబ్బై నాలుగు',75:'డెబ్బై అయిదు',
                76:'డెబ్బై ఆరు',77:'డెబ్బై ఏడు',78:'డెబ్బై ఎనిమిది',79:'డెబ్బై తొమ్మిది',80:'ఎనభై',
                81:'ఎనభై ఒకటి',82:'ఎనభై రెండు',83:'ఎనభై మూడు',84:'ఎనభై నాలుగు',85:'ఎనభై అయిదు',
                86:'ఎనభై ఆరు',87:'ఎనభై ఏడు',88:'ఎనభై ఎనిమిది',89:'ఎనభై తొమ్మిది',90:'తొంభై',
                91:'తొంభై ఒకటి',92:'తొంభై రెండు',93:'తొంభై మూడు',94:'తొంభై నాలుగు',95:'తొంభై అయిదు',
                96:'తొంభై ఆరు',97:'తొంభై ఏడు',98:'తొంభై ఎనిమిది',99:'తొంభై తొమ్మిది',100:'వంద'}
        numMarathi={0:' ',1:'एक',2:'दोन',3:'तीन',4:'चार',5:'पाच',6:'सहा',7:'सात',8:'आठ',9:'नऊ',10:'दहा',    #0:'शून्य',
                11:'अकरा',12:'बारा',13:'तेरा',14:'चौदा',15:'पंधरा',16:'सोळा',17:'सतरा',18:'अठरा',19:'एकोणीस',
                20:'वीस',21:'एकवीस',22:'बावीस',23:'तेवीस',24:'चोवीस',25:'पंचवीस',26:'सव्वीस',27:'सत्तावीस',
                28:'अठ्ठावीस',29:'एकोणतीस',30:'तीस',31:'एकतीस',32:'बत्तीस',33:'तेहेतीस',34:'चौतीस',
                35:'पस्तीस',36:'छत्तीस',37:'सदतीस',38:'अडतीस',39:'एकोणचाळीस',40:'चाळीस',41:'एक्केचाळीस',
                42:'बेचाळीस',43:'त्रेचाळीस',44:'चव्वेचाळीस',45:'पंचेचाळीस',46:'सेहेचाळीस',47:'सत्तेचाळीस',
                48:'अठ्ठेचाळीस',49:'एकोणपन्नास',50:'पन्नास',51:'एक्कावन्न',52:'बावन्न',53:'त्रेपन्न',54:'चोपन्न',
                55:'पंचावन्न',56:'छप्पन्न',57:'सत्तावन्न',58:'अठ्ठावन्न',59:'एकोणसाठ',60:'साठ',61:'एकसष्ठ',
                62:'बासष्ठ',63:'त्रेसष्ठ',64:'चौसष्ठ',65:'पासष्ठ',66:'सहासष्ठ',67:'सदुसष्ठ',68:'अडुसष्ठ',
                69:'एकोणसत्तर',70:'सत्तर',71:'एक्काहत्तर',72:'बाहत्तर',73:'त्र्याहत्तर',74:'चौर्‍याहत्तर',75:'पंच्याहत्तर',
                76:'शहात्तर',77:'सत्याहत्तर',78:'अठ्ठ्याहत्तर',79:'एकोण ऐंशी',80:'ऐंशी',81:'एक्क्याऐंशी',82:'ब्याऐंशी',
                83:'त्र्याऐंशी',84:'चौऱ्याऐंशी',85:'पंच्याऐंशी',86:'शहाऐंशी',87:'सत्त्याऐंशी',88:'अठ्ठ्याऐंशी',89:'एकोणनव्वद',
                90:'नव्वद',91:'एक्क्याण्णव',92:'ब्याण्णव',93:'त्र्याण्णव',94:'चौऱ्याण्णव',95:'पंच्याण्णव',96:'शहाण्णव',
                97:'सत्त्याण्णव',98:'अठ्ठ्याण्णव',99:'नव्यान्नव',100:'शंभर'}
        numPunjabi={0:' ',1:'ਇੱਕ',2:'ਦੋ',3:'ਤਿੰਨ',4:'ਚਾਰ',5:'ਪੰਜ',6:'ਛੇ',7:'ਸੱਤ',8:'ਅੱਠ',9:'ਨੌ',10:'ਦਸ',   #0:'ਸਿਫਰ',
                11:'ਗਿਆਰਾਂ',12:'ਬਾਰਾਂ',13:'ਤੇਰਾਂ',14:'ਚੌਦਾਂ',15:'ਪੰਦਰਾਂ',16:'ਸੋਲਾਂ',17:'ਸਤਾਰਾਂ',18:'ਅਠਾਰਾਂ',19:'ਉੱਨੀ',
                20:'ਵੀਹ',21:'ਇੱਕੀ',22:'ਬਾਈ',23:'ਤੇਈ',24:'ਚੌਬੀ',25:'ਪੱਚੀ',26:'ਛੱਬੀ',27:'ਸਤਾਈ',28:'ਅਠਾਈ',29:'ਉਨੱਤੀ',
                30:'ਤੀਹ',31:'ਇਕੱਤੀ',32:'ਬੱਤੀ',33:'ਤੇਤੀ',34:'ਚੌਂਤੀ',35:'ਪੈਂਤੀ',36:'ਛੱਤੀ',37:'ਸੈਂਤੀ',38:'ਅਠੱਤੀ',39:'ਉਨਤਾਲੀ',
                40:'ਚਾਲੀ',41:'ਇਕਤਾਲੀ',42:'ਬਿਆਲੀ',43:'ਤਰਤਾਈ',44:'ਚੁਤਾਲੀ',45:'ਪਨਤਾਲੀ',46:'ਛਿਆਲੀ',47:'ਸਨਤਾਲੀ',
                48:'ਅਠਤਾਲੀ',49:'ਉਨੰਜਾ',50:'ਪੰਜਾਹ',51:'ਇਕਵੰਜਾ',52:'ਬਵੰਜਾ',53:'ਤਰਵੰਜਾ',54:'ਚਰਵੰਜਾ',55:'ਪਚਵੰਜਾ',
                56:'ਛਪੰਜਾ',57:'ਸਤਵੰਜਾ',58:'ਅਠਵੰਜਾ',59:'ਉਨਾਹਠ',60:'ਸੱਠ',61:'ਇਕਾਹਠ',62:'ਬਾਹਠ',63:'ਤਰੇਂਹਠ',
                64:'ਚੌਂਹਠ',65:'ਪੈਂਹਠ',66:'ਛਿਆਹਠ',67:'ਸਤਾਹਠ',68:'ਅਠਾਹਠ',69:'ਉਨੱਤਰ',70:'ਸੱਤਰ',71:'ਇਕਹੱਤਰ',
                72:'ਬਹੱਤਰ',73:'ਤਹੇਤਰ',74:'ਚਹੱਤਰ',75:'ਪਚੱਤਰ',76:'ਛਿਅੱਤਰ',77:'ਸਤੱਤਰ',78:'ਅਠੱਤਰ',79:'ਉਨਾਸੀ',
                80:'ਅੱਸੀ',81:'ਇਕਆਸੀ',82:'ਬਿਆਸੀ',83:'ਤਿਰਾਸੀ',84:'ਚੌਰਾਸੀ',85:'ਪਚਾਸੀ',86:'ਛਿਆਸੀ',87:'ਸਤਾਸੀ',
                88:'ਅਠਾਸੀ',89:'ਉਨੱਨਵੇਂ',90:'ਨੱਬੇ',91:'ਇਕੱਨਵੇ',92:'ਬੱਨਵੇ',93:'ਤਰੱਨਵੇ',94:'ਚਰੱਨਵੇ',95:'ਪਚੱਨਵੇ',
                96:'ਛਿਅੱਨਵੇ',97:'ਸਤੱਨਵੇ',98:'ਅਠੱਨਵੇ',99:'ਨੜਿੱਨਵੇ',100:'ਸੌ'}
        numKannada={0:' ',1:'ಒಂದು',2:'ಎರಡು',3:'ಮೂರು',4:'ನಾಲ್ಕು',5:'ಅಯ್ದು',6:'ಆರು',7:'ಏಳು',8:'ಎಂಟು',    #0:'ಸೊನ್ನೆ',
                9:'ಒಂಬತ್ತು',10:'ಹತ್ತು',11:'ಹನ್ನೊಂದು',12:'ಹನ್ನೆರಡು',13:'ಹದಿಮೂರು',14:'ಹದಿನಾಲ್ಕು',15:'ಹದಿನೈದು',
                16:'ಹದಿನಾರು',17:'ಹದಿನೇಳು',18:'ಹದಿನೆಂಟು',19:'ಹತ್ತೊಂಬತ್ತು',20:'ಇಪ್ಪತ್ತು',21:'ಇಪ್ಪತ್ತ್\’ಒಂದು',
                22:'ಇಪ್ಪತ್ತ್\’ಎರಡು',23:'ಇಪ್ಪತ್ತ್\’ಮೂರು',24:'ಇಪ್ಪತ್ತ್\’ನಾಲ್ಕು',25:'ಇಪ್ಪತ್ತ್\’ಐದು',26:'ಇಪ್ಪತ್ತ್\’ಆರು',
                27:'ಇಪ್ಪತ್ತ್\’ಏಳು',28:'ಇಪ್ಪತ್ತ್\’ಎಂಟು',29:'ಇಪ್ಪತ್ತ್\’ಒಂಬತ್ತು',30:'ಮೂವತ್ತು',31:'ಮುವತ್ತ್\’ಒಂದು',
                32:'ಮುವತ್ತ್\’ಎರಡು',33:'ಮುವತ್ತ್\’ಮೂರು',34:'ಮೂವತ್ತ್\’ನಾಲ್ಕು',35:'ಮೂವತ್ತ್\’ಐದು',36:'ಮೂವತ್ತ್\’ಆರು',
                37:'ಮೂವತ್ತ್\’ಏಳು',38:'ಮೂವತ್ತ್\’ಎಂಟು',39:'ಮೂವತ್ತ್\’ಒಂಬತ್ತು',40:'ನಲವತ್ತು',
                41: "ನಲವತ್ತೊಂದು",
                42: "ನಲವತ್ತ್ ಎರಡು",
                43: "ನಲವತ್ತ್ ಮೂರು",
                44: "ನಲವತ್ತ್ ನಾಲ್ಕು",
                45: "ನಲವತ್ತೈದು",
                46: "ನಲವತ್ತಾರು",
                47: "ನಲವತ್ತೇಳು",
                48: "ನಲವತ್ತೆಂಟು",
                49: "ನಲವತ್ತೊಂಬತ್ತು",
                50:'ಐವತ್ತು',
                51: "ಐವತ್ತೊಂದು",
                52: "ಐವತ್ತೆರಡು",
                53: "ಐವತ್ತಮೂರು",
                54: "ಐವತ್ತ್ನಾಲ್ಕು",
                55: "ಐವತ್ತೈದು",
                56: "ಐವತ್ತಾರು",
                57: "ಐವತ್ತೇಳು",
                58: "ಐವತ್ತೆಂಟು",
                59: "ಐವತ್ತೊಂಬತ್ತು",
                60:'ಅರುವತ್ತು',
                61: "ಅರವತ್ತೊಂದು",
                62: "ಅರವತ್ತೆರಡು",
                63: "ಅರವತ್ತ್ ಮೂರು",
                64: "ಅರವತ್ತ್ ನಾಲ್ಕು",
                65: "ಅರವತ್ತೈದು",
                66: "ಅರವತ್ತಾರು",
                67: "ಅರವತ್ತೇಳು",
                68: "ಅರವತ್ತೆಂಟು",
                69: "ಅರವತ್ತೊಂಬತ್ತು",
                70:'ಎಪ್ಪತ್ತು',
                71: "ಎಪ್ಪತ್ತೊಂದು",
                72: "ಎಪ್ಪತ್ತೆರಡು",
                73: "ಎಪ್ಪತ್ತ್ ಮೂರು",
                74: "ಎಪ್ಪತ್ತ್ ನಾಲ್ಕು",
                75: "ಎಪ್ಪತ್ತೈದು",
                76: "ಎಪ್ಪತ್ತಾರು",
                77: "ಎಪ್ಪತ್ತೇಳು",
                78: "ಎಪ್ಪತ್ತೆಂಟು",
                79: "ಎಪ್ಪತ್ತೊಂಬತ್ತು",
                80:'ಎಂಬತ್ತು',
                81: "ಎಂಬತ್ತೊಂದು",
                82: "ಎಂಬತ್ತೆರಡು",
                83: "ಎಂಬತ್ತ್ ಮೂರು",
                84: "ಎಂಬತ್ತ್ ನಾಲ್ಕು",
                85: "ಎಂಬತ್ತೈದು",
                86: "ಎಂಬತ್ತಾರು",
                87: "ಎಂಬತ್ತೇಳು",
                88: "ಎಂಬತ್ತೆಂಟು",
                89: "ಎಂಬತ್ತೊಂಬತ್ತು",
                90:'ತೊಂಬತ್ತು',
                91: "ತೊಂಬತ್ತೊಂದು",
                92: "ತೊಂಬತ್ತೆರಡು",
                93: "ತೊಂಬತ್ತ ಮೂರು",
                94: "ತೊಂಬತ್ತ ನಾಲ್ಕು",
                95: "ತೊಂಬತ್ತೈದು",
                96: "ತೊಂಬತ್ತಾರು",
                97: "ತೊಂಬತ್ತೇಳು",
                98: "ತೊಂಬತ್ತೆಂಟು",
                99: "ತೊಂಬತ್ತೊಂಬತ್ತು",
                100:'ನೂರು'}
        numTamil = {
                0:"",  #0:"பூஜ்ஜியம்",
                1:"ஒன்று",
                2:"இரண்டு",
                3:"மூன்று",
                4:"நான்கு",
                5:"ஐந்து",
                6:"ஆறு",
                7:"ஏழு",
                8:"எட்டு",
                9:"ஒன்பது",
                10:"பத்து",
                11:"பதினொன்று",
                12:"பன்னிரண்டு",
                13:"பதிமூன்று",
                14:"பதினான்கு",
                15:"பதினைந்து",
                16:"பதினாறு",
                17:"பதினேழு",
                18:"பதினெட்டு",
                19:"பத்தொன்பது",
                20:"இருபது",
                21:"இருபது ஒன்று",
                22:"இருபத்து இரண்டு",
                23:"இருபத்து மூன்று",
                24:"இருபத்து நான்கு",
                25:"இருபத்து ஐந்து",
                26:"இருபத்து ஆறு",
                27:"இருபத்து ஏழு",
                28:"இருபத்து எட்டு",
                29:"இருபத்து ஒன்பது",
                30:"முப்பது",
                31:"முப்பத்து ஒன்று",
                32:"முப்பத்து இரண்டு",
                33:"முப்பத்து மூன்று",
                34:"முப்பத்து நான்கு",
                35:"முப்பத்து ஐந்து",
                36:"முப்பத்து ஆறு",
                37:"முப்பத்து ஏழு",
                38:"முப்பத்து எட்டு",
                39:"முப்பத்து ஒன்பது",
                40:"நாற்பது",
                41:"நாற்பத்து ஒன்று",
                42:"நாற்பத்து இரண்டு",
                43:"நாற்பத்து மூன்று",
                44:"நாற்பத்து நான்கு",
                45:"நாற்பத்து ஐந்து",
                46:"நாற்பத்து ஆறு",
                47:" நாற்பத்து ஏழு",
                48:"நாற்பத்து எட்டு",
                49:"நாற்பத்து ஒன்பது",
                50:"ஐம்பது",
                51:"ஐம்பத்து ஒன்று",
                52:"ஐம்பத்து இரண்டு",
                53:"ஐம்பத்து மூன்று",
                54:"ஐம்பத்து நான்கு",
                55:"ஐம்பத்து ஐந்து",
                56:"ஐம்பத்து ஆறு",
                57:"ஐம்பத்து ஏழு",
                58:"ஐம்பத்து எட்டு",
                59:"ஐம்பத்து ஒன்பது",
                60:"அறுபது",
                61:"அறுபத்து ஒன்று",
                62:"அறுபத்து இரண்டு",
                63:"அறுபத்து மூன்று",
                64:"அறுபத்து நான்கு",
                65:"அறுபத்து ஐந்து",
                66:"அறுபத்து ஆறு",
                67:"அறுபத்து ஏழு",
                68:"அறுபத்து எட்டு",
                69:"அறுபத்து ஒன்பது",
                70:"எழுபது",
                71:"எழுபத்தி ஒன்று",
                72:"எழுபத்தி இரண்டு",
                73:"எழுபத்தி முச்சக்கர",
                74:"எழுபத்தி நான்கு",
                75:"எழுபத்தி ஐந்து",
                76:"எழுபத்தி ஆறு",
                77:"எழுபத்தி ஏழு",
                78:"எழுபத்தி எட்டு",
                79:"எழுபத்தி ஒன்பது",
                80:"எண்பது",
                81:"எண்பத்தியொன்று",
                82:"எண்பத்திரண்டு",
                83:"எண்பத்திமூன்று",
                84:"என்பதினான்கு",
                85:"என்பதினைந்து",
                86:"எண்பத்திஆறு",
                87:"எண்பத்திஏழு",
                88:"எண்பத்தியெட்டு",
                89:"எண்பத்தியொன்பது",
                90:"தொன்னூறு",
                91:"தொண்ணூற்றியொன்று",
                92:"தொண்ணூற்றிரண்டு",
                93:"தொண்ணூற்றிமூன்று",
                94:"தொண்ணூற்றிநான்கு",
                95:"தொண்ணூற்றிஐந்து",
                96:"தொண்ணூற்றியாறு",
                97:"தொண்ணூற்றியேழு",
                98:"தொண்ணூற்றியெட்டு",
                99:"தொண்ணூற்றிஒன்பது",
                100:"நூறு",
        }
                                                        


        k=1000
        oneLakh=k*100
        tenLakh=k*1000
        crore=k*10000
        tenCrore=k*100000
        arab=k*1000000
        tenArab=10000000000
        kharab=100000000000
        tenKharab=1000000000000
        neela=10000000000000
        tenNeela=100000000000000
        padma=1000000000000000
        tenPadma=10000000000000000
        shangkha=100000000000000000
        tenShangkha=1000000000000000000
        
        assert(0 <= number)
            
        if number < 100: 
            if language == "english":
                return numEnglish[number]
            elif language == 'hindi':
                return numHindi[number]
            elif language == 'marathi':
                return numMarathi[number]
            elif language == 'gujarati':
                return numGujarati[number]
            elif language == 'punjabi':
                return numPunjabi[number]
            elif language == 'kannada':
                return numKannada[number]
            elif language == 'malayalam':
                return numMalayalam[number]
            elif language == 'telugu':
                return numTelugu[number]
            elif language == 'odia':
                return numOdia[number]
            elif language == 'bengali':
                return numBengali[number]
            elif language == 'marathi':
                return numMarathi[number]
            elif language == 'tamil':
                return numTamil[number]
                
        elif number < 1000:
            if number % 100 == 0:
                if language == "english":
                    return numEnglish[number // 100] + ' hundred'
                elif language == 'hindi':
                    return numHindi[number // 100] + ' सौ'
                if language == 'gujarati':
                    return numGujarati[number // 100] + ' સો'
                if language == 'marathi':
                    return numMarathi[number // 100] + ' शंभर'
                if language == 'punjabi':
                    return numPunjabi[number // 100] + ' ਸੌ'
                if language == 'odia':
                    return numOdia[number // 100] + ' ଶହେ'
                if language == 'bengali':
                    return numBengali[number // 100] + ' শত'
                if language == 'telugu':
                    return numTelugu[number // 100] + ' వంద'
                if language == 'malayalam':
                    return numMalayalam[number // 100] + ' നൂറ്'
                if language == 'kannada':
                    return numKannada[number // 100] + ' ನೂರು'
                if language == 'tamil':
                    return numTamil[number // 100] + ' நூறு'
            else:
                if language == "english":
                    return numEnglish[number // 100] + ' Hundred ' + self.readNumber(number % 100,language)
                elif language == 'hindi':
                    return numHindi[number // 100] + ' सौ ' + self.readNumber(number % 100,language)
                if language == 'gujarati':
                    return numGujarati[number // 100] + ' સો ' + self.readNumber(number % 100,language)
                if language == 'marathi':
                    return numMarathi[number // 100] + ' शंभर ' + self.readNumber(number % 100,language)
                if language == 'punjabi':
                    return numPunjabi[number // 100] + ' ਸੌ ' + self.readNumber(number % 100,language)
                if language == 'odia':
                    return numOdia[number // 100] + ' ଶହେ ' + self.readNumber(number % 100,language)
                if language == 'bengali':
                    return numBengali[number // 100] + ' শত ' + self.readNumber(number % 100,language)
                if language == 'telugu':
                    return numTelugu[number // 100] + ' వంద ' + self.readNumber(number % 100,language)
                if language == 'malayalam':
                    return numMalayalam[number // 100] + ' നൂറ് ' + self.readNumber(number % 100,language)
                if language == 'kannada':
                    return numKannada[number // 100] + ' ನೂರು ' + self.readNumber(number % 100,language)
                if language == 'tamil':
                    return numTamil[number // 100] + ' நூறு ' + self.readNumber(number % 100,language)
        elif number < 10000: #less than ten thousand
            if number % 1000 == 0:
                if language == "english":
                    return numEnglish[number // 1000] + ' thousand'
                elif language == 'hindi':
                    return numHindi[number // 1000] + ' हजार'
                if language == 'gujarati':
                    return numGujarati[number // 1000] + ' હજાર'
                if language == 'marathi':
                    return numMarathi[number // 1000] + ' हजार'
                if language == 'punjabi':
                    return numPunjabi[number // 1000] + ' ਹਜ਼ਾਰ'
                if language == 'odia':
                    return numOdia[number // 1000] + ' ହଜାରେ'
                if language == 'bengali':
                    return numBengali[number // 1000] + ' হাজার'
                if language == 'telugu':
                    return numTelugu[number // 1000] + ' వెయ్యి'
                if language == 'malayalam':
                    return numMalayalam[number // 1000] + ' ആയിരം'
                if language == 'kannada':
                    return numKannada[number // 1000] + ' ಸಾವಿರ'
                if language == 'tamil':
                    return numTamil[number // 1000] + ' ஆயிரம்'
            else:
                if language == "english":
                    return numEnglish[number // 1000] + ' thousand ' + self.readNumber(number % 1000,language)
                elif language == 'hindi':
                    return numHindi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
                elif language == 'marathi':
                    return numMarathi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
                elif language == 'gujarati':
                    return numGujarati[number // 1000] + ' હજાર ' + self.readNumber(number % 1000,language)
                elif language == 'punjabi':
                    return numPunjabi[number // 1000] + ' ਹਜ਼ਾਰ ' + self.readNumber(number % 1000,language)
                elif language == 'kannada':
                    return numKannada[number // 1000] + ' ಸಾವಿರ ' + self.readNumber(number % 1000,language)
                elif language == 'malayalam':
                    return numMalayalam[number // 1000] + ' ആയിരം ' + self.readNumber(number % 1000,language)
                elif language == 'telugu':
                    return numTelugu[number // 1000] + ' వెయ్యి ' + self.readNumber(number % 1000,language)
                elif language == 'odia':
                    return numOdia[number // 1000] + ' ହଜାରେ ' + self.readNumber(number % 1000,language)
                elif language == 'bengali':
                    return numBengali[number // 1000] + ' হাজার ' + self.readNumber(number % 1000,language)
                elif language == 'tamil':
                    return numTamil[number // 1000] + ' ஆயிரம் ' + self.readNumber(number % 1000,language)
    
        elif number < 100000: #less than one lakh
            if number%1000 == 0:
                if language == "english":
                    return numEnglish[number // 1000] + ' thousand ' 
                elif language == 'hindi':
                    return numHindi[number // 1000] + ' हजार ' 
                elif language == 'marathi':
                    return numMarathi[number // 1000] + ' हजार ' 
                elif language == 'gujarati':
                    return numGujarati[number // 1000] + ' હજાર '
                elif language == 'punjabi':
                    return numPunjabi[number // 1000] + ' ਹਜ਼ਾਰ ' 
                elif language == 'kannada':
                    return numKannada[number // 1000] + ' ಸಾವಿರ ' 
                elif language == 'malayalam':
                    return numMalayalam[number // 1000] + ' ആയിരം ' 
                elif language == 'telugu':
                    return numTelugu[number // 1000] + ' వెయ్యి ' 
                elif language == 'odia':
                    return numOdia[number // 1000] + ' ହଜାରେ ' 
                elif language == 'bengali':
                    return numBengali[number // 1000] + ' হাজার ' 
                elif language == 'tamil':
                    return numTamil[number // 1000] + ' ஆயிரம் ' 
            else:
                if language == "english":
                    return numEnglish[number // 1000] + ' thousand ' + self.readNumber(number % 1000,language)
                elif language == 'hindi':
                    return numHindi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
                elif language == 'marathi':
                    return numMarathi[number // 1000] + ' हजार ' + self.readNumber(number % 1000,language)
                elif language == 'gujarati':
                    return numGujarati[number // 1000] + ' હજાર ' + self.readNumber(number % 1000,language)
                elif language == 'punjabi':
                    return numPunjabi[number // 1000] + ' ਹਜ਼ਾਰ ' + self.readNumber(number % 1000,language)
                elif language == 'kannada':
                    return numKannada[number // 1000] + ' ಸಾವಿರ ' + self.readNumber(number % 1000,language)
                elif language == 'malayalam':
                    return numMalayalam[number // 1000] + ' ആയിരം ' + self.readNumber(number % 1000,language)
                elif language == 'telugu':
                    return numTelugu[number // 1000] + ' వెయ్యి ' + self.readNumber(number % 1000,language)
                elif language == 'odia':
                    return numOdia[number // 1000] + ' ହଜାରେ ' + self.readNumber(number % 1000,language)
                elif language == 'bengali':
                    return numBengali[number // 1000] + ' হাজার ' + self.readNumber(number % 1000,language)
                elif language == 'tamil':
                    return numTamil[number // 1000] + ' ஆயிரம் ' + self.readNumber(number % 1000,language)
                      
        elif number < tenLakh: #less than ten lakh
            if number%1000000 == 0:
                if language == "english":
                    return numEnglish[number // 100000] + ' lakh ' 
                elif language == 'hindi':
                    return numHindi[number // 100000] + ' लाख ' 
                elif language == 'marathi':
                    return numMarathi[number // 100000] + ' लाख '
                elif language == 'gujarati':
                    return numGujarati[number // 1000] + ' लाख '
                elif language == 'punjabi':
                    return numPunjabi[number // 100000] + ' लाख ' 
                elif language == 'kannada':
                    return numKannada[number // 100000] + ' ಲಕ್ಷ ' 
                elif language == 'malayalam':
                    return numMalayalam[number // 100000] + ' ലക്ഷം '
                elif language == 'telugu':
                    return numTelugu[number // 100000] + ' లాక్ '
                elif language == 'odia':
                    return numOdia[number // 100000] + ' ଲକ୍ଷ ' 
                elif language == 'bengali':
                    return numBengali[number // 100000] + ' लाख ' 
                elif language == 'tamil':
                    return numTamil[number // 100000] + ' இலட்சம் ' 
            else:
                if language == "english":
                    return numEnglish[number // 100000] + ' lakh ' + self.readNumber(number % 100000,language)
                elif language == 'hindi':
                    return numHindi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
                elif language == 'marathi':
                    return numMarathi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
                elif language == 'gujarati':
                    return numGujarati[number // 1000] + ' लाख ' + self.readNumber(number % 100000,language)
                elif language == 'punjabi':
                    return numPunjabi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
                elif language == 'kannada':
                    return numKannada[number // 100000] + ' ಲಕ್ಷ ' + self.readNumber(number % 100000,language)
                elif language == 'malayalam':
                    return numMalayalam[number // 100000] + ' ലക്ഷം ' + self.readNumber(number % 100000,language)
                elif language == 'telugu':
                    return numTelugu[number // 100000] + ' లాక్ ' + self.readNumber(number % 100000,language)
                elif language == 'odia':
                    return numOdia[number // 100000] + ' ଲକ୍ଷ ' + self.readNumber(number % 100000,language)
                elif language == 'bengali':
                    return numBengali[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
                elif language == 'tamil':
                    return numTamil[number // 100000] + ' இலட்சம் ' + self.readNumber(number % 100000,language)
        
        elif number < crore: #less than one crore
            if language == "english":
                return numEnglish[number // 100000] + ' lakh ' + self.readNumber(number % 100000,language)
            elif language == 'hindi':
                return numHindi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'gujarati':
                return numGujarati[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
            elif language == 'kannada':
                return numKannada[number // 100000] + ' ಲಕ್ಷ ' + self.readNumber(number % 100000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000] + ' ലക്ഷം ' + self.readNumber(number % 100000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000] + ' లాక్ ' + self.readNumber(number % 100000,language)
            elif language == 'odia':
                return numOdia[number // 100000] + ' ଲକ୍ଷ ' + self.readNumber(number % 100000,language)
            elif language == 'bengali':
                return numBengali[number // 100000] + ' लाख ' + self.readNumber(number % 100000)            
            elif language == 'tamil':
                return numTamil[number // 100000] + ' இலட்சம் ' + self.readNumber(number % 100000)            
                #return numHindi[number // 100000] + ' लाख ' + self.readNumber(number % 100000,language)
        elif number < tenCrore: #less than
            if language == "english":
                return numEnglish[number // 10000000] + ' crore ' + self.readNumber(number % 10000000,language)
            elif language == 'hindi':
                return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'tamil':
                return numTamil[number // 10000000] + ' கோடி ' + self.readNumber(number % 10000000,language)
                #return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000)   
        elif number < arab: #less than
            if language == "english":
                return numEnglish[number // 10000000] + ' crore ' + self.readNumber(number % 10000000,language)
            elif language == 'hindi':
                return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
            elif language == 'tamil':
                return numTamil[number // 10000000] + ' கோடி ' + self.readNumber(number % 10000000,language)
                #return numHindi[number // 10000000] + ' करोड़ ' + self.readNumber(number % 10000000,language)
        elif number < tenArab: #less than
            if language == "english":
                return numEnglish[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'hindi':
                return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'kannada':
                return numKannada[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'odia':
                return numOdia[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'bengali':
                return numBengali[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'tamil':
                return numTamil[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
                #return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
        elif number < kharab: #less than
            if language == "english":
                return numEnglish[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'hindi':
                return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'kannada':
                return numKannada[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'odia':
                return numOdia[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'bengali':
                return numBengali[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
            elif language == 'tamil':
                return numTamil[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
                #return numHindi[number // 1000000000] + ' अरब ' + self.readNumber(number % 1000000000,language)
        elif number < tenKharab: #less than
            if language == "english":
                return numEnglish[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'hindi':
                return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'kannada':
                return numKannada[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'odia':
                return numOdia[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'bengali':
                return numBengali[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'tamil':
                return numTamil[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
                #return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
        elif number < neela: #less than
            if language == "english":
                return numEnglish[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'hindi':
                return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'kannada':
                return numKannada[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'odia':
                return numOdia[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'bengali':
                return numBengali[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
            elif language == 'tamil':
                return numTamil[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
                #return numHindi[number // 100000000000] + ' खरब ' + self.readNumber(number % 100000000000,language)
        elif number < tenNeela: #less than
            if language == "english":
                return numEnglish[number]
            elif language == 'hindi':
                return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'tamil':
                return numTamil[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)

                #return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
        elif number < padma: #less than
            if language == 'hindi':
                return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'marathi':
                return numMarathi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'gujarati':
                return numGujarati[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'punjabi':
                return numPunjabi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'kannada':
                return numKannada[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'malayalam':
                return numMalayalam[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'telugu':
                return numTelugu[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'odia':
                return numOdia[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'bengali':
                return numBengali[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
            elif language == 'tamil':
                return numTamil[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)

                #return numHindi[number // 10000000000000] + ' नील ' + self.readNumber(number % 10000000000000,language)
        elif number < tenPadma: #less than
            if language == 'hindi':
                return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'marathi':
                return numMarathi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'gujarati':
                return numGujarati[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'punjabi':
                return numPunjabi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'kannada':
                return numKannada[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'malayalam':
                return numMalayalam[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'telugu':
                return numTelugu[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'odia':
                return numOdia[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'bengali':
                return numBengali[number // padma] + ' नील ' + self.readNumber(number % padma,language)
            elif language == 'tamil':
                return numTamil[number // padma] + ' नील ' + self.readNumber(number % padma,language)
                #return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
        elif number < shangkha: #less than
            if language == 'hindi':
                return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'marathi':
                return numMarathi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'gujarati':
                return numGujarati[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'punjabi':
                return numPunjabi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'kannada':
                return numKannada[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'malayalam':
                return numMalayalam[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'telugu':
                return numTelugu[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'odia':
                return numOdia[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'bengali':
                return numBengali[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
            elif language == 'tamil':
                return numTamil[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
          
                #return numHindi[number // padma] + ' पद्म ' + self.readNumber(number % padma,language)
        elif number < tenShangkha: #less than
            if language == 'hindi':
                return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'marathi':
                return numMarathi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'gujarati':
                return numGujarati[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'punjabi':
                return numPunjabi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'kannada':
                return numKannada[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'malayalam':
                return numMalayalam[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'telugu':
                return numTelugu[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'odia':
                return numOdia[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'bengali':
                return numBengali[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'tamil':
                return numTamil[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)

                #return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
        elif number >= tenShangkha : #less than
            if language == 'hindi':
                return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'marathi':
                return numMarathi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'gujarati':
                return numGujarati[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'punjabi':
                return numPunjabi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'kannada':
                return numKannada[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'malayalam':
                return numMalayalam[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'telugu':
                return numTelugu[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'odia':
                return numOdia[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'bengali':
                return numBengali[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)
            elif language == 'tamil':
                return numTamil[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha,language)

                #return numHindi[number // shangkha] + ' शंख ' + self.readNumber(number % shangkha)
        raise AssertionError('the number is too large: %s' % str(number))
    
    def parseSymbols(self, sentence,language):
        
        #comma separated 12,300 or 12,300.00
        numWithComma= '[\d]+[.,\d]+'
        if bool(''.join(re.findall(numWithComma,sentence)))==True:
            withComma=''.join(re.findall(numWithComma,sentence))
            commaRemoved=withComma.replace(',','')
            sentence=sentence.replace(withComma,commaRemoved)
            
        #decimal / floats 0.123 or .123
        decimal='[\d]*[.][\d]+'
        postPointNum=[]
        if bool(''.join(re.findall(decimal,sentence)))==True:
            decimalNum=''.join(re.findall(decimal,sentence))
            postPoint=''.join(re.findall('[.][\d]+',decimalNum))
            for aNum in postPoint:
                if aNum !='.':
                    postPointNum.append(''.join(self.readNumber(int(aNum),language)))
            
            sentence=sentence.replace(postPoint,' पोय्ण्ट् '+' '.join(postPointNum))
        #number 1234
        numbers='[\d]+'
        #all types of number
        wholeNumber = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        numbersAll=''.join(re.findall(numbers,sentence))
        # print(numbersAll)
        sentence=sentence.replace(numbersAll,self.readNumber(int(numbersAll),language))
        
        return sentence


def convert_numbers(number,language):
    print("number in file ",number)
    print("language",language)
    # start_time = datetime.datetime.now()
    sp = SymbolParser()
    number = sp.parseSymbols(number,language)
    if "zero" in number:
        number = number.replace("zero","")
    # print("Delay ---> ",datetime.datetime.now()-start_time)
    return number

# start_time = time.time()
# print(convert_numbers("99110","english"))
# print("delay in conve",time.time()-start_time)

