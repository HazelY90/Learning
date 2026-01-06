import json

class Dicipline:
    def __init__(self,name,exp=0):
        self.name=name
        self.exp=exp
    
    @property
    def exp(self):
        return self.__exp
    @exp.setter
    def exp(self,exp:int):
        if exp>=0:
            self.__exp=exp
        else:
            raise ValueError("Illegal exp value.")
    
    @property
    def level(self):
        '''Return the level'''
        if self.exp<=15000:
            return self.exp//500
        elif self.exp<=85000:
            return 30+(self.exp-15000)//1000
        else:
            return 100 + int(((self.exp - 85000) / 1000) ** 0.7)
    
    @property
    def currentExp(self):
        '''Return the experience of current level.'''
        if self.level<=30:
            return self.exp % 500
        elif self.level<=100:
            return (self.exp-15000) % 1000
        else:
            return self.exp-85000-int(1000 * ((self.level-100) ** (1 / 0.7)))
    
    @property
    def expToNext(self):
        '''Return the value of experience needed to next level.'''
        if self.level<=30:
            return 500-self.currentExp
        elif self.level<=100:
            return 1000-self.currentExp
        else:
            return 85000+int(1000*((self.level+1-100)**(1/0.7)))-self.exp
              

    def updateExp(self):
        '''
        Docstring for updateExp

        :input: study_time,non-negtive integer. 
        :input: exercises,non-negtive integer. 
        Update the exp.
        No return value.
        '''
        while True:
            try:
                study_time = int(input(f"Enter the study time for {self.name} in minutes: "))
                if study_time<0:
                    raise ValueError("Negative value not allowed")
                break 
            except ValueError:
                print("Illegal input of study time. It should be non-negtive integer.")
        
        while True:
            try:
                exercises = int(input(f"Enter the number of exercises completed for {self.name}: "))
                if exercises <0:
                    raise ValueError("Negative value not allowed")
                break
            except ValueError:
                print("Illegal input of exercises. It should be non-negtive integer.")

        exp = study_time + 50 * exercises
        self.exp += exp
    
    def __str__(self):
        return f"Dicipline:{self.name}\nCurrent level:{self.level}\nCurrent exp:{self.currentExp}\nExp to next level:{self.expToNext}"
    
    def __repr__(self):
        return f"Dicipline:{self.name}\nTotal exp:{self.exp}\nCurrent level:{self.level}\nCurrent exp:{self.currentExp}\n\nExp to next level:{self.expToNext}"  

    def toDict(self):
        return {"name":self.name,"exp":self.exp}

class User:
    def __init__(self,name):
        self.name=name
        self.diciplines=[]
    
    def add_diciplines(self,name,exp=0):
        new=Dicipline(name,exp)
        self.diciplines.append(new)
    
    def toDict(self):
        dict={}
        dict["name"]=self.name
        dict["diciplines"]=[d.toDict() for d in self.diciplines]
        return dict
    
    def save(self,file):
        with open(file,"w") as f:
            json.dump(self.toDict(),f,indent=4)
        print("Data saved.")
    
    def __repr__(self):
        return str(self.toDict())

    @classmethod
    def load_in(cls,file):
        try:
            with open(file, 'r') as f:
                data=json.load(f)
            if not data:
                return None
            user=cls(data["name"])
            for d in data["diciplines"]:
                user.add_diciplines(d["name"],d["exp"])
            return user
        except (FileNotFoundError,json.JSONDecodeError):
            print("File not found.")
            return None
    
    @classmethod
    def create_new_user(cls):
        name=input("Enter the name of the user:")
        while not name:
            print("Empty value not allowed.")
            name=input("Enter the name of the user:")
        user=cls(name)
        n=int(input("Enter the number of diciplines (positive integer):"))
        while n<=0:
            print("Illegal value. The number should be a positive integer.")
            n=int(input("Enter the number of diciplines (positive integer):"))
        for i in range(n): 
            dicipline=input(f"Enter the name of dicipline {i+1}:")
            while not dicipline:
                print("Empty value not allowed.")
                dicipline=input(f"Enter the name of dicipline {i+1}:")
            user.add_diciplines(dicipline)
        return user

def main():
    user=User.load_in("study_data.json")
    if not user:
        user=User.create_new_user()
    for d in user.diciplines:
        d.updateExp()
        print(d)
    user.save("study_data.json")
    print("Done")

if __name__ == "__main__":
    main()