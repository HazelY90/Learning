import json
from datetime import date
from collections import OrderedDict
from matplotlib import pyplot as plt

class Dicipline:
    def __init__(self,name,exp=0):
        self.name=name
        self.exp=exp
        self.__studytime=OrderedDict()
        self.__exercise=OrderedDict()
    
    @property
    def exp(self):
        return self.__exp
    @exp.setter
    def exp(self,exp:int):
        if exp>=0:
            self.__exp=exp
        else:
            raise ValueError("Illegal exp value.")
    
    # Level, exp of current level, exp to next level are calculated dynamically.
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
        Update the exp and store the data of study time and exercises.
        No return value.
        '''
        # get the date ,if the date already exists, ask user whether to update or not.
        day=str(date.today())
        if day in self.__sdutytime or day in self.__exercise :
            update=""
            while update!="yes" and update!="no":
                update=input("Today's data was recorded. Do you want to update it (substitude the old data with the new)? (yes/no):")
            if update=="no":
                return    
        # input user data of study time and exercises
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
        
        # add the data to ordered dictonary and keep the number of data under 30 (inclusive)
        self.__studytime[day]=study_time
        while len(self.__studytime)>30:
            self.__studytime.popitem(last=False)
        
        self.__exercise[day]=exercises
        while len(self.__exercise)>30:
            self.__exercise.popitem(last=False)

        # update the exp
        exp = study_time + 50 * exercises
        self.exp += exp
    
    def __str__(self):
        return f"Dicipline:{self.name}\nCurrent level:{self.level}\nCurrent exp:{self.currentExp}\nExp to next level:{self.expToNext}"
    
    def __repr__(self):
        return f"Dicipline:{self.name}\nTotal exp:{self.exp}\nCurrent level:{self.level}\nCurrent exp:{self.currentExp}\n\nExp to next level:{self.expToNext}"  

    def toDict(self):
        return {"name":self.name,"exp":self.exp,"studytime":self.__studytime,"exercise":self.__exercise}
    
    def get_study_data(self):
        #get data as list for visualization

        days=list(self.__studytime.keys())[-7:]
        times=list(self.__studytime.values())[-7:]
        exercises=list(self.__exercise.values())[-7:]

        return (days,times,exercises)
    
    def read_study_data(self,studytime,exercises):
        for day,time in studytime.items():
            self.__studytime[day]=time
        for day,exercise in exercises.items():
            self.__exercise[day]=exercise



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
    
    def visualize(self):
        fig,axs=plt.subplots(2,1,figsize=(8,6),sharex=True)
        width = 0.3
        n=len(self.diciplines)
        for i,dicipline in enumerate(self.diciplines):
            days,times,exercises=dicipline.get_study_data()

            base_x=range(len(days)) 
            offset=i*width-(n-1)*width/2
            x=[j+offset for j in range(len(days))]

            axs[0].bar(x,times,label=f"{dicipline.name}",width = 0.3)
            axs[1].bar(x,exercises,label=f"{dicipline.name}",width = 0.3)

            if i==len(self.diciplines)-1:
                plt.xticks(base_x, days, rotation=45)

        axs[0].set_title(f"Study Time")
        axs[0].set_xlabel("Date")
        axs[0].set_ylabel("Study Time by Minutes")
        axs[0].legend()
        axs[1].set_title(f"Number of Exercises")
        axs[1].set_xlabel("Date")
        axs[1].set_ylabel("Number of Exercises")
        axs[1].legend()

        plt.tight_layout()
        plt.show()

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
                user.diciplines[-1].read_study_data(d["studytime"],d["exercise"])
                
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
    user.visualize()
    user.save("study_data.json")
    print("Done")

if __name__ == "__main__":
    main()
