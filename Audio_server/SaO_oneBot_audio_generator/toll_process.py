import os, sys
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # This is your Project Root
print("e322",CURRENT_PATH)
sys.path.append(CURRENT_PATH)
from SaO_oneBot_audio_generator.gtts import synthesize_text as gtts
from SaO_oneBot_audio_generator.gtts import mstts as mstts
from num2words import num2words
from pydub import AudioSegment


numEnglish = { 0 : ' zero', 1 : ' one', 2 : ' two', 3 : ' three', 4 : ' four', 
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

numHindi = {0:'शून्य',1:'एक',2:'दो',3:'तीन',4:'चार',5:'पांच',  #0:'शून्य'
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
def get_audios(value,audio_server,language):
    print("language,",language)
    print("value<><><><>",value)
    sound=None
    new_num = ""
    num_lang = {
        "english":"numEnglish",
        "hindi":"numHindi"
    }
    for i in value:
        print("i<><>",i)
        new_num = new_num + " " + eval(num_lang[language])[int(i)]
    print("new_num<><>",new_num)
    if value+".wav" in os.listdir(f"{CURRENT_PATH}/{audio_server}/{language}/customer_care_number/"):
        sound = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/customer_care_number/{value}.wav")
    else:
        _ = eval(audio_server)(language=language,text=new_num,fileName=value,path_to_write=f"{CURRENT_PATH}/{audio_server}/{language}/customer_care_number/")
        sound = AudioSegment.from_wav(f"{CURRENT_PATH}/{audio_server}/{language}/customer_care_number/{value}.wav")
    return sound
