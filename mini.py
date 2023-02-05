#توجه . اسم استیت ها تک حرفی می باشد
class DFA:

    def __init__(self, states, alphabet, initial_state, final_states,
                 transition_function):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_function = transition_function

    def __str__(self):
        return f"states= {self.states}\nalphabet= {self.alphabet}\ninitial state= {self.initial_state}\nfinal states= {self.final_states}\ntransition function= {self.transition_function}"

    def isAccepted(self, _str):
        #استیت فعلی که در آن هستیم
        # که به صورت پیشفرض برابر با استیت شروع است
        current_state = self.initial_state
        # در این حلقه به ازای هر حرف در رشته تابع انتقال را نسبت به استیت فعلی صدا میزنیم و حرکت میکنیم
        for char in _str:
            next_state = self.transition_function[current_state][char]
            current_state = next_state
        # اگر با آخرین حرف رشته به یک استیت پذیرش رفته باشیم آنگاه رشته در زبان است
        if (current_state in self.final_states):
            return True
        else:
            return False

    def generator(self, len_of_str):
        #ساخت ارایه همه رشته ها با مقدار پیشفرض الفبا
        #از کپی برای این استفاده کردیم که تغییراتی که روی متغیر ال استرینگ اعمال میشه روی الفبا اثر نذاره
        all_strings = self.alphabet.copy()
        alpha=len(self.alphabet)
        # در این حلقه ابتدا ما از طول ۲ (چون به طول ۱ برابر الفباست ) شروع به ساخت رشته ها میکنیم تا طول خواسته شده
        # هدف اینست که به رشته های ساخته شده در مرحله ؛قبلی؛ کاراکتر های الفبا را بچسباینم و رشته به طول فعلی را بسازیم
        for i in range(2, len_of_str + 1):
            # در هرمرحله به تعداد طول الفبا به توان طول رشته تولید میشود
            #لذا نیاز است از خانه ای از ارایه شروع کنیم که رشته های تولیدی طول قبل شروع شوند
            start = len(all_strings) - (alpha**(i - 1))
            end = len(all_strings)
            #رشته های تولید شده در طول قبلی را انتخاب میکنیم و با کاراکتر های الفبا الحاق میکنیم
            for _str in all_strings[start:end]:
                for symbols in self.alphabet:
                    all_strings.append(_str + symbols)
        return all_strings

    def isEmpty(self):
        #هدف کلی اینست که تمام رشته های تا طول تعداد استیت را حساب کرده و چک کنیم که در زبان صدق میکنند یا خیر
        #اگر هیچ رشته ای در زبان صدق نکرد گوییم که زبان تهی است
        counter = 0
        self.generator(len(self.states))
        for _str in all_strings:
            if (self.isAccepted(_str)):
                counter += 1
                break
        if (counter != 0):
            print('Is Not Empty')
        else:
            print('Is Empty')

    def isInfinite(self):
        # روش کلی اینست که تمام رشته های با طول بین ان تا دو ان را میسازیم و روی آن پیمایش میکنیم
        # اگر رشته ای در این بازه پیدا شده آنگاه گوییم که زبان نامتناهی است
        n = len(self.states)
        all_strings_to_2n = self.generator(2 * n)
        counter = 0
        for _str in all_strings_to_2n:
            if (len(_str) >= n and self.isAccepted(_str)):
                counter += 1
                break
        if (counter != 0):
            return True
        else:
            return False

    def members_of_language(self):
        # روش کلی اینست که تمام رشته های تا طول ان را گرفته و هر کدام که در زبان صدق میکرد را در آرایه اعضا اضافه کنیم
        if (self.isInfinite()):
            print("Language is infinite!")
        else:
            all_strings_to_n = self.generator(len(self.states))
            members = []
            for string in all_strings_to_n:
                if (self.isAccepted(string)):
                    members.append(string)
            return members

    def number_of_members(self):
        if (self.isInfinite()):
            print("Language is infinite!")
        else:
            return (len(self.members_of_language()))

    def shortest_element(self):
        # از آنجایی که در آرایه اعضای زبان به ترتیب طول اضافه میشدند لذا کافیست اولین خانه ارایه را به عنوان کوتاه ترین طول برگردانیم
        if (self.isInfinite()):
            print("Language is infinite!")
        else:
            shortest = self.members_of_language()[0]
            return (shortest)

    def longest_element(self):
        if (self.isInfinite()):
            print("Language is infinite!")
        else:
            length = self.number_of_members()
            longest = self.members_of_language()[length - 1]
            return (longest)

    def supplement_dfa(self):
        # میدانیم متمم زبان برابرست با همان آتاماتا با این تفاوت که جای استیت های عادی و پذیرش عوض میشود
        if (self.isInfinite()):
            print("Language is infinite!")
        else:
            new_final = list(set(self.states) - set(self.final_states))
            L_supplement = DFA(self.states, self.alphabet, self.initial_state,
                               new_final, self.transition_function)
            return L_supplement

    def op(self, L2):
        #ترکیب
        transition_function = {}
        initial = self.initial_state + L2.initial_state
        combined_states = [initial]#لیست استیت های ترکیب شده با مقدار پیشفرض استیت های شروع هر زبان
        start = 0  #{'CP', 'CQ', 'BQ', 'AP', 'AR', 'CR'}
        been_saw = []
        while (start < len(combined_states)):# حلقه تا زمانی که به خانه ای  از ارایه اشاره کنیم که وجود داشته باشد
            #روش کار اینست که از استیت ترکیبی ابتدایی شروع کرده و تنها روی استیت هایی کار میکنیم که به آنها دسترسی داشته ایم 
            if (combined_states[start] in been_saw):#چون ممکن است یک ترکیب به خودش برود . بنابراین در ارایه اضافه میشود . لذا چک میکنیم که تکراری ها را درنظر نگیریم
                start += 1
                continue
            else:
                states = combined_states[start]  #استیت کنونی
                been_saw.append(combined_states[start])
                current_state_1 = states[0]
                current_state_2 = states[1]
                state_value = {}# دیکشنری داخلی تابع انتقال است
                for symbols in self.alphabet:
                    #به ازای هر حرف الفبا چک میکنیم که هر بخش از استیت الحاقی به کجا میرود
                    next_state_1 = self.transition_function[current_state_1][symbols]
                    next_state_2 = L2.transition_function[current_state_2][symbols]
                    next_state = next_state_1 + next_state_2# استیت ترکیبی بعدی شامل استیت بعدی هر بخش استیت ترکیبی فعلی است
                    combined_states.append(next_state)#اضافه کردن استیت ترکیبی به لیست استیت های ترکیبی
                    state_value.update({symbols: next_state})#ساخت دیکشنری داخلی تابع انتقال
                transition_function.update({states: state_value})#ساخت تابع انتقال برای استیت فعلی ترکیبی
                start += 1
        combined_states = list(set(combined_states))# میدانیم که در لیست ممکن است استیت های تکراری باشند . لذا باتبدیل به مجموعه آنها را حذف میکنیم و سپس دوباره تبدیل به لیست میکنیم

        # استیت های پذیرش
        union_final_states = []#استیت های پذیرش اجتماع
        intersect_final_states = []#استیت های پذیرش اشتراک
        subtract_L1L2_final_states = []#استیت های پذیرش زبان اول منهای زبان دوم
        subtract_L2L1_final_states = []
        for states in combined_states:
            # هر استیت در لیست استیت های ترکیبی را انتخاب کرده و براساس قوانین استیت های پذیرش را مشخص میکنیم در هر بخش
            current_state_1 = states[0]
            current_state_2 = states[1]
            #اجتماع
            if ((current_state_1 in self.final_states)
                    or (current_state_2 in L2.final_states)):
                union_final_states.append(states)

            #اشتراک
            if ((current_state_1 in self.final_states)
                    and (current_state_2 in L2.final_states)):
                intersect_final_states.append(states)

            #تفاضل یک از دو
            if ((current_state_1 in self.final_states)
                    and not (current_state_2 in L2.final_states)):
                subtract_L1L2_final_states.append(states)

            #تفاضل دو از یک
            if (not (current_state_1 in self.final_states)
                    and (current_state_2 in L2.final_states)):
                subtract_L2L1_final_states.append(states)

        #اجتماع
        #print(union_final_states)
        union = [
            combined_states, L2.alphabet, initial, union_final_states,
            transition_function
        ]
        print('This is the DFA for Union of Languages \n %s' % (union))

        #اشتراک
        intersection = [
            combined_states, L2.alphabet, initial, intersect_final_states,
            transition_function
        ]
        print('\n\nThis is the DFA for Intersection of Languages \n %s' %
              (intersection))

        #تفاضل یک از دو
        subtraction_l1l2 = [
            combined_states, L2.alphabet, initial, subtract_L1L2_final_states,
            transition_function
        ]
        print('\n\nThis is the DFA for L1-L2 \n %s' % (subtraction_l1l2))
        if (len(subtract_L1L2_final_states) == 0):
            print('L1 is a subset of L2')

        #تفاضل دو از یک
        subtraction_l2l1 = [
            combined_states, L2.alphabet, initial, subtract_L2L1_final_states,
            transition_function
        ]
        print('\n\nThis is the DFA for L2-L1 \n %s' % (subtraction_l2l1))
        if (len(subtract_L2L1_final_states) == 0):
            print('L2 is a subset of L1')

        if ((len(subtract_L1L2_final_states) == 0)
                and (len(subtract_L2L1_final_states) == 0)):
            print('L1 and L2 are the Equals')
        if ((len(subtract_L1L2_final_states) != 0)
                and (len(subtract_L2L1_final_states) != 0)):
            print('L1 and L2 are the Seperated')

    def minimizing(self):
        #مرحله اول : جدول
        pairs = []# لیست شامل تمام ترکیب استیت های ممکن
        for i in self.states:
            for j in self.states:
                if ((i != j) and not (j + i in pairs)):
                    pairs.append(i + j)
        marked_pairs = []#استیت های علامت گذاری شده
        step = 1
        while (True):
            end = 0# متغیر اند برای اینست که زمان متوقف شدن حلقه را بفهمیم
            #زمانی حلقه متوقف میشود که در یک گام کامل ما هیچ استیتی را علامت گذاری نکنیم
            # گام اول
            # در صورتی استیت ها را علامت گذاری کن که یکی پذیرش  و دیگری نباشد
            if (step == 1):
                for pair in pairs:
                    current_state_1 = pair[0]
                    current_state_2 = pair[1]
                    if ((current_state_1 in self.final_states
                         and current_state_2 not in self.final_states)
                            or (current_state_1 not in self.final_states
                                and current_state_2 in self.final_states)):
                        marked_pairs.append(pair)
                        end += 1
                step += 1# بعد از پایان گام اول مقدار استپ را یک عدد زیاد کنیم که در مرحله بعدی وایل به استپ دو بریم

            else:
                for pair in pairs:
                    if (pair not in marked_pairs):# استیت هایی را انتخاب کن که علامت گذاری نشده اند
                        current_state_1 = pair[0]
                        current_state_2 = pair[1]
                        for symbols in self.alphabet:# در این حلقه به ازای هر حرف الفبا چک میکنیم که آیا به استیت های علامتگذاری شده دسترسی داریم یا خیر
                            next_state_1 = self.transition_function[current_state_1][symbols]
                            next_state_2 = self.transition_function[current_state_2][symbols]
                            next_state = next_state_1 + next_state_2
                            next_state_reverse = next_state_2 + next_state_1
                            if (next_state in marked_pairs
                                    or next_state_reverse in marked_pairs): # اگر توانستیم از استیت فعلی با یک حرفی از الفبا به یک استیت علامت گذاری شده بریم.
                                marked_pairs.append(pair)# آنگاه آن استیت را علامتگذاری کن
                                end += 1#برای اینکه بدانیم حداقل یک استیت را علامتگذاری کرده ایم . بنابرین باید حلقه وایل ادامه پیدا کند به ازای گام بعدی
                                break
                if (end == 0):#اگر هیج استیتی علامتگذاری نشده از حلقه وایل بیرون بپر
                    break
                step += 1
        #print(marked_pairs)
        unmarked_pairs = list(set(pairs) - set(marked_pairs))
        if(len(unmarked_pairs)!=0):
            #ساخت اتاماتا
            minimized_states = []#استیت های آتاماتای مینیمایز شده ما
            #در این حلقه ما سعی داریم استیت هایی که با همه ترکیبات ممکناشان علامتگذاری شده اند را بیابیم و سپس به صورت تک استیت در مجموعه استیت هایمان اد کنیم
            # در مثال کتاب این دو استیت ۰ و ۹ هستند
            for i in self.states:
                for n in range(len(unmarked_pairs)):
                    if (i in unmarked_pairs[n]):
                        break
                    if (n == (len(unmarked_pairs) - 1)):#وقتی به این ایف میرسیم یعنی به ازای هیچیک از استیت های علامتگذاری شده استیت مورد نظر ما وجود ندارد . یعنی به طور کامل علامتگذاری شدهه است
                        minimized_states.append(i)
            #print(unmarked_pairs)
            unmarked_pairs.sort()#برای اینکه هربار با ترکیبات مختلفی از استیت های علامتگذاری نشده سروکار نداشته باشیم آنها سورت میکنیم
            equal_states = {}#دیکشنری شامل کلید پارت اول ترکیب استیت ها و با مقدار استیت های معادل
            #در نهایت به دیکشنری میرسیم که به ازای هر کلید در مقدار تمام استیت های معادل را داریم که آنها را میتوانیم یک استیت در نظر بگیریم
            for pair in unmarked_pairs:
                if (equal_states != {}):
                    key = list(equal_states.keys())
                    for n in range(len(key)):
                        if (pair[0] in equal_states[key[n]]):
                            equal_states[key[n]].add(pair[1])
                            break
                        if (n == (len(key) - 1)):
                            equal_states.update({pair[0]: {pair[0], pair[1]}})
                else:
                    equal_states.update({pair[0]: {pair[0], pair[1]}})

            for keys in equal_states.keys():
                minimized_states.append(list(equal_states[keys]))#استیت های معادل به عنوان لیست به عنوان یک تک استیت شناخته میشود
            #print(minimized_states)
            #ساخت تابع انتقال
            new_final_states = []
            #یافتن استیت شروع و فاینال جدید
            for states in minimized_states:
                if (self.initial_state in states):#خانه ای از جدول (که میتواند لیست یا تک کاراکتر باشد) استیت شروع است که شامل استیت شروع باشد
                    new_initial = states
                for final in self.final_states:
                    if (final in states):
                        new_final_states.append(states)
                        break

            #تابع انتفال
            new_transition_func = {}
            for state in minimized_states:
                new_value_dict = {}
                for symbols in self.alphabet:
                    simple_value = self.transition_function[state[0]][symbols]  #مقصد در حالتی که به استیت تنها به طور مستقیم از مبدا میرویم
                    for destination in minimized_states:
                        if (simple_value in destination):
                            value_in_form = destination  #انتخاب کردن لیست شامل استیت مقصد به عنوان مقصد نهایی
                    new_value_dict[symbols] = value_in_form
                new_transition_func.update({str(state): new_value_dict})
            #print(new_transition_func)
            print(
                "\n************This Is The Minimized DFA for Your Selected Language*************\nstates= %s\nalphabet= %s\ninitial state= %s\nfinal states= %s\ntransition function= %s"
                % (minimized_states, self.alphabet, new_initial, new_final_states,
                   new_transition_func))
        else:
            print('Your DFA is Also Minimized')


class NFA:

    def __init__(self, states, alphabet, initial_state, final_states,
                 transition_function):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transition_function = transition_function

    def __str__(self):
        return f"states= {self.states}\nalphabet= {self.alphabet}\ninitial state= {self.initial_state}\nfinal states= {self.final_states}\ntransition function= {self.transition_function}"

    def lambda_deleter(self):#در این متد تابع انتقال بدون انتقال لامبدا ریترن میشود
        new_transition_func={}
        for state in self.states:
            all_trans={}
            for char in self.alphabet:
                all_trans[char]=set()
            first_step = [state]#گام اول شامل استیت هایی می شود که از استیت مورد نظر ما با یک یا چند انتقال لامبدا قابل دسترسی اند
            been_saw = []
            for element in first_step:#در این حلقه تمام استیت هایی که از استیت مورد نظر ما با یک یا چند انتقال لامبدا قابل دسترسی اند را در گام اول اضافه میکنیم
                transition = list(self.transition_function[element].keys())
                if ('$' in transition and element not in been_saw):#اگر استیت ما انتقال لامبدا دارد و برای اولین بار است که میبینیمش
                    been_saw.append(element)
                    for trans in self.transition_function[element]['$']:
                        first_step.append(trans)#انتقال استیت هایی که با انتقال لامبدا قابل دسترسی هستند به لیست گام اول

            for st in first_step:
                #در این حلقه میخواهیم تمام انتقال های حروف الفبا را به ازای تمام استیت های قابل دسترسی با انتقال لامبدا را مشخص کنیم
                enteghal=self.transition_function[st].keys()
                for symbol in self.alphabet:
                    if(symbol in enteghal):#اگر انتقال با حرف الفبا موردنظر وجود داشت آنرا در آل ترنس اد کن
                        all_trans[symbol].add(self.transition_function[st][symbol])
            keys=all_trans.keys()
            for sym in  keys:
                #در این حلقه میخواهیم انتقال های لامبدای پس از انجام انتقال الفبا را به مجموعه انتقالاتمان اضافه کنیم
                #به طور مثال اگر از ۱ با آ به ۳ میرویم و از ۳ با لامبدا میتوانیم به ۴ و ۶ برویم
                #برای انتقال های آ در استیت ۱ ما ۳ و ۴ و ۶ را داریم
                value=list(all_trans[sym])
                #print(value)
                for item in value:
                    item_trans=self.transition_function[item]
                    if('$' in item_trans):
                        for trans in self.transition_function[item]['$']:
                            all_trans[sym].add(trans)
            for key in list(all_trans.keys()):#حذف انتقال هایی که استیت آن را ندارد
                if all_trans[key]==set() :
                    del all_trans[key]
            new_transition_func.update({state:all_trans})
        return new_transition_func
        #print(new_transition_func)#ساخته شد بدون انتقال لامبدا

    def fa_converter(self):
        mark=0
        trans_func=self.transition_function
        #تشخیص انتقال لامبدا داشتن یا نداشتن اتاماتا
        for states in self.states:
            if('$' in list(self.transition_function[states].keys())):
                mark+=1
                break
        if(mark!=0):
            trans_func=self.lambda_deleter()
        
        #ساخت انتقال ها
        fa_states=[self.initial_state]#برای تبدیل به اتاماتای دترمینستیک باید از استیت ابتدایی شروع کنیم
        fa_trans_func={}
        new_trans_func={}
        been_saw=[]
        for state in fa_states:
            if(state not  in been_saw):
                value_dict={}
                been_saw.append(state)
                for alpha in self.alphabet:
                    value_dict[alpha]=set()
                
                for symbol in self.alphabet:
                    pak_state=[]
                    for single_state in state:
                        if(symbol in list(trans_func[single_state].keys())):
                            for  el in trans_func[single_state][symbol]:
                                pak_state.append(el)
                                value_dict[symbol].add(el)
                    if(pak_state!=[] and pak_state not in fa_states):
                        fa_states.append(pak_state)
                new_trans_func.update({str(state):value_dict})
        #اد کردن انتقال استیت برای انتقال هایی که وجود نداشت
        for st in list(new_trans_func.keys()):
            for sym in list(new_trans_func[st].keys()):
                if(new_trans_func[st][sym]==set()):
                    if('@' not in fa_states):
                        fa_states.append('@')
                        val={}
                        for char in self.alphabet:
                            val[char]='@'
                        new_trans_func['@']=val
                    new_trans_func[st][sym]='@'
        #ساخت استیت فاینال جدید
        new_final=[]
        for state in fa_states:
            for  final in self.final_states:
                if(final in state):
                    new_final.append(state)
                    break
        #print(fa_states)
        #print(new_trans_func)
        #ساخت عناصر به حالتی که بتوان آنرا به یک آتاماتا داد
        #ابتدا تمام استیت ها را مجدد نامگذاری میکنیم از ای تا زی
        #این کار به این علت است که ورودیه استاندارد یک آتاماتا دارای نامگذاری تک حرفی است ولی ما در این آتاماتا به عنوان اسم حتی آرایه هم داریم
        state_mark=ord('A')
        fa_form_states=[]
        for states in fa_states:
            if(states!='@'):
                fa_form_states.append(chr(state_mark))
                state_mark+=1
        fa_form_states.append('@')
         #دراین حلقه کار عجیبی صورت نگرفته
        #فقط چون در ادامه مقایسه برابری یک لیست با مجموعه را داریم به خاطر همین اسم هر استیت را مرتب میکنیم
        #مثال روی استیتی به نام [1,2]
        str_form_states=[]#همچنین این آرایه را برای این میسازیم که اسم تمام استیت ها را به شکل رشته کنیم چون کلید تابع انتقال همگی رشته اند
        for num in range(len(fa_states)-1):
            str_form_states.append(str(fa_states[num]))
            fa_states[num]=sorted(fa_states[num])

        #انجام عملیات تبدیل به فرم استاندارد تابع انتقال 
        trans_func_fa_form={}
        for key_state in new_trans_func.keys():
            if(key_state!='@'):
                index=str_form_states.index(key_state)
                key=fa_form_states[index]
            else:
                key='@'
            val={}
            for sym in new_trans_func[key_state].keys():
                if(new_trans_func[key_state][sym]!='@'):
                    value_index=fa_states.index(list(sorted(new_trans_func[key_state][sym])))
                    value_fa_form=fa_form_states[value_index]
                    val[sym]=value_fa_form
                else:
                    val[sym]='@'
            trans_func_fa_form[key]=val
        #print(fa_states)
        #print(fa_form_states)
        #print(new_trans_func)
        #print(trans_func_fa_form)
        #انجام عملیات تبدیل به فرم استاندارد استیت های شروع و پذیرش
        final_fa_form=[]
        for state in new_final:
            index=fa_states.index(sorted(state))
            final_fa_form.append(fa_form_states[index])
        #print(final_fa_form)
        initial_fa_form='A'
        #توانستیم تمام عناصر ورودیه لازم برای آتاماتا را به فرم درست درآوریم 
        #حال با ریترن کردن یک دی اف ای ما یک آتاماتای نان دترمینستیکی داریم که دترمینستیک شده و میتوان تمام متدهای دی افی ای را روی آن فراخوانی کرد
        return DFA(fa_form_states,self.alphabet,initial_fa_form,final_fa_form,trans_func_fa_form)
