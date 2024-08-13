import re
import win32clipboard
import datetime
Minimum88 = False #8/8 minimum reqs. True for yes, false for no.
class ParsingWizard():
    def __init__(self):
        now = datetime.datetime.now()
        date = "{}-{}-{}_{}_{}_{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        #log = 'C:\\Users\\Administrator\\Desktop\Parse\\logs\\'
        win32clipboard.OpenClipboard()
        try:
            self.data = win32clipboard.GetClipboardData()
        except:
            win32clipboard.CloseClipboard()
        #with open(log+''+date+'_parse.json','w') as f:
        #    f.write(self.data)
        print('No clipboard data found')
        win32clipboard.CloseClipboard()
    def ID_Monster(self):
        count = 0
        Name = re.findall(r'\"name\":\"([a-zA-Z0-9\' ]+)\"', self.data)
        Class = re.findall(r'\"class\":\"([a-zA-Z]+)\"', self.data)
        Level = str(re.findall(r'\"level\":([0-9]+)', self.data))
        Guild = re.findall(r'\"guild\":\"([a-zA-Z0-9\'\- ]+)\"', self.data)
        Seasonal = re.findall(r'\"seasonal\":\"([a-z]+)\"', self.data)
        Crucible = re.findall(r'\"crucible\":\"([a-z]+)\"', self.data)
        Weapon = re.findall(r'\"weapon\":\"([a-zA-Z0-9\'\-\. ]+)\"', self.data)
        WeaponID = re.findall(r'\"weaponid\":([\-0-9]+)', self.data)
        Ability = re.findall(r'\"ability\":\"([a-zA-Z0-9\'\-\. ]+)\"', self.data)
        AbilityID = re.findall(r'\"abilityid\":([\-0-9]+)', self.data)
        Armor = re.findall(r'\"armor\":\"([a-zA-Z0-9\'\-\. ]+)\"', self.data)
        ArmorID = re.findall(r'\"armorid\":([\-0-9]+)', self.data)
        Ring = re.findall(r'\"ring\":\"([a-zA-Z0-9\'\-\. ]+)\"', self.data)
        RingID = re.findall(r'\"ringid\":([\-0-9]+)', self.data)
        MaxStats = re.findall(r'\"maxstats\":([0-9]+)', self.data)
        MissingStats = re.findall(r'\"missingstats\":{[^}]+}', self.data)
        UnderreqsList = []
        UnderreqsNames = []
        UnderreqsKick = []
        for each in Name:
            UnderreqsReason = []
            #Sets reqs, will change to false if they are under reqs later
            WeaponReqs = True
            AbilityReqs = True
            ArmorReqs = True
            RingReqs = True
            try:
                MaxAtt = re.search(r'\"Atk\":([\d+]+)', MissingStats[count]).group(1)
                if int(MaxAtt) <= 3 and Minimum88 == False:
                    MaxAtt = 0
                else:
                    UnderreqsReason.append("Att")
            except AttributeError:
                MaxAtt = 0
            try:
                MaxDex = re.search(r'\"Dex\":([\d+]+)', MissingStats[count]).group(1)
                if int(MaxDex) <= 3 and Minimum88 == False:
                    MaxDex = 0
                else:
                    UnderreqsReason.append("Dex")
            except AttributeError:
                MaxDex = 0
            for match in re.findall('Unloaded', Weapon[count]) or re.findall('T0 ', Weapon[count]) or re.findall('T1 ', Weapon[count]) or re.findall('T2 ', Weapon[count]) or re.findall('T3 ', Weapon[count])or re.findall('T4', Weapon[count])or re.findall('T5 ', Weapon[count])or re.findall('T6 ', Weapon[count])or re.findall('T7 ', Weapon[count])or re.findall('T8 ', Weapon[count])or re.findall('T9 ', Weapon[count])or re.findall('T10 ', Weapon[count]):# or re.findall('T11 ', Weapon[count]):
                WeaponReqs = False
                UnderreqsReason.append("Weapon")
            for match in re.findall('Unloaded', Ability[count]) or re.findall('T0 ', Ability[count]) or re.findall('T1 ', Ability[count]) or re.findall('T2 ', Ability[count]) or re.findall('T3 ', Ability[count]):
                if Class[count] != "Trickster":
                    if Class[count] != "Priest":
                        AbilityReqs = False
                        UnderreqsReason.append("Ability")
            for match in re.findall('Unloaded', Armor[count]) or re.findall('T0 ', Armor[count]) or re.findall('T1 ', Armor[count]) or re.findall('T2 ', Armor[count]) or re.findall('T3 ', Armor[count])or re.findall('T4', Armor[count])or re.findall('T5 ', Armor[count])or re.findall('T6 ', Armor[count])or re.findall('T7 ', Armor[count])or re.findall('T8 ', Armor[count])or re.findall('T9 ', Armor[count])or re.findall('T10 ', Armor[count]):#or re.findall('T11 ', Armor[count]):
                ArmorReqs = False
                #UnderreqsReason.append("Armor")
            for match in re.findall('Unloaded', Ring[count]) or re.findall('T0 ', Ring[count]) or re.findall('T1 ', Ring[count]) or re.findall('T2 ', Ring[count]) or re.findall('T3 ', Ring[count]):
                RingReqs = False
                UnderreqsReason.append("Ring")
            if WeaponReqs == False or AbilityReqs == False or ArmorReqs == False or RingReqs == False or int(MaxAtt) != 0 or MaxDex != 0:
                UnderreqsList.append(Name[count]+"|"+Weapon[count]+"|"+Ability[count]+"|"+Armor[count]+"|"+Ring[count]+"|MaxedStats: "+MaxStats[count]+"|Att: "+str(MaxAtt)+"|Dex: "+str(MaxDex))
                UnderreqsNames.append(Name[count] +" ["+", ".join(UnderreqsReason)+"]")
                UnderreqsKick.append(Name[count])
            count += 1
        for each in sorted(UnderreqsList):
            print(each)
        print('-----------------------------------')
        for each in sorted(UnderreqsNames):
            print(each)
        print('-----------------------------------')
        #print("Please /kick "+" ".join(UnderreqsKick)+ " for being under reqs")
ParsingWizard().ID_Monster()

