class PasswordStrengthChecker(object):
    def __init__(self,strict=True):
        self.strict = strict
    def classify_chr(self, c):
        """
        return values meaning:
            0: lower case
            1: upper case
            2: number
            3: special character
        """
        if c.islower():
            # lower case
            return 0
        elif c.isupper():
            # upper case
            return 1
        elif ord('0')<=ord(c)<=ord('9'):
            # number
            return 2
    def is_secure(self,pwd):
        """
        return True, "some_msg" if pwd is secure
        return False, "err_msg" if pwd isn't secure
        """
        if self.strict==False:
            if len(pwd)>0:
                return True, "password is secure"
            else:
                return False, "password must not be blank"
        if len(pwd)<8:
            return False, "password length must be greater or equal to 8"
        cnt_lst = [0,0,0,0]
        for c in pwd:
            cnt_lst[self.classify_chr(c)]=1
        if sum(cnt_lst) != 3:
            return False, "password must contain at least one uppercase letter, lowercase letter, number and special character."
        return True, "password is secure"