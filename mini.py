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
