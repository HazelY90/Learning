from study_simulator import User,Dicipline
import random
from datetime import date,timedelta
import json

def generate_test_data():
    test_user = User("TestStudent")
    test_user.add_diciplines("Python")
    test_user.add_diciplines("Java")


    start_date = date.today() - timedelta(days=29)
    for i in range(30):
        current_day = str(start_date + timedelta(days=i))
        
        study_time = random.randint(30, 180)
        exercises = random.randint(0, 10)
        test_user.diciplines[0]._Dicipline__studytime[current_day] = study_time
        test_user.diciplines[0]._Dicipline__exercise[current_day] = exercises
        test_user.diciplines[0].exp += (study_time + 50 * exercises)
        study_time = random.randint(30, 180)
        exercises = random.randint(0, 10)
        test_user.diciplines[1]._Dicipline__studytime[current_day] = study_time
        test_user.diciplines[1]._Dicipline__exercise[current_day] = exercises
        test_user.diciplines[1].exp += (study_time + 50 * exercises)

    data = test_user.toDict()
    with open("test_user_data.json", "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4, default=str)
    

if __name__ == "__main__":
    generate_test_data()
    user=User.load_in("test_user_data.json")
    user.save("data.json")
    user.visualize()
    print("Done")